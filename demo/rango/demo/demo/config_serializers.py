from rest_framework import serializers
from rango.frame.serializers import APISerializer



class ConstantsPostSerializer(APISerializer):
    key = serializers.CharField(required=True, max_length=64)
    value = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True,
                                        max_length=256)



class ConstantPutSerializer(APISerializer):
    value = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True,
                                        max_length=256)
