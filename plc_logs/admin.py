from django.contrib import admin

from .models import WellLogEntry


class WellLogEntryAdmin(admin.ModelAdmin):
    list_display = ('well_name', 'timestamp', )
    list_filter = ('well_name', )
    list_per_page = 25


admin.site.register(WellLogEntry, WellLogEntryAdmin)
