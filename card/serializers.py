from card.models import Cards, Department, Season, Workshop
from rest_framework import serializers


class CheckInSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cards
        fields = ('card_number',)
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
