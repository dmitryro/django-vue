from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import generics

#from custom.consult.models import Country
from custom.consult.models import Children
from custom.consult.models import Consultation
from custom.consult.models import MaritalStatus
from custom.consult.models import StatusChoice
from custom.payments.serializers import CustomerPaymentSerializer

#class CountrySerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Country
#        fields = ('id','name','abbreviation')


class ChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Children
        fields = ('id', 'number', 'value', 'numeric',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name')


class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = ('id','status','code')


class StatusChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusChoice
        fields = ('id','status','code')

class ConsultationSerializer(serializers.ModelSerializer):
    payment = CustomerPaymentSerializer(many=False)
    user = UserSerializer(many=False)
    
    class Meta:
        model = Consultation
        fields = ('id','payment','amount', 'user',
                  'status',
                  'marital_status', 'number_of_children',
                  'invoice', 'individual_full_name', 'billing_full_name',
                  'billing_phone', 'individual_email', 'individual_phone',
                  'purpose', 'billing_address',
                  'country_of_citizenship', 'individual_address',
                  'use_billing', 'date_of_birth', 'time_responded',)
