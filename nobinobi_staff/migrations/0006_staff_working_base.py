# Generated by Django 2.0.9 on 2018-11-26 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nobinobi_staff', '0005_auto_20181116_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='working_base',
            field=models.FloatField(default=40, verbose_name='Working base'),
        ),
    ]
