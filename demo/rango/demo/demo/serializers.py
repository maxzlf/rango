from rest_framework import serializers
from rango.frame.serializers import APISerializer, ListSerializer



class ExampleSerializer(APISerializer):
    foo = serializers.CharField(required=False)
    bar = serializers.IntegerField(min_value=0, max_value=100)
    input_only = ("foo", )
    output_only = ('bar', )



class ClassesPostSerializer(APISerializer):
    class_id = serializers.UUIDField(required=False)
    class_no = serializers.IntegerField(required=True, min_value=0)
    is_activated = serializers.BooleanField(required=False, default=False)
    create_time = serializers.DateTimeField(required=False)
    update_time = serializers.DateTimeField(required=False)
    output_only = ('class_id', 'create_time', 'update_time')



class ClassesListSerializer(ListSerializer):
    order_by_fields = ('class_no', 'create_time', 'update_time')



class StudentsPostSerializer(APISerializer):
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



class StudentsListSerializer(ListSerializer):
    order_by_fields = ('name', 'create_time', 'update_time')



class StudentPutSerializer(APISerializer):
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



class UsersPostSerializer(APISerializer):
    user_id = serializers.UUIDField(required=False)
    account = serializers.CharField(min_length=1, max_length=64)
    password = serializers.CharField(min_length=1, max_length=128)
    is_activated = serializers.BooleanField(required=False, default=False)
    create_time = serializers.DateTimeField(required=False)
    update_time = serializers.DateTimeField(required=False)
    input_only = ('password', )
    output_only = ('user_id', 'create_time', 'update_time')



class UsersListSerializer(ListSerializer):
    order_by_fields = ('account', 'create_time', 'update_time')



class UserPutSerializer(APISerializer):
    user_id = serializers.UUIDField(required=False)
    account = serializers.CharField(required=False, min_length=1, max_length=64)
    password = serializers.CharField(required=False, max_length=128)
    is_activated = serializers.BooleanField(required=False, default=False)
    create_time = serializers.DateTimeField(required=False)
    update_time = serializers.DateTimeField(required=False)
    input_only = ('password', )
    output_only = ('user_id', 'create_time', 'update_time')



class LoginSerializer(APISerializer):
    account = serializers.CharField(required=True, min_length=1, max_length=64)
    password = serializers.CharField(min_length=1, max_length=128)
    input_only = ('account', 'password')
