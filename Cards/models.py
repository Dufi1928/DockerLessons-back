from django.db import models
from django.conf import settings

class CardCollection(models.Model):
    is_public = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='collections', null=True)
    categories = models.ManyToManyField('Category', related_name='collections')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_cards'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserCardCollection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_collections'
    )
    collection = models.ForeignKey(CardCollection, on_delete=models.CASCADE, related_name='collection_subscribers', null=True)

class Card(models.Model):
    collection = models.ForeignKey(CardCollection, on_delete=models.CASCADE, related_name='cards')
    front_content = models.TextField()
    back_content = models.TextField()
    image_url = models.URLField(blank=True, null=True)



class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)



class Subject(models.Model):
    categories = models.ManyToManyField(Category, related_name='subjects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


