from django.contrib import admin

from .models import GeneralConfig, WellConfig


class GeneralConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'well_record_minutes', )
    list_editable = ('well_record_minutes', )
    list_per_page = 5


class WellConfigAdmin(admin.ModelAdmin):
    list_display = ('well_name', 'tag_prefix', 'cycle_gallons', 'sleep_minutes', )
    list_editable = ('cycle_gallons', 'sleep_minutes', )
    list_per_page = 25


admin.site.register(GeneralConfig, GeneralConfigAdmin)
admin.site.register(WellConfig, WellConfigAdmin)
