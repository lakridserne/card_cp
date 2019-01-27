from django.utils import timezone
from django.http import HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from card.models import Cards, Participants, Attendance, Season, \
                        SeasonParticipant, WorkshopParticipant
from card.serializers import CheckInSerializer


# Create your views here.
class CheckInView(viewsets.ReadOnlyModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CheckInSerializer
    lookup_field = 'card_number'

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
        else:
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
            registered_dtm__date=timezone.now())

        if not attendance.exists():
            Attendance.objects.create(
                participant=participant,
                season=seasonparticipant.season,
                workshop=workshopparticipant.workshop,
                registered_dtm=timezone.now(),
                status="PR"
            )
        return self.queryset
