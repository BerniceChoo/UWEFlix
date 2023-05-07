from rest_framework import serializers

class ScreenSerializer(serializers.Serializer):
    name = serializers.CharField()
    capacity = serializers.IntegerField()
    social_distancing = serializers.BooleanField()
    

class EditScreenSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    capacity = serializers.IntegerField()
    social_distancing = serializers.BooleanField()


class DeleteScreenSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()