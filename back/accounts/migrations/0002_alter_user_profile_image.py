# Generated by Django 4.2.16 on 2024-11-25 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default='static/images/default.png', upload_to='profile_images/', verbose_name=' '),
        ),
    ]
