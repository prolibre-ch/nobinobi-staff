# Generated by Django 2.0.9 on 2018-11-07 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nobinobi_staff', '0004_team_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qualification',
            name='used_ratio',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='preparation_time',
        ),
    ]
