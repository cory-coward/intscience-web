from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from datetime import datetime

from .models import WellLogEntry


class WellLogEntryAdmin(admin.ModelAdmin):
    list_display = ('well_name', 'gal_per_minute', 'total_gal', 'is_running', 'timestamp', )
    list_filter = (('timestamp', DateRangeFilter), 'well_name', )
    list_per_page = 25
    readonly_fields = ('well_name', 'gal_per_minute', 'total_gal', 'is_running', 'timestamp', )

    def get_rangefilter_timestamp_default(self, request):
        return datetime.today, datetime.today

    def get_rangefilter_timestamp_title(self, request, field_path):
        return 'Well Log Entry Date/Time'


admin.site.register(WellLogEntry, WellLogEntryAdmin)
