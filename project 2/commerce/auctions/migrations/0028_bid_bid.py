# Generated by Django 4.2.5 on 2023-10-15 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_closebid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(default=0),
        ),
    ]
