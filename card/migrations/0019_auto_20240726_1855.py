# Generated by Django 3.2.25 on 2024-07-26 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0018_auto_20240726_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='season',
            name='ice',
        ),
        migrations.RemoveField(
            model_name='season',
            name='ice_require_card',
        ),
        migrations.RemoveField(
            model_name='season',
            name='ice_require_row',
        ),
        migrations.RemoveField(
            model_name='season',
            name='merchandise',
        ),
        migrations.RemoveField(
            model_name='season',
            name='merchandise_require_card',
        ),
        migrations.RemoveField(
            model_name='season',
            name='merchandise_require_row',
        ),
        migrations.RemoveField(
            model_name='season',
            name='stickers',
        ),
        migrations.RemoveField(
            model_name='season',
            name='stickers_require_card',
        ),
        migrations.RemoveField(
            model_name='season',
            name='stickers_require_row',
        ),
        migrations.AddField(
            model_name='season',
            name='basic_award',
            field=models.IntegerField(default=4, max_length=2, verbose_name='Antal gange for at tjene basal præmie'),
        ),
        migrations.AddField(
            model_name='season',
            name='basic_award_require_card',
            field=models.BooleanField(default=False, verbose_name='Kortet skal være brugt for at tælle for basal præmie'),
        ),
        migrations.AddField(
            model_name='season',
            name='basic_award_require_row',
            field=models.BooleanField(default=True, verbose_name='Gangene skal være registreret i træk for basal præmie'),
        ),
        migrations.AddField(
            model_name='season',
            name='medium_award',
            field=models.IntegerField(default=7, max_length=2, verbose_name='Antal gange for at tjene medium præmie'),
        ),
        migrations.AddField(
            model_name='season',
            name='medium_award_require_card',
            field=models.BooleanField(default=True, verbose_name='Kortet skal være brugt for at tælle for medium præmie'),
        ),
        migrations.AddField(
            model_name='season',
            name='medium_award_require_row',
            field=models.BooleanField(default=True, verbose_name='Gangene skal være registreret i træk for medium præmie'),
        ),
        migrations.AddField(
            model_name='season',
            name='season_award',
            field=models.IntegerField(default=12, max_length=2, verbose_name='Antal gange for at tjene sæson præmie'),
        ),
        migrations.AddField(
            model_name='season',
            name='season_award_require_card',
            field=models.BooleanField(default=False, verbose_name='Kortet skal være brugt for at tælle for sæson præmie'),
        ),
        migrations.AddField(
            model_name='season',
            name='season_award_require_row',
            field=models.BooleanField(default=False, verbose_name='Gangene skal være registreret i træk for sæson præmie'),
        ),
    ]