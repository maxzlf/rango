from rest_framework import serializers
from . import errors



class APISerializer(serializers.Serializer):
    request_time = serializers.DateTimeField(required=False)
    validate_only = serializers.BooleanField(required=False)
    field_mask = serializers.CharField(required=False, allow_null=False,
                                       default="")
    input_only = ()
    output_only = ()


    def validate_field_mask(self, data):
        fields = data.split(',')
        fields = [i.strip() for i in fields]
        fields = [i for i in fields if i]
        return fields



class ListSerializer(APISerializer):
    offset = serializers.IntegerField(required=False, min_value=0, default=0)
    limit = serializers.IntegerField(required=False, min_value=0, max_value=50,
                                     default=20)
    order_by = serializers.CharField(required=False, allow_null=False,
                                     default="")
    order_by_fields = ()


    def validate_order_by(self, data):
        rules = data.split(',')
        rules = [i.strip() for i in rules]
        rules = [i for i in rules if i]
        fields = [i[1:] if '-' == i[0] else i for i in rules]

        if any(f not in self.order_by_fields for f in fields):
            raise errors.ParamError(msg="Unsupported order by fields, {}"
                                    .format(rules))
        return rules
