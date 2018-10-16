from rest_framework import serializers
from rango.frame import errors
from .common import DemoAPISerializer



class ExampleSerializer(DemoAPISerializer):
    foo = serializers.CharField(max_length=16)
    bar = serializers.IntegerField(min_value=0, max_value=100)


    def validate_bar(self, data):
        if data % 5 == 0:
            raise errors.ParamValidationError(
                msg='bar should not be divided by 5')
        return data
