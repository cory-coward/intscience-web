from django.contrib import admin

from .models import PLCAlarm


class PLCAlarmAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'is_active', 'timestamp', 'timestamp_acknowledged', 'timestamp_cleared', )
    list_filter = ('tag_name', )
    list_per_page = 25


admin.site.register(PLCAlarm, PLCAlarmAdmin)
