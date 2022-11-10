from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from datetime import datetime
from import_export import resources
from import_export.admin import ExportMixin

from .models import WellLogEntry, AirStripperLogEntry, ZoneFlowLogEntry, GardnerDenverBlowerLogEntry, \
    HeatExchangerLogEntry, SurgeTankLogEntry, DischargeWaterLogEntry


class WellLogEntryResource(resources.ModelResource):
    class Meta:
        model = WellLogEntry


class AirStripperLogEntryResource(resources.ModelResource):
    class Meta:
        model = AirStripperLogEntry


class ZoneFlowLogEntryResource(resources.ModelResource):
    class Meta:
        model = ZoneFlowLogEntry


class GardnerDenverLogEntryResource(resources.ModelResource):
    class Meta:
        model = GardnerDenverBlowerLogEntry


class HeatExchangerLogEntryResource(resources.ModelResource):
    class Meta:
        model = HeatExchangerLogEntry


class SurgeTankLogEntryResource(resources.ModelResource):
    class Meta:
        model = SurgeTankLogEntry


class DischargeWaterLogEntryResource(resources.ModelResource):
    class Meta:
        model = DischargeWaterLogEntry


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


class AirStripperLogEntryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('air_stripper_name', 'pump_runtime', 'blower_runtime', 'timestamp', )
    list_filter = (('timestamp', DateRangeFilter), 'air_stripper_name', )
    list_per_page = 25
    readonly_fields = ('air_stripper_name', 'pump_runtime', 'blower_runtime', 'timestamp', )
    resource_classes = [AirStripperLogEntryResource, ]

    def get_rangefilter_timestamp_default(self, request):
        return datetime.today, datetime.today

    def get_rangefilter_timestamp_title(self, request, field_path):
        return 'Air Stripper Log Entry Date/Time'


class ZoneFlowLogEntryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('zone_flow_left', 'zone_flow_right', 'timestamp', )
    list_filter = (('timestamp', DateRangeFilter), )
    list_per_page = 25
    readonly_fields = ('zone_flow_left', 'zone_flow_right', 'timestamp', )
    resource_classes = [ZoneFlowLogEntryResource, ]

    def get_rangefilter_timestamp_default(self, request):
        return datetime.today, datetime.today

    def get_rangefilter_timestamp_title(self, request, field_path):
        return 'Zone Flow Log Entry Date/Time'


class GardnerDenverLogEntryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('intake_pre_air_filter_vacuum', 'intake_temp', 'timestamp', )
    list_filter = (('timestamp', DateRangeFilter),)
    list_per_page = 25
    readonly_fields = ('intake_pre_air_filter_vacuum', 'intake_temp', 'timestamp',)
    resource_classes = [GardnerDenverLogEntryResource, ]

    def get_rangefilter_timestamp_default(self, request):
        return datetime.today, datetime.today

    def get_rangefilter_timestamp_title(self, request, field_path):
        return 'Gardner Denver Blower Log Entry Date/Time'


class HeatExchangerLogEntryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('flow_rate', 'flow_total', 'pressure', 'outlet_air_temp', 'timestamp',)
    list_filter = (('timestamp', DateRangeFilter),)
    list_per_page = 25
    readonly_fields = ('flow_rate', 'flow_total', 'pressure', 'outlet_air_temp', 'timestamp',)
    resource_classes = [HeatExchangerLogEntryResource, ]

    def get_rangefilter_timestamp_default(self, request):
        return datetime.today, datetime.today

    def get_rangefilter_timestamp_title(self, request, field_path):
        return 'Heat Exchanger Log Entry Date/Time'

class DischargeWaterLogEntryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('flow_rate', 'flow_total', 'timestamp',)
    list_filter = (('timestamp', DateRangeFilter),)
    list_per_page = 25
    readonly_fields = ('flow_rate', 'flow_total', 'timestamp',)
    resource_classes = [DischargeWaterLogEntryResource, ]

    def get_rangefilter_timestamp_default(self, request):
        return datetime.today, datetime.today

    def get_rangefilter_timestamp_title(self, request, field_path):
        return 'Discharge Water Log Entry Date/Time'

class SurgeTankLogEntryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('flow_rate', 'flow_total', 'timestamp',)
    list_filter = (('timestamp', DateRangeFilter),)
    list_per_page = 25
    readonly_fields = ('flow_rate', 'flow_total', 'timestamp',)
    resource_classes = [SurgeTankLogEntryResource, ]

    def get_rangefilter_timestamp_default(self, request):
        return datetime.today, datetime.today

    def get_rangefilter_timestamp_title(self, request, field_path):
        return 'Surge Tank Log Entry Date/Time'


admin.site.register(WellLogEntry, WellLogEntryAdmin)
admin.site.register(AirStripperLogEntry, AirStripperLogEntryAdmin)
admin.site.register(ZoneFlowLogEntry, ZoneFlowLogEntryAdmin)
admin.site.register(GardnerDenverBlowerLogEntry, GardnerDenverLogEntryAdmin)
admin.site.register(HeatExchangerLogEntry, HeatExchangerLogEntryAdmin)
admin.site.register(SurgeTankLogEntry, SurgeTankLogEntryAdmin)
admin.site.register(DischargeWaterLogEntry, DischargeWaterLogEntryAdmin)
