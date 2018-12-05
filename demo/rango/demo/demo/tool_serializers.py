from rest_framework import serializers
from .common import DemoAPISerializer



class HmacSerializer(DemoAPISerializer):
    password = serializers.CharField(required=True)
    data = serializers.DictField(required=True)
    hmac = serializers.CharField(required=False)
    json_encoded = serializers.CharField(required=False)
    input_only = ("password", "data")
    output_only = ('hmac', 'json_encoded')
