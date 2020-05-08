from django.forms import ModelForm, Textarea
from redactor.widgets import RedactorEditor
from models import Post
from suit_redactor.widgets import RedactorWidget


class PostForm(ModelForm):
    class Meta:
        model = Post
        widgets = {
            'body':  RedactorWidget(editor_options={'lang': 'en'}),
        }
        fields = '__all__' #

