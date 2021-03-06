# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-02-07 21:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_dtm', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Registreret')),
                ('status', models.CharField(choices=[('NO', 'Afbud'), ('PR', 'Til stede')], max_length=2, verbose_name='Fremmøde status')),
            ],
            options={
                'verbose_name': 'Fremmøde',
                'verbose_name_plural': 'Fremmøde',
            },
        ),
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Kortnummer')),
                ('activated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Aktiveret')),
                ('deactivated', models.DateTimeField(blank=True, null=True, verbose_name='Deaktiveret')),
            ],
            options={
                'verbose_name': 'Kort',
                'verbose_name_plural': 'Kort',
            },
        ),
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('members_id', models.CharField(max_length=6, unique=True, verbose_name='ID i medlemssystemet')),
                ('name', models.CharField(max_length=200, verbose_name='Navn')),
                ('birthday', models.DateField(verbose_name='Fødselsdag')),
            ],
            options={
                'verbose_name': 'Deltager',
                'verbose_name_plural': 'Deltagere',
            },
        ),
        migrations.CreateModel(
            name='ParticipantsFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.FileField(upload_to='')),
            ],
            options={
                'verbose_name': 'Upload medlemsfil',
                'verbose_name_plural': 'Upload medlemsfiler',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Navn')),
                ('start_date', models.DateField(verbose_name='Startdato')),
                ('end_date', models.DateField(verbose_name='Slutdato')),
                ('weekday', models.CharField(choices=[('0', 'Mandag'), ('1', 'Tirsdag'), ('2', 'Onsdag'), ('3', 'Torsdag'), ('4', 'Fredag'), ('5', 'Lørdag'), ('6', 'Søndag')], max_length=2, verbose_name='Ugedag')),
            ],
            options={
                'verbose_name': 'Sæson',
                'verbose_name_plural': 'Sæsoner',
            },
        ),
        migrations.CreateModel(
            name='SeasonParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Tilføjet')),
                ('stopped', models.DateTimeField(blank=True, null=True, verbose_name='Stoppet')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Participants')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Season')),
            ],
            options={
                'verbose_name': 'Sæsondeltager',
                'verbose_name_plural': 'Sæsondeltagere',
            },
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Navn')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Season')),
            ],
            options={
                'verbose_name': 'Workshop',
                'verbose_name_plural': 'Workshops',
            },
        ),
        migrations.CreateModel(
            name='WorkshopParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateField(default=django.utils.timezone.now, verbose_name='Tilføjet')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Participants')),
                ('seasonparticipant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.SeasonParticipant')),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Workshop')),
            ],
            options={
                'verbose_name': 'Workshopdeltager',
                'verbose_name_plural': 'Workshopdeltagere',
            },
        ),
        migrations.AddField(
            model_name='cards',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Participants'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Participants'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Season'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='workshop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Workshop'),
        ),
    ]
