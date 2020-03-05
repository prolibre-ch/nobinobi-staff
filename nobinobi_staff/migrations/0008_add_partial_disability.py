# Generated by Django 2.0.13 on 2020-03-05 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import nobinobi_staff.models


class Migration(migrations.Migration):

    dependencies = [
        ('nobinobi_staff', '0007_auto_20200221_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='partial_disability',
            field=models.IntegerField(blank=True, help_text='In percentage %', null=True, verbose_name='Partial disability'),
        ),
    ]
