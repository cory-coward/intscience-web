from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from datetime import datetime
from import_export import resources
from import_export.admin import ExportMixin

from .models import WellLogEntry


class WellLogEntryResource(resources.ModelResource):
    class Meta:
        model = WellLogEntry


class WellLogEntryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('well_name', 'gal_per_minute', 'total_gal', 'pump_mode', 'is_running', 'timestamp', )
    list_filter = (('timestamp', DateRangeFilter), 'well_name', )
    list_per_page = 25
    readonly_fields = ('well_name', 'gal_per_minute', 'total_gal', 'pump_mode', 'is_running', 'timestamp', )
    resource_classes = [WellLogEntryResource, ]

    def get_rangefilter_timestamp_default(self, request):
        return datetime.today, datetime.today

    def get_rangefilter_timestamp_title(self, request, field_path):
        return 'Well Log Entry Date/Time'


admin.site.register(WellLogEntry, WellLogEntryAdmin)
