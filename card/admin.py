from django import forms
from django.contrib import admin
from django.db import models, transaction
from django.utils import timezone
from django.shortcuts import render
from django.conf.urls import include, url
from card.models import (Participants, Cards, Season, SeasonParticipant,
                         ParticipantsFile, Workshop, WorkshopParticipant,
                         Attendance, Department, Union)
from django.contrib import messages
from daterange_filter.filter import DateRangeFilter

admin.site.site_header = "Coding Pirates Check-in system"
admin.site.index_title = "Check-in Coding Pirates"


class CardNumberInline(admin.TabularInline):
    model = Cards
    extra = 1


class SeasonInline(admin.TabularInline):
    model = SeasonParticipant
    extra = 0


class WorkshopInline(admin.TabularInline):
    model = WorkshopParticipant
    extra = 0


class ParticipantDepartmentListFilter(admin.SimpleListFilter):
    title = ('Afdeling')
    parameter_name = 'dept'

    def lookups(self, request, model_admin):
        departments = Department.objects.all()
        department_list = [('any', 'Alle i en afdeling'),
                           ('none', 'Ikke i en afdeling')]
        for department in departments:
            department_list.append((str(department.pk), str(department)))
        return department_list

    def queryset(self, request, queryset):
        if self.value() == 'any':
            return queryset.exclude(
                seasonparticipant__season__department__isnull=True)
        elif self.value() == 'none':
            return queryset.filter(
                seasonparticipant__season__department__isnull=True)
        elif self.value() is None:
            return queryset
        else:
            return queryset.filter(
                seasonparticipant__season__department=self.value())


class SeasonListFilter(admin.SimpleListFilter):
    title = ('Sæson')
    parameter_name = 'season'

    def lookups(self, request, model_admin):
        seasons = Season.objects.all()
        season_list = [('any', 'Alle deltagere samlet'),
                       ('none', 'Deltager ikke i en sæson')]
        for season in seasons:
            season_list.append((str(season.pk), str(season)))
        return season_list

    def queryset(self, request, queryset):
        if self.value() == 'any':
            return queryset.exclude(seasonparticipant__isnull=True)
        elif self.value() == 'none':
            return queryset.filter(seasonparticipant__isnull=True)
        elif self.value() is None:
            return queryset
        else:
            return queryset.filter(seasonparticipant__season=self.value())


class WorkshopListFilter(admin.SimpleListFilter):
    title = ('Workshop')
    parameter_name = 'workshop'

    def lookups(self, request, model_admin):
        workshops = Workshop.objects.all()
        workshop_list = [('any','Alle deltagere samlet'), ('none','Deltager ikke i en workshop')]
        for workshop in workshops:
            workshop_list.append((str(workshop.pk), str(workshop)))
        return workshop_list

    def queryset(self, request, queryset):
        if self.value() == 'any':
            return queryset.exclude(workshopparticipant__isnull=True)
        elif self.value() == 'none':
            return queryset.filter(workshopparticipant__isnull=True)
        elif self.value() is None:
            return queryset
        else:
            return queryset.filter(workshopparticipant__workshop=self.value())


class CardListFilter(admin.SimpleListFilter):
    title = ('Kort')
    parameter_name = 'card'

    def lookups(self, request, model_admin):
        card_list = [('any', 'Alle med kort'), ('none', 'Alle uden kort')]
        return card_list

    def queryset(self, request, queryset):
        if self.value() == 'any':
            return queryset.exclude(cards__isnull=True)
        elif self.value() == 'none':
            return queryset.filter(cards__isnull=True)
        elif self.value() is None:
            return queryset


