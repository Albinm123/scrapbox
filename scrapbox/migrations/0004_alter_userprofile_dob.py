# Generated by Django 4.2.7 on 2023-12-15 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapbox', '0003_rename_scap_bids_scrap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(null=True),
        ),
    ]