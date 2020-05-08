from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from restless.views import Endpoint

from custom.users.models import Contact
from custom.users.models import StateProvince
from custom.utils.models import Logger
from custom.services.models import PackageType
from custom.services.models import Package
from custom.payments.models import CardType
from custom.payments.models import CreditCard
from custom.payments.models import Payment
from custom.payments.models import Address
from custom.payments.models import State
from custom.payments.models import CustomerPayment

from django.contrib.auth import logout
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from filters import AddressFilter
from signals import payment_send_confirmation_email
from callbacks import  payment_send_confirmation_email_handler
from serializers import PaymentSerializer
from serializers import AddressSerializer
from serializers import StateProvinceSerializer
from serializers import CardTypeSerializer
from utils import randomDigits
from utils import getPaymentProcessing
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def get_or_create_user(email):
    try:
        log = Logger(log='WILL TRY TO GET USER FOR {}'.format(email))
        log.save()

        user = User.objects.get(email=email)
        log = Logger(log='WE FOUND A USER FOR {}'.format(email))
        log.save()
        return user

    except Exception as e:
        log = Logger(log='WE FOUND NO USER FOR {} - {}'.format(email, e))
        log.save()
        return None


class AddressList(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'id', 'user_id', 'email')

    def get_queryset(self):
        """
        This view should return a list of all the messages
        that are outgoing for the given sender.
        """
        try:
            user_id = self.kwargs['user_id']
            user_id = int(user_id)

            return Address.objects.filter(user_id=user_id)

        except Exception, R:
            user_id = self.request.user.id

            return Address.objects.filter(user_id=user_id)


class CardTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CardTypeSerializer
    queryset = CardType.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'card', 'code',)

class AddressViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    filter_class = AddressFilter
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'user_id', 'name_or_company', 'city', 'nickname', 'state_province', 'country')


def reset_default_billing(address_id, user_id):
    try:
        addresses = Address.objects.filter(user_id=user_id).exclude(id=address_id)
        for address in addresses:
            address.is_default = False
            address.save()
    except Exception as e:
        log = Logger(log='SOMETHING BROKE {}'.format(e))
        log.save()

class PaymentMethodViewSet(viewsets.ModelViewSet):
   pass

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def add_payment_method_view(request):
    """
    A view to add payment method
    """
    pass

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def delete_payment_method_view(request):
    """
    A view to depete a payment method
    """
    pass


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def add_address_view(request):
    """
    A view to add a billing address
    """

    data = JSONParser().parse(request)
    user_id = data['user_id']
    address1 = data['address_1']
    address2 = data['address_2']
    address_id = data['address_id'] or None
    city = data['city']
    state_id = data['state']
    zip_or_postal = data['zip_or_postal']
    country = data['country']
    nickname = data['nickname']
    name_or_company = data['name_or_company']
    is_default = bool(data['make_default'])
    is_active = True

    if request.user.is_authenticated():
        user = request.user
    else:
        try:
            user = User.objects.get(id=int(user_id))
        except Exception as e:
            return Response({'result':'error'})

    try:
        state = StateProvince.objects.get(id=int(state_id))
    except Exception as e:
        return Response({'result':'error {}'.format(e)})

 
    try:
        address_id = int(address_id)
    except Exception as e:
        address_id = 0

    if address_id and address_id > 0:     
        try:  
            address = Address.objects.get(id=address_id)
	    address.address1 = address1
            address.name_or_company = name_or_company
	    address.user = user
            address.address2 = address2
            address.city = city
            address.state_province = state
	    address.country = country
            address.is_default = is_default
            address.is_active = is_active
            address.zip_or_postal = zip_or_postal
            address.save()
            reset_default_billing(address.id, user.id)
        except ObjectDoesNotExist:
            address = Address.objects.create(user=user,
                                             state_province=state,
                                             city=city,
                                             zip_or_postal=zip_or_postal,
                                             name_or_company=name_or_company,
                                             address1=address1,
                                             address2=address2,
                                             country=country,
                                             nickname=nickname,
                                             is_default=is_default,
                                             is_active=is_active)
           

    else:
        address = Address.objects.create(user=user,
				         state_province=state,
					 city=city,
                                         zip_or_postal=zip_or_postal,
                                         name_or_company=name_or_company,
			        	 address1=address1,
					 address2=address2,
					 country=country,
					 nickname=nickname,
					 is_default=is_default,
					 is_active=is_active)
    addresses = Address.objects.filter(user=user)
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)   
        

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def delete_address_view(request):
    """
    A view to delete a billing address
    """
    data = JSONParser().parse(request)
    address_id = data['address_id']
    user_id = data['user_id']

    if request.user.is_authenticated():
        user = request.user
    else:
        try:
            user = User.objects.get(id=int(user_id))
        except Exception as e:
            return Response({'result':'error'})

    try:
        address = Address.objects.get(id=int(address_id))
        address.delete()
    except Exception as e:
        pass

    addresses = Address.objects.filter(user=user) 
    log = Logger(log='TOTAL ADDRESSES {}'.format(len(addresses)))
    log.save()
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)
    

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def read_addresses_view(request):
    """
    A view to delete a billing address
    """

    if request.user.is_authenticated():
        user = request.user
    else:
        try:
            user_id = request.data['user_id']
            user = User.objects.get(id=int(user_id))
        except Exception as e:
            log = Logger(log='Could not read user {}'.format(e))
            log.save()
            return Response({'result':'error'})

    addresses = Address.objects.filter(user=user)
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)



