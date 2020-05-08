from rest_framework import serializers
from rest_framework import generics

from models import Service
from models import Package
from models import PackageType
from models import PackageNote
from custom.gui.serializers import StateSerializer

class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ('id', 'package_type', 'code',)


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ('id','title','fees','price','is_available','avatar')

class PackageNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageNote
        fields = ('id', 'note',)


class PackageSerializer(serializers.ModelSerializer):

    services = ServiceSerializer(many=True, read_only=True)
    state = StateSerializer(many=False, read_only=True)
    package_type = PackageTypeSerializer(many=False, read_only=True)
    notes = PackageNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ('id', 'title', 'fees', 'price', 
                  'is_available', 'services', 'state',
                  'package_type', 'description', 'notes')



