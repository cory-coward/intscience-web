from django.contrib import admin

from .forms import WellConfigForm
from .models import GeneralConfig, WellConfig


class GeneralConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'well_record_minutes', )
    list_editable = ('well_record_minutes', )
    list_per_page = 5


class WellConfigAdmin(admin.ModelAdmin):
    list_display = ('well_name', 'tag_prefix', 'cycle_gallons', 'sleep_minutes', )
    list_editable = ('cycle_gallons', 'sleep_minutes', )
    list_per_page = 25

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not request.user.has_perm('plc_config.add_wellconfig'):
            self.readonly_fields = ('tag_prefix', )
        form = super(WellConfigAdmin, self).get_form(request, obj, **kwargs)
        return form


admin.site.register(GeneralConfig, GeneralConfigAdmin)
admin.site.register(WellConfig, WellConfigAdmin)
