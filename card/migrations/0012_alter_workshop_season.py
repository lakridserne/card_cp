# Generated by Django 3.2.18 on 2023-09-03 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0011_alter_workshop_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workshops', to='card.season'),
        ),
    ]