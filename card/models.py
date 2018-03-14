from django.db import models
from datetime import datetime, timedelta
from django.template import Engine, Context
from django.core.mail import send_mail
from django.utils import timezone, html
import csv

# Create your models here.

class Participants(models.Model):
    class Meta:
        verbose_name = "Deltager"
        verbose_name_plural = "Deltagere"
    members_id = models.CharField('ID i medlemssystemet',max_length=6,blank=False,null=False,unique=True)
    name = models.CharField('Navn',max_length=200)
    birthday = models.DateField('Fødselsdag')

    def __str__(self):
        return self.name

    def age_years(self):
        today = timezone.now().date()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    age_years.admin_order_field = '-birthday'
    age_years.short_description = "Alder"

class Cards(models.Model):
    class Meta:
        verbose_name = "Kort"
        verbose_name_plural = "Kort"
    participant = models.ForeignKey(Participants,on_delete=models.CASCADE)
    card_number = models.CharField('Kortnummer',max_length=10,unique=True,blank=True,null=True)
    activated = models.DateTimeField('Aktiveret',blank=False,null=False,default=timezone.now)
    deactivated = models.DateTimeField('Deaktiveret',blank=True,null=True)

class Season(models.Model):
    class Meta:
        verbose_name = "Sæson"
        verbose_name_plural = "Sæsoner"
    MONDAY = "0"
    TUESDAY = "1"
    WEDNESDAY = "2"
    THURSDAY = "3"
    FRIDAY = "4"
    SATURDAY = "5"
    SUNDAY = "6"
    DAYS_CHOICES = (
        (MONDAY, 'Mandag'),
        (TUESDAY, 'Tirsdag'),
        (WEDNESDAY, 'Onsdag'),
        (THURSDAY, 'Torsdag'),
        (FRIDAY, 'Fredag'),
        (SATURDAY, 'Lørdag'),
        (SUNDAY, 'Søndag')
    )
    name = models.CharField('Navn',max_length=200)
    start_date = models.DateField('Startdato',blank=False,null=False)
    end_date = models.DateField('Slutdato',blank=False,null=False)
    weekday = models.CharField('Ugedag',blank=False,null=False,max_length=2,choices=DAYS_CHOICES)

    def __str__(self):
        return self.name

class SeasonParticipant(models.Model):
    class Meta:
        verbose_name = "Sæsondeltager"
        verbose_name_plural = "Sæsondeltagere"
    season = models.ForeignKey(Season,on_delete=models.CASCADE)
    participant = models.ForeignKey(Participants,on_delete=models.CASCADE)
    added = models.DateTimeField('Tilføjet',default=timezone.now)
    stopped = models.DateTimeField('Stoppet',blank=True,null=True)
    def __str__(self):
        return self.participant.name + ", " + self.season.name

class Workshop(models.Model):
    class Meta:
        verbose_name = "Workshop"
        verbose_name_plural = "Workshops"
    name = models.CharField('Navn',max_length=200)
    season = models.ForeignKey(Season,on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ", " + self.season.name

class WorkshopParticipant(models.Model):
    class Meta:
        verbose_name = "Workshopdeltager"
        verbose_name_plural = "Workshopdeltagere"
    seasonparticipant = models.ForeignKey(SeasonParticipant,on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop,on_delete=models.CASCADE)
    participant = models.ForeignKey(Participants,on_delete=models.CASCADE)
    added = models.DateField('Tilføjet',default=timezone.now)

    def __str__(self):
        return self.seasonparticipant.participant.name

    def seasonparticipant_name(self):
        return self.seasonparticipant.participant.name

class Attendance(models.Model):
    class Meta:
        verbose_name = "Fremmøde"
        verbose_name_plural = "Fremmøde"
    NOTICE = "NO"
    PRESENT = "PR"
    ABSENCE_CHOICES = (
        (NOTICE, 'Afbud'),
        (PRESENT, 'Til stede'),
    )
    participant = models.ForeignKey(Participants,on_delete=models.CASCADE)
    season = models.ForeignKey(Season,on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop,on_delete=models.CASCADE)
    registered_dtm = models.DateTimeField('Registreret',default=timezone.now)
    status = models.CharField('Fremmøde status',blank=False,null=False,max_length=2,choices=ABSENCE_CHOICES)

    def __str__(self):
        return self.participant.name

class ParticipantsFile(models.Model):
    class Meta:
        verbose_name = "Upload medlemsfil"
        verbose_name_plural = "Upload medlemsfiler"
    data = models.FileField()

    def save(self, *args, **kwargs):
        super(ParticipantsFile, self).save(*args, **kwargs)
        filename = self.data.url
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Participants.objects.get_or_create(
                    members_id=row[0],
                    name=row[1],
                    birthday=row[2],
                )

class Department(models.Model):
    class Meta:
        verbose_name = "Afdeling"
        verbose_name_plural = "Afdelinger"
    name=model.CharField("Navn",max_length=128)
