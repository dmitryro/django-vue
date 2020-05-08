from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from custom.users.models import Profile
from custom.users.models import StateProvince
from taggit.managers import TaggableManager

class CustomerPayment(models.Model):
    time_posted = models.DateTimeField(default=datetime.now, blank=True)
    amount = models.FloatField(default=0.0, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    is_successful = models.NullBooleanField(default=True, blank=True, null=True)
    charge = models.CharField(max_length=250, blank=True, null=True)
    invoice = models.CharField(max_length=250, blank=True, null=True) 

    class Meta:
        verbose_name = 'Customer Payment'
        verbose_name_plural = 'Customer Payments'


class State(models.Model):
    name = models.CharField(max_length=150,blank=True,null=True)
    abbreviation = models.CharField(max_length=150,blank=True,null=True)


class Address(models.Model):
    time_published = models.DateTimeField(default=datetime.now, blank=True)
    nickname = models.CharField(max_length=150, blank=True, null=True)
    name_or_company = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    address1 = models.CharField(max_length=150, blank=True, null=True)
    address2 = models.CharField(max_length=150, blank=True, null=True)
    city  = models.CharField(max_length=150, blank=True, null=True)
    state_province = models.ForeignKey(StateProvince, related_name='state_province', blank=True, null=True)
    zip_or_postal = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    is_default = models.NullBooleanField(default=False, blank=True, null=True)  
    is_active = models.NullBooleanField(default=True,blank=True,null=True)  
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return str(self.nickname)

    def __unicode__(self):
        return unicode(str(self.nickname))

    def get_absolute_url(self):
        return "/comments/%s/" % self.nickname

class PaymentStatus(models.Model):
    """ Payment Status  Approved, Declined, on hold"""
    status = models.CharField(max_length=200,blank=True,null=True)
    code = models.CharField(max_length=200,blank=True,null=True)
    description = models.CharField(max_length=400,blank=False,null=False)

    class Meta:
        verbose_name = 'Payment Status'
        verbose_name_plural = 'Payment Statuses'

class MerchantActivity(models.Model):
    amount = models.FloatField(default=0.0,blank=True,null=True)
    activity_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Merchant Activity'
        verbose_name_plural = 'Merchant Activities'

    def __str__(self):
        return str(self.amount)+' - '+str(self.activity_date)

    def __unicode__(self):
        return unicode(str(self.amount)+' - '+str(self.activity_date))


class MerchantActivityStats(models.Model):
    total_transactions = models.IntegerField(default=0,blank=True,null=True)
    total_paid = models.IntegerField(default=0,blank=True,null=True)
    total_refunded = models.IntegerField(default=0,blank=True,null=True)
    total_failed_transactions = models.IntegerField(default=0,blank=True,null=True)
    total_succeeded_transactions = models.IntegerField(default=0,blank=True,null=True)
    credibility_rating = models.IntegerField(default=0,blank=True,null=True)
    last_purchase = models.DateTimeField(blank=True,null=True)

    class Meta:
        verbose_name = 'Merchant Activity Stats'
        verbose_name_plural = 'Merchant Activity Stats'

class CustomerActivityStats(models.Model):
    total_transactions = models.IntegerField(default=0,blank=True,null=True)
    total_paid = models.IntegerField(default=0,blank=True,null=True)
    total_refunded = models.IntegerField(default=0,blank=True,null=True)
    total_failed_transactions = models.IntegerField(default=0,blank=True,null=True)
    total_succeeded_transactions = models.IntegerField(default=0,blank=True,null=True)
    credibility_rating = models.IntegerField(default=0,blank=True,null=True)
    last_purchase = models.DateTimeField(blank=True,null=True)

    class Meta:
        verbose_name = 'Customer Activity Stats'
        verbose_name_plural = 'Customer Activity Stats'


class CardType(models.Model):
    """ Card Type  identify which card type is used """
    card = models.CharField(max_length=100,blank=False,null=False)
    code = models.CharField(max_length=100,blank=False,null=False)

    class Meta:
        verbose_name = 'Card Type'
        verbose_name_plural = 'Card Types'

    def __str__(self):
        return self.card

    def __unicode__(self):
        return unicode(self.card)


class CreditCard(models.Model):
    """ Customer Credit Card """
    time_published = models.DateTimeField(default=datetime.now, blank=True)
    is_default = models.NullBooleanField(default=False,blank=True,null=True)
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=200,blank=True,null=True)
    address = models.ForeignKey(Address, blank=True,null=True)
    owner = models.ForeignKey(Profile, blank=True,null=True)
    token = models.CharField(max_length=600,blank=True,null=True)
    nonce = models.CharField(max_length=600,blank=True,null=True)
    card_id = models.IntegerField(default=0,blank=True,null=True)
    customer_id =  models.IntegerField(blank=True,null=True)
    issuing_bank = models.CharField(max_length=150,blank=True,null=True)
    country_of_issuance = models.CharField(max_length=150,blank=True,null=True)
    unique_number_identifier = models.CharField(max_length=150,blank=True,null=True)
    durbin_regulated = models.CharField(max_length=30,blank=True,null=True)
    payroll = models.CharField(max_length=150,blank=True,null=True)
    card_bin = models.CharField(max_length=150,blank=True,null=True)
    cardholder_name = models.CharField(max_length=140,blank=True)
    prepaid = models.CharField(max_length=150,blank=True,null=True)
    last_4 = models.CharField(max_length=10,blank=True,null=True)
    card_name = models.CharField(max_length=200,blank=True,null=True)
    card_type = models.ForeignKey(CardType,blank=True,null=True)
    card_number = models.CharField(max_length=200,blank=True,null=True)
    card_real_number = models.CharField(max_length=200,blank=True,null=True)
    card_expiration = models.DateField(blank=True, null=True)
    card_cvv = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    card_expiration_year = models.IntegerField()
    card_expiration_month = models.IntegerField()
    holder_first_name = models.CharField(max_length=100,blank=True,null=True)
    holder_last_name = models.CharField(max_length=100,blank=True,null=True)
    card_icon_url  =  models.CharField(max_length=500,blank=True,null=True)
    is_default = models.NullBooleanField(default=False,blank=True,null=True)
    image_url = models.CharField(max_length=300,blank=True,null=True)
 
    class Meta:
        verbose_name = 'Custom Credit Card'
        verbose_name_plural = 'Custom Cards'

    def __str__(self):
        return self.card_number

    def get_username(self):
        return self.owner.username


