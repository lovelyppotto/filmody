# Generated by Django 4.2.16 on 2024-11-24 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('audience_acc', models.IntegerField()),
                ('genre', models.CharField(max_length=100)),
                ('poster_url', models.CharField(max_length=500)),
                ('plot', models.TextField()),
                ('actors', models.CharField(max_length=200)),
                ('open_year', models.CharField(max_length=4)),
                ('nation', models.CharField(max_length=50)),
                ('rating', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('director', models.ManyToManyField(related_name='movies', to='movies.director')),
                ('like_users', models.ManyToManyField(blank=True, related_name='liked_movies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BoxOffice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_date', models.DateField()),
                ('rank', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
    ]
