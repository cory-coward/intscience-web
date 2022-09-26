from django import forms
from django.utils.translation import gettext as _

from .models import MaintenanceLog, GardnerDenverLog


class MaintenanceLogForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ('log_text', )
        labels = {'log_text': _('Maintenance log text')}
        help_texts = {'log_text': _('Enter the text for your maintenance log entry.')}
        widgets = {'log_text': forms.Textarea(attrs={'rows': 5, }), }


class GardnerDenverLogForm(forms.ModelForm):
    class Meta:
        model = GardnerDenverLog
        fields = ('log_text', )
        labels = {'log_text': _('Gardner Denver log text')}
        help_texts = {'log_text': _('Enter the text for your Gardner Denver measurements.')}
        widgets = {'log_text': forms.Textarea(attrs={'rows': 5, }), }
