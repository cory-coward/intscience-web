from rest_framework import serializers


class WellLogEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    well_name = serializers.CharField(max_length=25)
    gal_per_minute = serializers.FloatField(default=0)
    total_gal = serializers.FloatField(default=0)
    pump_mode = serializers.CharField(max_length=20)
    is_running = serializers.BooleanField(default=False)
    timestamp = serializers.DateTimeField()

    # We won't need to save through the API so these functions aren't needed
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
