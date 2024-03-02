from rest_framework import serializers
from .models import CardCollection, Subject, Category, Card

class CardCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardCollection
        fields = ['id', 'is_public', 'title', 'description', 'subject', 'categories', 'creator', 'created_at', 'updated_at']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'collection', 'front_content', 'back_content', 'image_url']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class SubjectSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'categories']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        subject = Subject.objects.create(**validated_data)
        for category_data in categories_data:
            subject.categories.add(category_data)
        return subject

