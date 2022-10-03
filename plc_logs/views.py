from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import WellLogEntrySerializer

from datetime import datetime
import pytz


@csrf_exempt
def current_well_logs(request):
    if request.method == 'GET':
        # cached_well_readings = cache.get(settings.CACHE_KEY_CURRENT_WELL_READINGS)
        #
        # if cached_well_readings is None:
        #     return JsonResponse({})

        cached_well_readings = []
        for i in range(10):
            wc = {
                'id': i,
                'well_name': f'DRW-{i}',
                'gal_per_minute': i * 10,
                'total_gal': i * 25,
                'timestamp': datetime.now(pytz.timezone('America/Chicago'))
            }
            cached_well_readings.append(wc)

        serializer = WellLogEntrySerializer(cached_well_readings, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return
