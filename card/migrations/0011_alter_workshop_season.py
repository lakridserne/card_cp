# Generated by Django 3.2.18 on 2023-09-03 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0010_participantsfile_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workshop', to='card.season'),
        ),
    ]