class ParticipantAdmin(admin.ModelAdmin):
    model = Participants
    list_display = ('name', 'age_years')
    list_filter = (ParticipantDepartmentListFilter, SeasonListFilter,
                   WorkshopListFilter, CardListFilter)
    search_fields = ('name', 'cards__card_number')
    actions = ['add_to_season', 'add_to_workshop', 'register_attendance_multi']
    inlines = (CardNumberInline, SeasonInline, WorkshopInline)

    def add_to_season(self, request, queryset):
        # get list of seasons
        seasons = Season.objects.all()
        season_list = [('-', '-')]
        for season in seasons:
            season_list.append((season.id, season.name + ", " +
                                season.department.name))

        class MassAdd(forms.Form):
            season = forms.ChoiceField(label='Sæson', choices=season_list)
        # get selected persons
        persons = queryset

        context = admin.site.each_context(request)
        context['persons'] = persons
        context['queryset'] = queryset

        if request.method == 'POST':
            mass_add_season_form = MassAdd(request.POST)
            context['mass_add_season_form'] = mass_add_season_form

            if (mass_add_season_form.is_valid() and
               mass_add_season_form.cleaned_data['season'] != '-'):
                season = Season.objects.get(
                    pk=mass_add_season_form.cleaned_data['season'])

                # make sure person is not already added
                added_counter = 0
                already_added = Participants.objects.filter(
                    seasonparticipant__season=mass_add_season_form.cleaned_data
                    ['season'],
                    seasonparticipant__participant__in=queryset).all()
                list(already_added)
                already_added_ids = already_added.values_list('id', flat=True)

                try:
                    with transaction.atomic():
                        for current_participant in queryset:
                            if (current_participant.id
                               not in already_added_ids):
                                added_counter += 1
                                add_participant = SeasonParticipant(
                                    season=season,
                                    participant=current_participant)
                                add_participant.save()
                except Exception as e:
                    messages.error(request, "Fejl - ingen personer blev tilføjet til sæsonen. Der var problemer med " + add_participant.participant.name + ".")
                    return

                # return ok message
                already_added_text = ""
                if(already_added.count()):
                    already_added_text = ". Dog var : " + str.join(', ', already_added.values_list('name', flat=True)) + " allerede tilføjet!"
                messages.success(request, str(added_counter) + " af " + str(queryset.count()) + " valgte personer blev tilføjet til " + str(season) + already_added_text)
                return
            else:
                messages.error(request, 'Du skal vælge en sæson')
        else:
            context['mass_add_season_form'] = MassAdd()

        return render(request, 'admin/mass_add_season.html', context)
    add_to_season.short_description = "Tilføj til sæson"

    def add_to_workshop(self, request, queryset):
        # get list of workshops
        workshops = Workshop.objects.all()
        workshop_list = [('-', '-')]
        for workshop in workshops:
            workshop_list.append((workshop.id, workshop.name + ", " +
                                  workshop.season.name + ", " +
                                  workshop.season.department.name))

        class MassAdd(forms.Form):
            workshop = forms.ChoiceField(label='Workshop', choices=workshop_list)
        # get selected persons
        persons = queryset

        context = admin.site.each_context(request)
        context['persons'] = persons
        context['queryset'] = queryset

        if request.method == 'POST':
            mass_add_workshop_form = MassAdd(request.POST)
            context['mass_add_workshop_form'] = mass_add_workshop_form

            if mass_add_workshop_form.is_valid() and mass_add_workshop_form.cleaned_data['workshop'] != '-':
                workshop = Workshop.objects.get(pk=mass_add_workshop_form.cleaned_data['workshop'])

                # make sure person is not already added
                added_counter = 0
                already_added = Participants.objects.filter(workshopparticipant__workshop=mass_add_workshop_form.cleaned_data['workshop'], workshopparticipant__participant__in=queryset).all()
                list(already_added)
                already_added_ids = already_added.values_list('id', flat=True)

                try:
                    with transaction.atomic():
                        for current_participant in queryset:
                            if (current_participant.id not in already_added_ids):
                                added_counter += 1
                                seasonparticipant = SeasonParticipant.objects.get(participant__pk=current_participant.id)
                                add_participant = WorkshopParticipant(seasonparticipant=seasonparticipant,workshop=workshop,participant=current_participant)
                                add_participant.save()
                except Exception as e:
                    messages.error(request,"Fejl - ingen personer blev tilføjet til workshoppen. Der var problemer med " + add_participant.participant.name + ".")
                    return

                #return ok message
                already_added_text=""
                if(already_added.count()):
                    already_added_text = ". Dog var : " + str.join(', ', already_added.values_list('name', flat=True)) + " allerede tilføjet!"
                messages.success(request, str(added_counter) + " af " + str(queryset.count()) + " valgte personer blev tilføjet til " + str(workshop) + already_added_text)
                return
            else:
                messages.error(request, 'Du skal vælge en workshop')
        else:
            context['mass_add_workshop_form'] = MassAdd()

        return render(request, 'admin/mass_add_workshop.html', context)
    add_to_workshop.short_description = "Tilføj til workshop"

    def register_attendance_multi(self, request, queryset):
        # make list of possibilities
        status_list = [('-','-'),('PR','Fremmødt'),('NO','Afbud')]
        class MassAdd(forms.Form):
            status = forms.ChoiceField(label='Status', choices=status_list)
        # get selected persons
        persons = queryset

        context = admin.site.each_context(request)
        context['persons'] = persons
        context['queryset'] = queryset

        if request.method == 'POST':
            register_attendance_multi_form = MassAdd(request.POST)
            context['register_attendance_multi_form'] = register_attendance_multi_form

            if register_attendance_multi_form.is_valid() and register_attendance_multi_form.cleaned_data['status'] != '-':

                # make sure person is not already added
                added_counter = 0
                already_added = Attendance.objects.filter(participant__in=queryset,registered_dtm__date=timezone.now()).all()
                list(already_added)
                already_added_ids = already_added.values_list('participant__id', flat=True)

                try:
                    with transaction.atomic():
                        for current_participant in queryset:
                            if (current_participant.id not in already_added_ids):
                                added_counter += 1
                                seasonparticipant = SeasonParticipant.objects.get(participant__pk=current_participant.id,season__start_date__lte=timezone.now(),season__end_date__gte=timezone.now()) # we need to make this unique... Add date
                                season = Season.objects.get(pk=seasonparticipant.season.id)
                                workshopparticipant = WorkshopParticipant.objects.get(seasonparticipant__pk=seasonparticipant.id,added__lte=timezone.now())
                                workshop = Workshop.objects.get(pk=workshopparticipant.workshop.id)
                                registered_dtm = timezone.now()
                                status = register_attendance_multi_form.cleaned_data['status']
                                add_attendance = Attendance(participant=current_participant,season=season,workshop=workshop,registered_dtm=registered_dtm,status=status)
                                add_attendance.save()
                except Exception as e:
                    messages.error(request,"Fejl - ingen personer fik registreret fremmøde. Der var problemer med " + add_attendance.participant.name + ".")
                    return

                #return ok message
                already_added_text=""
                if(already_added.count()):
                    already_added_text = ". Dog var: " + str.join(', ', already_added.values_list('participant__name', flat=True)) + " allerede registreret i dag!"
                messages.success(request, str(added_counter) + " af " + str(queryset.count()) + " valgte personer fik registreret fremmøde." + already_added_text)
                return
            else:
                messages.error(request, 'Du skal vælge en status')
        else:
            context['register_attendance_multi_form'] = MassAdd()

        return render(request, 'admin/register_attendance_multi.html', context)
    register_attendance_multi.short_description = "Registrer fremmøde"
