from rest_framework import serializers
from . import errors



class APISerializer(serializers.Serializer):
    validate_only = serializers.BooleanField(required=False)
    input_only = ()
    output_only = ()



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
