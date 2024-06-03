# Generated by Django 5.0.3 on 2024-05-28 13:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(blank=True, default='', max_length=140)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
