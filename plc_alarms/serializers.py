from rest_framework import serializers


class CurrentAlarmSerializer(serializers.Serializer):
    alarm_tag = serializers.CharField(max_length=50)
    alarm_description = serializers.CharField(max_length=250)
    dial = serializers.BooleanField(default=False)
    alarm_time = serializers.DateTimeField()
    ack_time = serializers.DateTimeField()
    clear_time = serializers.DateTimeField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
