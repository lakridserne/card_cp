from django.utils import timezone
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

        # find season participant participates in now - if any
        workshopparticipants = WorkshopParticipant.objects.filter(
            participant=participant).filter(
            seasonparticipant__season__start_date__lte=timezone.now()).filter(
            seasonparticipant__season__end_date__gte=timezone.now()).filter(
            seasonparticipant__season__weekday=timezone.now().weekday())

        """
        # first find the seasons currently ongoing
        seasons = Season.objects.filter(
                                        start_date__lte=timezone.now()).filter(
                                        end_date__gte=timezone.now()).filter(
                                        weekday=timezone.now().weekday())
        if not seasons.exists():
            raise NotFound({"message": "Noget gik galt - ingen sæsoner!"})
        elif len(seasons) != 1:
            raise NotFound({"message": "Flere sæsoner - du kan kun være\
                            tilmeldt 1!"})
        else:
            season = seasons[0]

        seasonparticipants = SeasonParticipant.objects.filter(
            season=season).filter(participant=participant)

        # get current workshop
        workshopparticipants = WorkshopParticipant.objects.filter(
            seasonparticipant=seasonparticipants,
            added__lte=timezone.now()).order_by('-id')
        workshopparticipant = workshopparticipants[0]

        # get attendance and see if person has checked in today
        attendance = Attendance.objects.filter(
            participant=participant, season=season,
            workshop=workshopparticipant.workshop,
            registered_dtm__date=timezone.now())

        if not attendance.exists():
            Attendance.objects.create(
                participant=participant,
                season=season,
                workshop=workshopparticipant.workshop,
                registered_dtm=timezone.now(),
                status="PR"
            )
        return self.queryset
        """
        print(workshopparticipants)
