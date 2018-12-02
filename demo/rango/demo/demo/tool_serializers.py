from rest_framework import serializers
from .common import DemoAPISerializer



class HmacSerializer(DemoAPISerializer):
    password = serializers.CharField(required=True)
    request_time = serializers.DateTimeField(required=True)
    hmac = serializers.CharField(required=False)
    input_only = ("password", "request_time")
    output_only = ('hmac', )
