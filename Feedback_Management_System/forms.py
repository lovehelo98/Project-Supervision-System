from django import forms
from .models import descriptions

class descriptionform(forms.ModelForm):
    class Meta:
        model = descriptions
        fields =('descp',)