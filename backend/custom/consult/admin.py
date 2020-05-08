from django.contrib import admin

#from custom.consult.models import Country
from custom.consult.models import Children
from custom.consult.models import Consultation
from custom.consult.models import MaritalStatus
from custom.consult.models import StatusChoice

# Register your models here.

#class CountryAdmin(admin.ModelAdmin):
#    fieldsets = ((None, {'fields': ['name',
#                                    'abbreviation',]}),)
#    list_display = ('id', 'name', 'abbreviation',)

#    class Meta:
#         verbose_name = 'Country'
#         verbose_name_plural = 'Countries'


class ChildrenAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['number',
                                    'value',
                                    'numeric',]}),)
    list_display = ('id', 'number', 'value', 'numeric')

    class Meta:
         verbose_name = 'Children'
         verbose_name_plural = 'Children'


class ConsultationAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['user',
                                    'status',
                                    'marital_status',
                                    'number_of_children',
                                    'invoice',
                                    'amount',
                                    'payment',
                                    'billing_full_name',
                                    'individual_email', 
                                    'individual_full_name', 
                                    'billing_phone', 
                                    'individual_phone', 
                                    'purpose', 
                                    'billing_address', 
                                    'country_of_citizenship', 
                                    'individual_address', 
                                    'use_billing', 
                                    'date_of_birth', 
                                    'time_responded',]}),)
    list_display = ('id', 'user', 'status', 'individual_full_name', 
                    'individual_email', 'individual_phone', 'time_responded', 
                    'amount', 'invoice',)
    class Meta:
         verbose_name = 'Consultation'
         verbose_name_plural = 'Consultations'
   

class MaritalStatusAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['status',
                                    'code',]}),)
    list_display = ('id', 'status', 'code',)

    class Meta:
         verbose_name = 'Country'
         verbose_name_plural = 'Countries'


class StatusChoiceAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['status',
                                    'code',]}),)
    list_display = ('id', 'status', 'code',)

    class Meta:
         verbose_name = 'Status Choice'
         verbose_name_plural = 'Status Choices'


#admin.site.register(Country, CountryAdmin)
admin.site.register(Children, ChildrenAdmin)
admin.site.register(Consultation, ConsultationAdmin)
admin.site.register(MaritalStatus, MaritalStatusAdmin)
admin.site.register(StatusChoice, StatusChoiceAdmin)

