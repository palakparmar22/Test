# Generated by Django 5.0.3 on 2024-05-02 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_masteruser',
            field=models.BooleanField(default=False),
        ),
    ]
