# Generated by Django 4.2.7 on 2023-12-08 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrap',
            name='scrap_pic',
            field=models.ImageField(null=True, upload_to='images\\scrap_img'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='images\\profile_img'),
        ),
    ]