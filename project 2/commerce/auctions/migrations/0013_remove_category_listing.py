# Generated by Django 4.2.5 on 2023-10-10 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_bid_category_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='listing',
        ),
    ]