class TransactionStatus(models.Model):
    """ Transaction Status  identify which transaction type is used """
    status = models.CharField(max_length=100,blank=False,null=False)
    code = models.CharField(max_length=100,blank=False,null=False)

    class Meta:
        verbose_name = 'Transaction Status'
        verbose_name_plural = 'Transaction Status'

    def __str__(self):
        return self.status+' '+self.code

class TransactionType(models.Model):
    """ Transaction Type  identify which transaction type is used """
    type = models.CharField(max_length=100,blank=False,null=False)
    code = models.CharField(max_length=100,blank=False,null=False)

    class Meta:
        verbose_name = 'Transaction Type'
        verbose_name_plural = 'Transaction Types'

    def __str__(self):
        return self.type+' '+self.code


class Transaction(MerchantActivity):
    """ Seller or Buyer"""
    transaction_id = models.CharField(max_length=400,blank=True,null=True)
    type = models.ForeignKey(TransactionType,blank=False,null=True)
    payment_method_used = models.ForeignKey(CreditCard,blank=True,null=True)
    card_unique_identifier = models.CharField(max_length=400,blank=True,null=True)
    total_amount = models.FloatField(default=0)
    shipping_amount = models.FloatField(default=0)
    commission_amount = models.FloatField(default=0)
    taxes_amount = models.FloatField(default=0)
    take_home_amount = models.FloatField(default=0)
    status = models.ForeignKey(TransactionStatus,blank=True,null=True)
    merchant_id = models.CharField(max_length=400,blank=True,null=True)
    customer_id = models.CharField(max_length=400,blank=True,null=True)
    is_in_escrow = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    order_number = models.IntegerField(default=0,null=True,blank=True)
    time_processed = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return self.transaction_id

class Payment(models.Model):
    payment = models.ForeignKey(CustomerPayment, blank=True,null=True) 
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    package_type = models.CharField(max_length=100, blank=True, null=True)
    package_price = models.CharField(max_length=100, blank=True, null=True) 
    message = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'



class CustomerProfile(models.Model):
    customer_id = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=1500,blank=True,null=True)
    ssn = models.CharField(max_length=100,blank=True,null=True)
    address = models.ForeignKey(Address,blank=True,null=True)
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(max_length=100,blank=True, null=True)
    phone = models.CharField(max_length=100,blank=True, null=True)
    customer_cards =  models.ManyToManyField(CreditCard,related_name='customer_cards',blank=True)
    profile = models.OneToOneField(Profile,related_name='customer_profle',blank=True,null=True)
    transactions = models.ManyToManyField(MerchantActivity,related_name='customer_transactions',blank=True)
    orders = models.ManyToManyField(MerchantActivity,related_name='customer_orders',blank=True)
    stats = models.OneToOneField(CustomerActivityStats,related_name='customer_activity_stats',blank=True,null=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'

    def get_card_by_id(self,card_id):
        return self.customer_cards.get(id=card_id)

    def get_default_card(self):
        return self.customer_cards.get(is_default=True)

    # https://developers.braintreepayments.com/start/hello-server/python#generate-a-client-token
    def gen_client_token(self):
        self.token = braintree.ClientToken.generate()
        return self.token

    # https://developers.braintreepayments.com/start/hello-server/python#receive-a-payment-method-nonce-from-your-client
    def save_payment_nonce(self, payment_method_nonce=""):
        self.payment_nonce = payment_method_nonce

    def __str__(self):
        return self.first_name+' '+self.last_name
