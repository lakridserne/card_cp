from django.utils import timezone
from card.models import Attendance, Cards, Department, Season, SeasonParticipant, Workshop
from rest_framework import serializers


class CheckInSerializer(serializers.HyperlinkedModelSerializer):
    streak_count = serializers.SerializerMethodField()

    def get_streak_count(self, obj):
        # figure out season and workshop
        seasonparticipants = SeasonParticipant.objects.filter(
            participant=obj.participant).filter(
            season__start_date__lte=timezone.now()).filter(
            season__end_date__gte=timezone.now()).filter(
            season__weekday=timezone.now().weekday())

        if not seasonparticipants:
            HttpResponseBadRequest("Der er ingen sæsoner. Kontakt kaptajnen")
        seasonparticipant = seasonparticipants[0]

        attendances = Attendance.objects.filter(
            season=seasonparticipant.season,
            participant=obj.participant,
        )
        for attendance in attendances:
            print(attendance.registered_at)
        return 1

    class Meta:
        model = Cards
        fields = ('card_number', 'streak_count')
        lookup_field = 'card_number'
        extra_kwargs = {
            'url': {'lookup_field': 'card_number'}
        }


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name') 
        model = Workshop


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name',)
        model = Department


class WorkshopOverviewSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only = True)
    workshops = WorkshopSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ('department', 'name', 'workshops')
        lookup_field = 'department_id'


class WorkshopAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = ('card_number',)
        lookup_field = 'card_number'
