from django.contrib import admin

from .models import MaintenanceLog, GardnerDenverLog


class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_on', )
    list_per_page = 25


class GardnerDenverLogAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_on',)
    list_per_page = 25


admin.site.register(MaintenanceLog, MaintenanceLogAdmin)
admin.site.register(GardnerDenverLog, GardnerDenverLogAdmin)
