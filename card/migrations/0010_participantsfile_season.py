# Generated by Django 3.2.15 on 2022-08-16 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0009_remove_participants_members_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='participantsfile',
            name='season',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='card.season'),
            preserve_default=False,
        ),
    ]