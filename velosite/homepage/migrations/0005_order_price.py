# Generated by Django 4.1.3 on 2022-12-20 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_rename_trolley_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='Rental price'),
        ),
    ]
