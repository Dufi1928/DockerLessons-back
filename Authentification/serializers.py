from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'small_size_avatar']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'small_size_avatar': {'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



class GetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'short_description', 'email', 'gender', 'online', 'small_size_avatar',
                  'big_size_avatar', 'pseudo', 'friends', 'age']



class GetUserPseudosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'pseudo']