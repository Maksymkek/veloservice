# Generated by Django 4.1.3 on 2022-12-14 20:36

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
            name='BicycleStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Bicycle name')),
            ],
        ),
        migrations.CreateModel(
            name='Bicycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='', verbose_name='Bicycle photo')),
                ('name', models.CharField(max_length=50, verbose_name='Bicycle name')),
                ('description', models.TextField(verbose_name='Description')),
                ('usages', models.PositiveIntegerField(verbose_name='Amount of usages')),
                ('status', models.CharField(max_length=50, verbose_name='Status')),
                ('price', models.PositiveIntegerField(verbose_name='Hire price')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.bicyclestation')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
