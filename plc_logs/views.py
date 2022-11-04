from django.conf import settings
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from plc_core.plc_ops import read_plc_tags, set_well_mode

from .permissions import WellPumpModePermission
from .serializers import WellLogEntrySerializer


@api_view(['GET'])
@csrf_exempt
def current_well_logs(request):
    cached_well_readings = cache.get(settings.CACHE_KEY_CURRENT_WELL_READINGS)

    if cached_well_readings is None:
        return Response({})

    serializer = WellLogEntrySerializer(cached_well_readings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((WellPumpModePermission, ))
def set_pump_mode(request):
    well_name = request.data.get('well_name', '')
    new_mode = request.data.get('new_mode', '')

    response: bool = set_well_mode(well_name, new_mode)

    http_status: int = 0

    if response is True:
        http_status = status.HTTP_200_OK
        read_plc_tags()
    else:
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response({'well_name': well_name, 'new_mode': new_mode}, status=http_status)
