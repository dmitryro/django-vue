from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import generics

from models import Payment
from models import State
from models import Address
from models import PaymentStatus
from models import MerchantActivity
from models import MerchantActivityStats
from models import CustomerActivityStats
from models import CardType
from models import CreditCard
from models import TransactionStatus
from models import TransactionType
from models import Transaction
from models import CustomerProfile
from custom.payments.models import CustomerPayment
from custom.users.models import StateProvince


class CardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardType
        fields = ('id','card','code')


class StateProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateProvince
        fields = ('id','name','abbreviation')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name')

class AddressSerializer(serializers.ModelSerializer):
    state_province = StateProvinceSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Address
        fields = ('id', 'name_or_company', 'address1',
                  'address2', 'city', 'state_province', 'country',
                  'zip_or_postal', 'user', 'is_default',
                  'is_active', 'nickname',)

class CustomerPaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = CustomerPayment
        fields = ('id', 'user', 'amount', 'is_successful',)


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ('id',)        

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ('id','type','code',)

class TransactionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionStatus
        fields = ('id','status','code',)


class TransactionSerializer(serializers.ModelSerializer):
    type = TransactionTypeSerializer(many=False, read_only=True)
    status = TransactionStatusSerializer(many=False, read_only=True)

    class Meta:
        model = Transaction
        fields = ('id','transaction_id','type','payment_method_used',
                  'payment_method_used','card_unique_identifier','total_amount',
                  'shipping_amount','commission_amount','taxes_amount',
                  'take_home_amount','status','merchant_id','customer_id',
                  'is_in_escrow','is_refunded','is_rejected','order_number',
                  'time_processed') 

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    transaction = TransactionSerializer(many=False, read_only=True)

    class Meta:
        model = Payment
        fields = ('id','email','first_name','last_name','fullname',
                  'address1','address2','city','state','cardtype',
                  'cardtype','cardnumber','month','year','zipcode',
                  'payment_processing_number',
                  'phone','message','user','transaction')

