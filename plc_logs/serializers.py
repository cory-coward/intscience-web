from rest_framework import serializers

from .models import WellLogEntry


# class WellLogEntrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WellLogEntry
#         fields = ['id', 'well_name', 'gal_per_minute', 'total_gal', 'timestamp']


class WellLogEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    well_name = serializers.CharField(max_length=25)
    gal_per_minute = serializers.FloatField(default=0)
    total_gal = serializers.FloatField(default=0)
    is_running = serializers.BooleanField(default=False)
    timestamp = serializers.DateTimeField()

    # We won't need to save through the API so these functions aren't needed
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
