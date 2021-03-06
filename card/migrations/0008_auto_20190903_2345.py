# Generated by Django 2.2.4 on 2019-09-03 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0007_wifipasswords_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wifipasswords',
            name='random_person',
        ),
        migrations.CreateModel(
            name='WiFiFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssid', models.CharField(max_length=32, verbose_name='SSID')),
                ('wifi_password', models.CharField(blank=True, max_length=128, null=True, verbose_name='WiFi Password')),
                ('data', models.FileField(upload_to='')),
                ('for_season', models.BooleanField(default=False, help_text='Skal koderne være til sæsonen? Alternativet er at de bruges til hver deltager på sæsonen (tilfældig kode til hver indtil der ikke er flere tilbage på den dato).', verbose_name='Koder til sæsonen?')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Season')),
            ],
            options={
                'verbose_name': 'Upload WiFi kode',
                'verbose_name_plural': 'Upload WiFi koder',
            },
        ),
    ]
