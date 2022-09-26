from django.contrib import admin

from .models import WellConfig


class WellConfigAdmin(admin.ModelAdmin):
    list_display = ('well_name', 'tag_prefix', 'record_minutes', )
    list_editable = ('record_minutes', )
    list_per_page = 25


admin.site.register(WellConfig, WellConfigAdmin)
