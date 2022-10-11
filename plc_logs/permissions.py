from rest_framework import permissions


class WellPumpModePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('plc_logs.change_welllogentry'):
            return True

        return False
