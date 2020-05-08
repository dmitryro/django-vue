from django.contrib import admin

from models import Package
from models import PackageType
from models import PackageNote
from models import Service
from models import PackageTerm

from forms import PackageForm
from forms import ServiceForm


class ServiceAdmin(admin.ModelAdmin):
    form = ServiceForm
    fieldsets = ((None, {'fields': ['title','fees','price','is_available','avatar', 'description']}),)
    list_display = ('id', 'title','fees','price','avatar')
    list_editable = ('title','fees','price')
    
    class Meta:
         verbose_name = 'Service'
         verbose_name_plural = 'Services'


class PackageTypeAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['package_type', 'code',]}),)
    list_display = ('id', 'package_type', 'code',)
    list_editable = ('package_type', 'code',)

    class Meta:
         verbose_name = 'Package Type'
         verbose_name_plural = 'Package Types'


class PackageTermAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['term',]}),)
    list_display = ('id', 'term',)
    list_editable = ('term',)

    class Meta:
         verbose_name = 'Package Term'
         verbose_name_plural = 'Package Term'


class PackageNoteAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['note', 'package',]}),)
    list_display = ('note', 'package',)
    list_editable = ('note', 'package',)

    class Meta:
         verbose_name = 'Package Note'
         verbose_name_plural = 'Package Notes'


class PackageAdmin(admin.ModelAdmin):
    form = PackageForm
    fieldsets = ((None, {'fields': ['title', 'fees', 'price', 'is_available',
                                    'services', 'description', 'state', 
                                    'package_type',]}),)
    list_display = ('id', 'title', 'fees', 'price','state', 'package_type',)
    list_editable = ('title', 'fees', 'price', 'state', 'package_type',)

    notes = (PackageNoteAdmin,)
    class Meta:
         verbose_name = 'Service Package'
         verbose_name_plural = 'Service Packages'

admin.site.register(Service, ServiceAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(PackageType, PackageTypeAdmin)
admin.site.register(PackageNote, PackageNoteAdmin)
admin.site.register(PackageTerm, PackageTermAdmin)

