admin.site.register(Participants, ParticipantAdmin)

class SeasonAdmin(admin.ModelAdmin):
    model = Season
    list_display = ('name','start_date','end_date','weekday')
admin.site.register(Season, SeasonAdmin)

class WorkshopParticipantAdmin(admin.ModelAdmin):
    model = WorkshopParticipant
    list_display = ('seasonparticipant_name','workshop')
admin.site.register(WorkshopParticipant,WorkshopParticipantAdmin)


class AttendanceDepartmentListFilter(admin.SimpleListFilter):
    title = ('afdeling')
    parameter_name = 'dept'

    def lookups(self, request, model_admin):
        departments = Department.objects.all()
        department_list = [('any', 'Alle i en afdeling'),
                           ('none', 'Ikke i en afdeling')]
        for department in departments:
            department_list.append((str(department.pk), str(department)))
        return department_list

    def queryset(self, request, queryset):
        if self.value() == 'any':
            return queryset.exclude(
                season__department__isnull=True)
        elif self.value() == 'none':
            return queryset.filter(
                season__department__isnull=True)
        elif self.value() is None:
            return queryset
        else:
            return queryset.filter(
                season__department=self.value())


class AttendanceAdmin(admin.ModelAdmin):
    date_hierachy = 'registered_dtm'
    list_filter = (AttendanceDepartmentListFilter, ('registered_dtm',
                   DateRangeFilter))
    list_display = ('participant', 'season', 'workshop', 'registered_dtm',
                    'status')
    model = Attendance


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(SeasonParticipant)
admin.site.register(ParticipantsFile)
admin.site.register(Workshop)
admin.site.register(Department)
admin.site.register(Union)
