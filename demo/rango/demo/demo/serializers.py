from rest_framework import serializers


from .common import DemoAPISerializer, DemoListSerializer



class ExampleSerializer(DemoAPISerializer):
    foo = serializers.CharField(required=False)
    bar = serializers.IntegerField(min_value=0, max_value=100)
    input_only = ("foo", )
    output_only = ('bar', )



class StudentsPostSerializer(DemoAPISerializer):
    student_id = serializers.UUIDField(required=False)
    gender = serializers.IntegerField(required=False,
                                      min_value=0,
                                      max_value=2,
                                      default=0)
    name = serializers.CharField(max_length=64)
    is_activated = serializers.BooleanField(required=False, default=False)
    create_time = serializers.DateTimeField(required=False)
    update_time = serializers.DateTimeField(required=False)
    output_only = ('student_id', 'create_time', 'update_time')



class StudentsListSerializer(DemoListSerializer):
    order_by_fields = ('name', 'create_time', 'update_time')



class StudentGetSerializer(DemoAPISerializer):
    student_id = serializers.UUIDField(required=False)
    gender = serializers.IntegerField(required=False,
                                      min_value=0,
                                      max_value=2,
                                      default=0)
    name = serializers.CharField(required=False, max_length=64)
    is_activated = serializers.BooleanField(required=False, default=False)
    create_time = serializers.DateTimeField(required=False)
    update_time = serializers.DateTimeField(required=False)
    output_only = ('student_id', 'gender', 'name',
                   'is_activated', 'create_time', 'update_time')



class StudentPutSerializer(DemoAPISerializer):
    student_id = serializers.UUIDField(required=False)
    gender = serializers.IntegerField(required=False,
                                      min_value=0,
                                      max_value=2,
                                      default=0)
    name = serializers.CharField(max_length=64)
    is_activated = serializers.BooleanField(required=False, default=False)
    create_time = serializers.DateTimeField(required=False)
    update_time = serializers.DateTimeField(required=False)
    output_only = ('student_id', 'create_time', 'update_time')
