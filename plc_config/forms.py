from django import forms

from .models import WellConfig


class WellConfigForm(forms.ModelForm):
    class Meta:
        model = WellConfig
        fields = ['well_name', 'description', 'tag_prefix', 'cycle_gallons', 'sleep_minutes', ]

    def __init__(self, *args, **kwargs):
        # user = kwargs.get('user', None)
        print(kwargs)
        super(WellConfigForm, self).__init__(*args, **kwargs)
        # if not user.has_perm('plc_config.add_well_config'):
        #     self.fields.pop('tag_prefix')

