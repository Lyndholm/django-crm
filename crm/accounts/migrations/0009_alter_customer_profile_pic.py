# Generated by Django 4.2 on 2023-04-12 12:09

from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default-avatar.png', null=True, upload_to=pathlib.PurePosixPath('/home/www/Code/django-crm-course/crm/static/images')),
        ),
    ]
