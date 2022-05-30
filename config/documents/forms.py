from django.forms import ModelForm

from .models import DocumentModel


class DocumentForm(ModelForm):
    class Meta:
        model = DocumentModel
        fields = '__all__'
        exclude = ('user_from', 'submited', 'archived', 'status', 'load_date')