class PaymentsList(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, )

    def get_queryset(self):
        """
        This view should return a list of all the messages
        that are outgoing for the given sender.
        """
        try:
            user_id = self.kwargs['user_id']
            user_id = int(user_id)

            return Payment.objects.filter(user_id=user_id)

        except Exception, R:
            user_id = self.request.user.id

            return Payment.objects.filter(user_id=user_id)


class PastPaymentsList(Endpoint):
    @csrf_exempt
    def post(self, request):
        try:
            user_id = request.user.id
            payments = Payment.objects.filter(user_id=user_id)

            for payment in payments:
               if payment.payment_processing_number==None:
                  payment.payment_processing_number = getPaymentProcessing()
                  payment.save()

            serializer = PaymentSerializer(payments,many=True)      
            return {"payments":serializer.data}      
        except Exception, R:
            return {"payments":str(R)}


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def send_confirmation_view(request):
    try:
        contact = None
        full_name = request.data.get("fullname", '')
        email = request.data['email']
        city = request.data['city']
        token = request.data.get("token", None)
        amount = request.data.get("amount", 0)
        package_price = request.data.get('amount', '')
        address1 = request.data.get("address1", "")
        address2 = request.data.get("address2", "")
        phone = request.data['phone']
        state_id = request.data['state']
        zipcode = request.data['zip']
        package_type = request.data.get('package_type', "General Payment")

        log = Logger(log="AMOUNT {} TOKEN {} EMAIL {}".format(amount, token, email))
        log.save()

        try:
            state = StateProvince.objects.get(id=int(state_id))
        except Exception as e:
            state = StateProvince.objects.get(name=state_id)

        try:
            contact = Contact.objects.get(email=email)
        except Exception as e:
            contact = Contact.objects.create(name=full_name, email=email)

    except Exception as e:
        log = Logger(log="Something went -  wrong {}".format(e))
        log.save()
        return Response({'message':'card processing error {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


    try:
        
        charge  = stripe.Charge.create(
                        amount      = 100*int(amount),
                        currency    = "usd",
                        source      = token,
                        description = "Customer payment"
        )

    except Exception as e:
        log = Logger(log="Something went --  wrong {}".format(e))
        log.save()
        return Response({'message':'card processing error {}'.format(e)},  status=status.HTTP_400_BAD_REQUEST)


    if request.user.is_authenticated():
        user = request.user
    else:
        user = get_or_create_user(email)

    if not user:
        return Response({'message':'card processing error - no user found'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        payment_id = CustomerPayment.objects.latest('id').id + 1
        customer_payment = CustomerPayment.objects.create(user=user,
                                                          charge=str(charge.id),
                                                          amount=float(package_price),
                                                          invoice="GS-{}-{}".format(datetime.now().strftime('%Y-%m-%d'), payment_id),
                                                          is_successful=True)

    except Exception as e:
        log = Logger(log="Something went ---  wrong {}".format(e))
        log.save()
        return Response({'message':'card processing error {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        payment = Payment.objects.create(payment=customer_payment, 
                                         fullname=full_name, 
                                         email=email,
                                         first_name=full_name.split(" ")[0],
                                         last_name=full_name.split(" ")[1],
                                         address1=address1,
                                         address2=address2,
                                         city=city,
                                         phone=phone,
                                         state=state.name,
                                         zipcode=zipcode,
                                         package_type=package_type,                             
                                         package_price=package_price,
                                         message="Customer Payment")
        payment_send_confirmation_email.send(sender=User, contact=contact, payment=payment)
        return Response({'message':'success'}, status=status.HTTP_200_OK) 
    except Exception as e:
        log = Logger(log="Something went ----  wrong {}".format(e))
        log.save()
        return Response({'message':'card processing error {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def save_payment_method_view(request):
    return Response({'message': 'failure', 'cause': ""})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def read_payment_methods_view(request):
    return Response({'message': 'failure', 'cause': ""})




payment_send_confirmation_email.connect(payment_send_confirmation_email_handler)
