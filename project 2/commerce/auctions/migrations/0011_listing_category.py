# Generated by Django 4.2.5 on 2023-10-10 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_remove_listing_categoryid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, default='000', max_length=64),
        ),
    ]
