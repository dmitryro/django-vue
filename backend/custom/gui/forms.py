from django.forms import ModelForm, Textarea
import django.forms as forms
import django.forms.widgets as widgets
from django.forms.widgets import Input
from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput
from ckeditor.widgets import CKEditorWidget
from tinymce.widgets import TinyMCE
from wymeditor.widgets import AdminWYMEditorArea
from froala_editor.widgets import FroalaEditor
from redactor.widgets import RedactorEditor
from suit_redactor.widgets import RedactorWidget
from models import AskTemplate
from models import ConsultTemplate
from models import ConsultationType
from models import Service
from models import Slide
from models import ContactInfo
from models import FAQ
from models import Article
from models import FrontBlock


class FrontBlockForm(ModelForm):
    class Meta:
        model = FrontBlock
        widgets = {
            'body': RedactorWidget(editor_options={'lang': 'en'}),
        }
        fields = '__all__' #


class ConsultationTypeForm(ModelForm):
    class Meta:
        model = ConsultationType
        widgets = {
            'description': RedactorWidget(editor_options={'lang': 'en'}),
        }
        fields = '__all__' #


class ConsultTemplateForm(ModelForm):
    class Meta:
        model = ConsultTemplate
        widgets = {
            'agreement': RedactorWidget(editor_options={'lang': 'en'}),
            'disclaimer': RedactorWidget(editor_options={'lang': 'en'}),
            'consult_intro': RedactorWidget(editor_options={'lang': 'en'}),
        }
        fields = '__all__' #


class AskTemplateForm(ModelForm):
    class Meta:
        model = AskTemplate
        widgets = {
            'agreement': RedactorWidget(editor_options={'lang': 'en'}),
            'disclaimer': RedactorWidget(editor_options={'lang': 'en'}),
            'ask_intro': RedactorWidget(editor_options={'lang': 'en'}),
        }
        fields = '__all__' #



class SlideForm(ModelForm):
    class Meta:
        model = Slide
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 30}),
        }
        fields = '__all__' #

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        widgets = {
            'body': RedactorWidget(editor_options={'lang': 'en'}),
        }
        fields = '__all__' #

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        widgets = {
            'statement': Textarea(attrs={'cols': 80, 'rows': 30}),
            'description': RedactorWidget(editor_options={'lang': 'en'}),
        }
        fields = '__all__' #

class FAQForm(ModelForm):
    class Meta:
        model = FAQ
        widgets = {
            'note': Textarea(attrs={'cols': 80, 'rows': 20}),#CKEditorWidget(),#AdminWYMEditorArea(),#Textarea(attrs={'class':'ckeedior','cols': 80, 'rows': 30}),
            'answer': RedactorWidget(editor_options={'lang': 'en'}), 
        }
        fields = '__all__' #


class ContactInfoForm(ModelForm):
    class Meta:
        model = ContactInfo
        widgets = {
            'statement': RedactorWidget(editor_options={'lang': 'en'}),
        }
        fields = '__all__' #

