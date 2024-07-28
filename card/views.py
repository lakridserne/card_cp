from django.utils import timezone
from django.http import HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from card.models import Cards, Participants, Attendance, Season, \
                        SeasonParticipant, Workshop, WorkshopParticipant, Department
from card.serializers import CheckInSerializer, WorkshopOverviewSerializer, WorkshopAddSerializer

import datetime

# Create your views here.
class CheckInView(viewsets.ReadOnlyModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CheckInSerializer
    lookup_field = 'participant__cards__card_number'

    def get_queryset(self):
        card_number = self.request.path.split('/')[2]
        participant = Participants.objects.get(cards__card_number=card_number)

        # figure out season and workshop
        seasonparticipants = SeasonParticipant.objects.filter(
            participant=participant).filter(
            season__start_date__lte=timezone.now()).filter(
            season__end_date__gte=timezone.now()).filter(
            season__weekday=timezone.now().weekday())

        if not seasonparticipants:
            HttpResponseBadRequest("Der er ingen sæsoner. Kontakt kaptajnen")
        seasonparticipant = seasonparticipants[0]

        # get current workshop
        workshopparticipants = WorkshopParticipant.objects.filter(
            seasonparticipant=seasonparticipant,
            added__lte=timezone.now()).order_by('-id')
        workshopparticipant = workshopparticipants[0]

        # get attendance and see if person has checked in today
        attendance = Attendance.objects.filter(
            participant=participant, season=seasonparticipant.season,
            workshop=workshopparticipant.workshop,
            registered_at__date=timezone.now())

        if not attendance.exists():
            Attendance.objects.create(
                participant=participant,
                season=seasonparticipant.season,
                workshop=workshopparticipant.workshop,
                registered_at=timezone.now(),
                status="PR"
            )

        return self.queryset


class WorkshopAddView(viewsets.ReadOnlyModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = WorkshopAddSerializer
    lookup_field = 'card_number'
    
    def get_queryset(self):
        card_number = self.kwargs['card_number']
        workshop_id = self.kwargs['workshop_id']
        participant = Participants.objects.get(cards__card_number=card_number)
        workshop = Workshop.objects.get(pk=workshop_id)

        # figure out season and workshop
        seasonparticipants = SeasonParticipant.objects.filter(
            participant=participant).filter(
            season__start_date__lte=timezone.now()).filter(
            season__end_date__gte=timezone.now()).filter(
            season__weekday=timezone.now().weekday())

        if not seasonparticipants:
            HttpResponseBadRequest("Der er ingen sæsoner. Kontakt kaptajnen")
        seasonparticipant = seasonparticipants[0]

        # get current workshop
        workshopparticipants = WorkshopParticipant.objects.filter(
            seasonparticipant=seasonparticipant,
            workshop=workshop,
            added__lte=timezone.now()).order_by('-id')
        

        if not workshopparticipants and workshop.season == seasonparticipant.season:
            WorkshopParticipant.objects.create(
                seasonparticipant=seasonparticipant,
                workshop=workshop,
                participant=participant,
                added=datetime.datetime.now(),
            )

        return self.queryset


class WorkshopOverviewView(viewsets.ReadOnlyModelViewSet):
    queryset = Season.objects.filter(
        start_date__lte=timezone.now()).filter(
        end_date__gte=timezone.now()).filter(
        weekday=timezone.now().weekday()
    )
    serializer_class = WorkshopOverviewSerializer
    lookup_field = 'department_id'

    def get_queryset(self):
        return self.queryset
