from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from serializers import PackageTypeSerializer
from serializers import PackageSerializer
from serializers import ServiceSerializer
from models import Package
from models import Service
from models import PackageType
from filters import PackageFilter

class PackageTypeViewSet(viewsets.ModelViewSet):
    serializer_class = PackageTypeSerializer
    queryset = PackageType.objects.all()


class PackageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing packages.
    """
    serializer_class = PackageSerializer
    queryset = Package.objects.all().order_by('price')
    filter_class = PackageFilter
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'title', 'fees', 'price', 'is_available', 'description', 'state', 'package_type', 'notes',)



class ServiceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing packages.
    """
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class ServiceList(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, )

    def get_queryset(self):
        """
        This view should return a list of all the services
        """
        try:
            return Service.objects.all()

        except Exception, R:

            return Service.objects.all()


class PackageList(generics.ListAPIView):
    serializer_class = PackageSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, )

    def get_queryset(self):
        """
        This view should return a list of all the services
        """
        try:
            return Package.objects.all()

        except Exception, R:

            return Package.objects.all()

