# Generated by Django 4.2.16 on 2024-11-19 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='show_reviews',
            field=models.BooleanField(default=False),
        ),
    ]
