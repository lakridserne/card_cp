# Generated by Django 2.2.4 on 2019-08-12 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0004_wifipasswords'),
    ]

    operations = [
        migrations.AddField(
            model_name='wifipasswords',
            name='random_person',
            field=models.BooleanField(default=False, verbose_name='Tilfældig person'),
        ),
    ]
