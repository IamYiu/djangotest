# Generated by Django 5.0.7 on 2024-08-11 20:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sun', '0007_moneybet'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneybet',
            name='created_date_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
