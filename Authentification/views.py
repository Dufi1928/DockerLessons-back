from django.contrib.auth.models import User
import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from django.contrib.auth.hashers import make_password

from .models import User
from .serializers import GetUserSerializer
from .serializers import UserSerializer
from .serializers import GetUserPseudosSerializer

from cryptography.hazmat.primitives.asymmetric import rsa  # Import des fonctions pour générer des clés RSA
from cryptography.hazmat.primitives.serialization import (  # Import des fonctions de sérialisation
    Encoding,  # Encodage de la clé
    PrivateFormat,  # Format de clé privée
    PublicFormat,  # Format de clé publique
    NoEncryption  # Aucun chiffrement de la clé
)
from cryptography.hazmat.backends import default_backend #Backend cryptographique par défaut pour les opérations cryptographiques.


def generate_jwt(user):
    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def authenticate_user(email, password=None):
    user = User.objects.filter(email=email).first()

    if not user:
        return None

    if password and not user.check_password(password):
        return None

    return user


class CheckIfUserExist(APIView):
    @staticmethod
    def post(request):
        email = request.data.get('email')
        passkey = request.data.get('passkey', None)
        pseudo = request.data.get('email')
        first_name = request.data.get('firstName')
        last_name = request.data.get('lastName')
        small_size_avatar = request.data.get('smallSizeAvatar')

        user_with_email = User.objects.filter(email=email).first()

        user_with_pseudo = User.objects.filter(pseudo=pseudo).first() if pseudo else None

        if passkey == settings.SECRET_KEY:
            if user_with_email:
                token = generate_jwt(user_with_email)
                return Response({'jwt': token}, status=200)
            else:
                private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,
                    backend=default_backend()
                )
                # Serialize the private key in PEM format without encryption
                private_key_pem = private_key.private_bytes(
                    encoding=Encoding.PEM,
                    format=PrivateFormat.PKCS8,
                    encryption_algorithm=NoEncryption()
                )
                # Generate the corresponding public key
                public_key = private_key.public_key()

                # Serialize the public key in PEM format
                public_key_pem = public_key.public_bytes(
                    encoding=Encoding.PEM,
                    format=PublicFormat.SubjectPublicKeyInfo
                )

                user = User.objects.create(
                    username=first_name,
                    email=email,
                    pseudo=pseudo,
                    first_name=first_name,
                    last_name=last_name,
                    small_size_avatar=small_size_avatar,
                    public_key=public_key_pem.decode(),  # Stocker la clé publique dans la base de données
                    private_key=private_key_pem.decode()  # Stocker la clé privée dans la base de données
                )
                UserSerializer(user)
                token = generate_jwt(user)
                return Response({'jwt': token}, status=200)

        elif user_with_email:
            return Response({'error_email': 'User with this email already exists', 'error_pseudo': 'User with this pseudo already exists'}, status=200)
        elif user_with_email and user_with_pseudo:
            return Response({'error_email': 'User with this email already exists', 'error_pseudo': 'User with this pseudo already exists'}, status=400)
        elif user_with_email:
            return Response({'error_email': 'User with this email already exists'}, status=400)
        elif user_with_pseudo:
            return Response({'error_pseudo': 'User with this pseudo already exists'}, status=400)
        else:
            return Response({'message': 'User with this email or pseudo does not exist'}, status=200)



class Register(APIView):
    def post(self, request):
        email = request.data.get('email')
        pseudo = request.data.get('pseudo')
        password = request.data.get('password')
        first_name = request.data.get('firstName')
        last_name = request.data.get('lastName')

        user_with_email = User.objects.filter(email=email).first()
        user_with_pseudo = User.objects.filter(pseudo=pseudo).first()

        if user_with_email:
            return Response({'error': 'User with this email already exists'}, status=400)
        elif user_with_pseudo:
            return Response({'error': 'User with this pseudo already exists'}, status=400)
        else:
            # Generate the private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            # Serialize the private key in PEM format without encryption
            private_key_pem = private_key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.PKCS8,
                encryption_algorithm=NoEncryption()
            )
            # Generate the corresponding public key
            public_key = private_key.public_key()

            # Serialize the public key in PEM format
            public_key_pem = public_key.public_bytes(
                encoding=Encoding.PEM,
                format=PublicFormat.SubjectPublicKeyInfo
            )

            hashed_password = make_password(password)
            user = User.objects.create(
                username=first_name,
                email=email,
                pseudo=pseudo,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                public_key=public_key_pem.decode(),  # Stocker la clé publique dans la base de données
                private_key=private_key_pem.decode()  # Stocker la clé privée dans la base de données
            )

            serializer = UserSerializer(user)

            user = authenticate_user(email, password)
            token = generate_jwt(user)

            response = Response({'message': 'User registered successfully', 'user': serializer.data})
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {'jwt': token}

            return response


class Login(APIView):
    @staticmethod
    def post(request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate_user(email, password)
        if not user:
            raise AuthenticationFailed('User not found or incorrect password')

        token = generate_jwt(user)
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        return response


class checkLoginView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response({'status': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'status': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(f"Error decoding token: {e}")
            return Response({'status': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(id=payload['id']).first()

        if not user:
            return Response({'status': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'status': 'logged in', 'id': user.id}, status=status.HTTP_200_OK)

class UserView(APIView):
    @staticmethod
    def get(request):
        # Récupérer le token de l'en-tête 'Authorization'
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('No token provided')

        # Supposer que le token est préfixé par 'Bearer'
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            raise AuthenticationFailed('Token format invalid')

        # Déchiffrer et valider le token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except Exception as e:
            print(f"Error decoding token: {e}")
            raise AuthenticationFailed('Invalid token')

        # Récupérer l'utilisateur et retourner ses données
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)




class UserDetail(APIView):
    def get(self, request, user_id, format=None):
        if user_id is not None:
            try:
                user = User.objects.get(pk=user_id)
                serializer = GetUserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "No id provided"}, status=status.HTTP_400_BAD_REQUEST)


class GetUsersNotif(APIView):
    def post(self, request):
        user_ids = request.data.get('senders', [])
        users = User.objects.filter(id__in=user_ids)
        serializer = GetUserPseudosSerializer(users, many=True)
        return Response(serializer.data)