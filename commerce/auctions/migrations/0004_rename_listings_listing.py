# Generated by Django 4.2.5 on 2023-10-08 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_min_bid_listings_current_bid_listings_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Listings',
            new_name='Listing',
        ),
    ]
