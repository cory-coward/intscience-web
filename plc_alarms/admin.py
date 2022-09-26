from django.contrib import admin

from .models import PLCAlarm


class PLCAlarmAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'timestamp', )
    list_filter = ('tag_name', )
    list_per_page = 25


admin.site.register(PLCAlarm, PLCAlarmAdmin)
