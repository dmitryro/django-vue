from __future__ import unicode_literals

from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from custom.gui.models import State
from taggit.managers import TaggableManager


class Service(models.Model):
   title = models.CharField(max_length=200,blank=True,null=True)
   fees = models.FloatField(default=0,blank=True,null=True)
   price = models.FloatField(default=0,blank=True,null=True)
   is_available = models.NullBooleanField(default=True,blank=True,null=True)
   description = models.TextField(blank=True,null=True)
   avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
   avatar_thumbnail = ImageSpecField(source='avatar',
                                     processors=[ResizeToFill(100, 50)],
                                     format='JPEG',
                                     options={'quality': 60})
   def __str__(self):
        return self.title

   class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class PackageType(models.Model):
   package_type =  models.CharField(max_length=200, blank=True, null=True)
   code =  models.CharField(max_length=200, blank=True, null=True)

   def __str__(self):
        return self.package_type

   class Meta:
        verbose_name = 'Package Type'
        verbose_name_plural = 'Packate Types'

class Package(models.Model):
   state = models.ForeignKey(State, blank=True, null=True)
   title = models.CharField(max_length=200, blank=True, null=True)
   fees = models.FloatField(default=0, blank=True, null=True)
   price = models.FloatField(default=0, blank=True, null=True)
   package_type = models.ForeignKey(PackageType, blank=True, null=True)
   is_available = models.NullBooleanField(default=True, blank=True, null=True)  
   description = models.TextField(blank=True, null=True)
   services = models.ManyToManyField(Service, related_name='services',
                                     symmetrical=False)

   def __str__(self):
        return self.title


   class Meta:
        verbose_name = 'Service Package'
        verbose_name_plural = 'Service Packages'  


class PackageNote(models.Model):
    note = models.CharField(max_length=200, blank=True, null=True)
    package = models.ForeignKey(Package, related_name='notes', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.note

    class Meta:
        unique_together = ('package', 'note')
        ordering = ['package']
        verbose_name = 'Package Note'
        verbose_name_plural = 'Package Notes'


class PackageTerm(models.Model):
    term = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.term

    class Meta:
        verbose_name = 'Package Term'
        verbose_name_plural = 'Package Terms'
   
 








  
   
# Create your models here.
