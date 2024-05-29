from django import forms
from .models import PumpingValueModel


class PumpForm(forms.ModelForm):
    class Meta:
        model = PumpingValueModel
        fields = ('value',)
