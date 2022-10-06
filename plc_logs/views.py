from django.conf import settings
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import WellLogEntrySerializer

from datetime import datetime
import pytz
import random


# @require_safe
@api_view(['GET'])
@csrf_exempt
def current_well_logs(request):
    # if settings.DEBUG is True:
    #     cached_well_readings = []
    #     for i in range(15):
    #         wc = {
    #             'id': i,
    #             'well_name': f'DRW-0{i}' if i < 10 else f'DRW-{i}',
    #             'gal_per_minute': i * random.randrange(1, 15),
    #             'total_gal': i * random.randrange(25, 75),
    #             'is_running': True if random.randrange(0, 1500) % 2 == 0 else False,
    #             'timestamp': datetime.now(pytz.timezone('America/Chicago'))
    #         }
    #         cached_well_readings.append(wc)
    # else:
    cached_well_readings = cache.get(settings.CACHE_KEY_CURRENT_WELL_READINGS)

    if cached_well_readings is None:
        return Response({})

    serializer = WellLogEntrySerializer(cached_well_readings, many=True)
    # return JsonResponse(serializer.data, safe=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def set_well_state(request):
    well_name = request.data.get('well_name', '')
    new_state = request.data.get('new_state', '')

    if well_name == '' or new_state == '':
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response({'well_name': well_name, 'new_state': new_state}, status=status.HTTP_200_OK)
