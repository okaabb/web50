# Generated by Django 4.2.5 on 2023-10-08 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_listings_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='status',
            new_name='available',
        ),
    ]