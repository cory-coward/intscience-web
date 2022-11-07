from django.conf import settings
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CurrentAlarmSerializer


@api_view(['GET'])
@csrf_exempt
def current_alarms(request):
    cached_alarms = cache.get(settings.CACHE_KEY_CURRENT_ALARMS)

    if cached_alarms is None:
        return Response({})

    serializer = CurrentAlarmSerializer(cached_alarms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
