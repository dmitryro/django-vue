from django.contrib import admin

# Register your models here.
from models import CreditCard
from models import CardType
from models import Transaction
from models import TransactionType
from models import TransactionStatus
from models import Address
from models import State
from models import PaymentStatus
from models import MerchantActivity
from models import MerchantActivityStats
from models import CustomerActivityStats
from models import CustomerProfile
from models import CustomerPayment

class CustomerPaymentAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['user',
                                    'amount',
                                    'is_successful',]}),)

    list_display = ('id', 'user', 'amount', 'is_successful',)

    class Meta:
         verbose_name = 'Customer Payment'
         verbose_name_plural = 'Customer Payments'


class AddressAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['user',
                                    'nickname',
                                    'address1',
                                    'address2',
                                    'city',
                                    'name_or_company',
                                    'state_province',
                                    'zip_or_postal',
                                    'country',
                                    'is_default',
                                    'is_active',]}),)
    list_display = ('id','nickname','user','address1', 'city', 'is_default','name_or_company',)
    class Meta:
         verbose_name = 'Billing Address'
         verbose_name_plural = 'Billing Addresses'
    
class CustomerProfileAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['customer_id',
                                    'token',
                                    'address',
                                    'first_name',
                                    'last_name',
                                    'email',
                                    'phone',
                                    'customer_cards',
                                    'profile',
                                    'transactions',
                                    'orders',
                                    'stats',]}),)
    list_display = ('id', 'token', 'address', 'first_name', 'last_name', 'email', 'profile',)

    class Meta:
         verbose_name = 'Customer Profile'
         verbose_name_plural = 'Customer Profiles'

class CardTypeAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['card',
                                    'code',]}),)

    class Meta:
         verbose_name = 'Card Type'
         verbose_name_plural = 'Card Types'

class CreditCardAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['is_defailt', 
                                    'first_name', 
                                    'last_name',
                                    'token', 
                                    'card_cvv', 
                                    'card_name', 
                                    'last_4', 
                                    'card_type', 
                                    'owner',]}),)

    class Meta:
         verbose_name = 'Credit Card'
         verbose_name_plural = 'Credit Cards'

admin.site.register(CustomerPayment, CustomerPaymentAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(CardType, CardTypeAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(Address, AddressAdmin)
