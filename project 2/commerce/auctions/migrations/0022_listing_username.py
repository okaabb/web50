# Generated by Django 4.2.5 on 2023-10-15 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_comment_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='username',
            field=models.TextField(default='None'),
        ),
    ]
