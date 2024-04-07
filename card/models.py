from django.db import models
from django.utils import timezone
import csv


class Participants(models.Model):
    class Meta:
        verbose_name = "Deltager"
        verbose_name_plural = "Deltagere"
    name = models.CharField('Navn', max_length=200)

    def __str__(self):
        return self.name


class Union(models.Model):
    class Meta:
        verbose_name = "Forening"
        verbose_name_plural = "Foreninger"
    name = models.CharField("Navn", max_length=128)

    def __str__(self):
        return self.name


class Department(models.Model):
    class Meta:
        verbose_name = "Afdeling"
        verbose_name_plural = "Afdelinger"
    name = models.CharField("Navn", max_length=128)
    union = models.ForeignKey(Union, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cards(models.Model):
    class Meta:
        verbose_name = "Kort"
        verbose_name_plural = "Kort"
    participant = models.ForeignKey(Participants, on_delete=models.CASCADE)
    card_number = models.CharField('Kortnummer', max_length=10, unique=True,
                                   blank=True, null=True)
    activated = models.DateTimeField('Aktiveret', blank=False, null=False,
                                     default=timezone.now)
    deactivated = models.DateTimeField('Deaktiveret', blank=True, null=True)


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
    name = models.CharField('Navn', max_length=200)
    start_date = models.DateField('Startdato', blank=False, null=False)
    end_date = models.DateField('Slutdato', blank=False, null=False)
    weekday = models.CharField('Ugedag', blank=False, null=False, max_length=2,
                               choices=DAYS_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ", " + self.department.name


class SeasonParticipant(models.Model):
    class Meta:
        verbose_name = "Sæsondeltager"
        verbose_name_plural = "Sæsondeltagere"
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participants, on_delete=models.CASCADE)
    added = models.DateTimeField('Tilføjet', default=timezone.now)
    stopped = models.DateTimeField('Stoppet', blank=True, null=True)

    def __str__(self):
        return self.participant.name + ", " + self.season.name


class Workshop(models.Model):
    class Meta:
        verbose_name = "Workshop"
        verbose_name_plural = "Workshops"
    name = models.CharField('Navn', max_length=200)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='workshops')

    def __str__(self):
        return (self.name +
                ", " + self.season.name +
                ", " + self.season.department.name)


class WorkshopParticipant(models.Model):
    class Meta:
        verbose_name = "Workshopdeltager"
        verbose_name_plural = "Workshopdeltagere"
    seasonparticipant = models.ForeignKey(SeasonParticipant,
                                          on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participants, on_delete=models.CASCADE)
    added = models.DateField('Tilføjet', default=timezone.now)

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
    participant = models.ForeignKey(Participants, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    registered_dtm = models.DateTimeField('Registreret', default=timezone.now)
    status = models.CharField('Fremmøde status', max_length=2, choices=ABSENCE_CHOICES)
    registered_automatically = models.BooleanField('Registreret automatisk', default=True)

    def __str__(self):
        return self.participant.name


class WiFiPasswords(models.Model):
    class Meta:
        verbose_name = "WiFi Kode"
        verbose_name_plural = "WiFi Koder"
    ssid = models.CharField("SSID", max_length=32)
    wifi_password = models.CharField("WiFi Password", max_length=128, null=True, blank=True)
    username = models.CharField("Brugernavn", max_length=128, blank=True, null=True)
    password = models.CharField("Kode", max_length=128, blank=True, null=True)
    seasonparticipant = models.ForeignKey("SeasonParticipant", on_delete=models.CASCADE, blank=True, null=True)
    season = models.ForeignKey("Season", on_delete=models.CASCADE, blank=True, null=True)
    start_dtm = models.DateTimeField("Start", default=timezone.now)
    end_dtm = models.DateTimeField("Slut", blank=True, null=True)
    active = models.BooleanField("Aktiv", default=True)


class WiFiFile(models.Model):
    class Meta:
        verbose_name = "Upload WiFi kode"
        verbose_name_plural = "Upload WiFi koder"
    ssid = models.CharField("SSID", max_length=32)
    wifi_password = models.CharField("WiFi Password", max_length=128, null=True, blank=True)
    data = models.FileField()
    season = models.ForeignKey("Season", on_delete=models.CASCADE)
    help_text = "Skal koderne være til sæsonen? Alternativet er at de bruges til hver deltager på sæsonen (tilfældig kode til hver indtil der ikke er flere tilbage på den dato)."
    for_season = models.BooleanField("Koder til sæsonen?", help_text=help_text, default=False)

    def save(self, *args, **kwargs):
        super(WiFiFile, self).save(*args, **kwargs)
        filename = self.data.url
        season_participants = SeasonParticipant.objects.filter(season=self.season)
        i = 0
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if self.for_season:
                    _, created = WiFiPasswords.objects.get_or_create(
                        ssid = self.ssid,
                        wifi_password = self.wifi_password,
                        username = row[0],
                        password = row[1],
                        start_dtm = row[2],
                        end_dtm = row[3],
                        season = self.season,
                    )
                else:
                    _, created = WiFiPasswords.objects.get_or_create(
                        ssid = self.ssid,
                        wifi_password = self.wifi_password,
                        username = row[0],
                        password = row[1],
                        start_dtm = row[2],
                        end_dtm = row[3],
                        seasonparticipant = season_participants[i]
                    )
                    i += 1
        self.delete()


class ParticipantsFile(models.Model):
    class Meta:
        verbose_name = "Upload medlemsfil"
        verbose_name_plural = "Upload medlemsfiler"
    data = models.FileField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(ParticipantsFile, self).save(*args, **kwargs)
        filename = self.data.path
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter = ';')
            next(reader)
            for row in reader:
                _, created = Participants.objects.get_or_create(
                    name=row[0],
                )
                
                # Add to season
                season_participant = SeasonParticipant.objects.get_or_create(
                    season = self.season,
                    participant = _,
                )
        self.delete()


class ClosingDays(models.Model):
    class Meta:
        verbose_name = "Lukkedag"
        verbose_name_plural = "Lukkedage"
    name = models.CharField("Navn", max_length=128)
    date = models.DateField("Dato")


class Awards(models.Model):
    class Meta:
        verbose_name = "Præmie"
        verbose_name_plural = "Præmier"
    BASIC="BC"
    MEDIUM="MM"
    SEASON="SN"
    AWARD_TYPES = (
        (BASIC, 'Basalt'),
        (MEDIUM, 'Medium'),
        (SEASON, 'Sæson'),
    )
    award_type = models.CharField("Præmietype", blank=False, null=False, max_length=2, choices=AWARD_TYPES)
    start_date = models.DateField("Startdato", blank=False, null=False)
    end_date = models.DateField("Slutdato", blank=False, null=False)
    delivered = models.DateField("Leveret", blank=False, null=False)
