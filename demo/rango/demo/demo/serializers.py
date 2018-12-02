from rest_framework import serializers
from .common import DemoAPISerializer, DemoListSerializer



class ExampleSerializer(DemoAPISerializer):
    foo = serializers.CharField(required=False)
    bar = serializers.IntegerField(min_value=0, max_value=100)
    input_only = ("foo", )
    output_only = ('bar', )



class ConstantsPostSerializer(DemoAPISerializer):
    key = serializers.CharField(required=True, max_length=64)
    value = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True,
                                        max_length=256)



class ConstantPutSerializer(DemoAPISerializer):
    value = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True,
                                        max_length=256)



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



class UsersPostSerializer(DemoAPISerializer):
    user_id = serializers.UUIDField(required=False)
    account = serializers.CharField(min_length=1, max_length=64)
    password = serializers.CharField(max_length=128)
    is_activated = serializers.BooleanField(required=False, default=False)
    create_time = serializers.DateTimeField(required=False)
    update_time = serializers.DateTimeField(required=False)
    input_only = ('password', )
    output_only = ('user_id', 'create_time', 'update_time')



class UsersListSerializer(DemoListSerializer):
    order_by_fields = ('account', 'create_time', 'update_time')



class UserPutSerializer(DemoAPISerializer):
    user_id = serializers.UUIDField(required=False)
    account = serializers.CharField(required=False, min_length=1, max_length=64)
    password = serializers.CharField(required=False, max_length=128)
    is_activated = serializers.BooleanField(required=False, default=False)
    create_time = serializers.DateTimeField(required=False)
    update_time = serializers.DateTimeField(required=False)
    input_only = ('password', )
    output_only = ('user_id', 'create_time', 'update_time')



class LoginSerializer(DemoAPISerializer):
    account = serializers.CharField(required=True, min_length=1, max_length=64)
    request_time = serializers.DateTimeField(required=True)
    hmac = serializers.CharField(required=True, min_length=1, max_length=128)
    input_only = ('account', 'request_time', 'hmac')
