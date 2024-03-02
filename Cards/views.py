from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from Authentification.models import User
from .serializers import CardCollectionSerializer, CardSerializer, CategorySerializer,SubjectSerializer
from .models import Card, UserCardCollection, CardCollection,Category

import jwt
from django.conf import settings

def get_user_from_token(token):
    if not token:
        raise AuthenticationFailed('No token provided')
    try:
        token = token.split(' ')[1]
    except IndexError:
        raise AuthenticationFailed('Token format invalid')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token expired')
    except jwt.DecodeError:
        raise AuthenticationFailed('Invalid token')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')
    user_id = payload.get('id')
    if not user_id:
        raise AuthenticationFailed('Invalid token - ID not found')
    user = User.objects.get(id=user_id)
    return user



class CreateCategoryView(APIView):
    def post(self, request):

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateSubjectView(APIView):
    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCollectionsView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('No token provided')

        user = get_user_from_token(token)

        try:
            user_collections = UserCardCollection.objects.filter(user=user)
            collections = [uc.collection for uc in user_collections]
            serializer = CardCollectionSerializer(collections, many=True)
            return Response(serializer.data)
        except UserCardCollection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserCreatedCollectionsView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('No token provided')
        user = get_user_from_token(token)

        try:
            user_created_collections = CardCollection.objects.filter(creator=user)
            serializer = CardCollectionSerializer(user_created_collections, many=True)
            return Response(serializer.data)
        except CardCollection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class AddCardCollectionView(APIView):
    def post(self, request, collection_id):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('No token provided')

        user = get_user_from_token(token)

        try:
            collection = CardCollection.objects.get(id=collection_id)
            UserCardCollection.objects.create(user=user, collection=collection)
            return Response({'message': 'Collection added successfully'}, status=status.HTTP_201_CREATED)
        except CardCollection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

class CreateCollectionView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('No token provided')

        user = get_user_from_token(token)

        data = request.data
        data['creator'] = user.id

        serializer = CardCollectionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllCategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubjectsByCategoryView(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            subjects = category.subjects.all()
            serializer = SubjectSerializer(subjects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


class CreateMultipleCardsView(APIView):
    def post(self, request):
        try:
            cards_data = request.data  # Expecting a list of card details

            if not cards_data or 'collection_id' not in cards_data[0]:
                return Response({'error': 'Collection ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            collection_id = cards_data[0]['collection_id']
            collection = CardCollection.objects.get(id=collection_id)

            for card_data in cards_data:
                card_data['collection'] = collection.id
                serializer = CardSerializer(data=card_data)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()

            return Response({'message': 'Cards created successfully'}, status=status.HTTP_201_CREATED)
        except CardCollection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)


class CreateCardView(APIView):
    def post(self, request):
        try:
            card_data = request.data
            collection_id = card_data.get('collection_id')

            if not collection_id:
                return Response({'error': 'Collection ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            collection = CardCollection.objects.get(id=collection_id)
            card_data['collection'] = collection.id

            serializer = CardSerializer(data=card_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CardCollection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)
