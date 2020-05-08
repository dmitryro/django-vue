from django.forms import ModelForm, Textarea
from redactor.widgets import RedactorEditor
from models import Service
from models import Package


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        widgets = {
            'description':  RedactorEditor(),
        }
        fields = '__all__' #


class PackageForm(ModelForm):
    class Meta:
        model = Package
        widgets = {
            'description':  RedactorEditor(),
        }
        fields = '__all__' #
