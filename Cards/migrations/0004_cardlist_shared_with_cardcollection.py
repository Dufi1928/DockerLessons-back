# Generated by Django 4.2.7 on 2023-11-27 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Cards', '0003_alter_card_word'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardlist',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_lists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CardCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_collections', to=settings.AUTH_USER_MODEL)),
                ('lists', models.ManyToManyField(to='Cards.cardlist')),
                ('shared_with', models.ManyToManyField(blank=True, related_name='shared_collections', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
