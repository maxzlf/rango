from rest_framework import serializers

from .common import DemoAPISerializer



class ExampleSerializer(DemoAPISerializer):
    foo = serializers.CharField(required=False)
    bar = serializers.IntegerField(min_value=0, max_value=100)
    output_only = serializers.ListField(required=False, default=['foo'])
