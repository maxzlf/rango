import datetime
from rango.frame.views import request_wrapper
from rango.frame.contrib import constant
from .student import Student
from .common import DemoAPIView
from .permissions import AllowAny
from . import serializers



class PingView(DemoAPIView):
    permission_classes = (AllowAny,)


    @request_wrapper
    def get(self, request, valid_data):
        result = dict(time=datetime.datetime.now())
        from django.contrib.auth.hashers import check_password
        from django.contrib.auth.hashers import make_password
        from django.contrib.auth.hashers import is_password_usable
        password = "plain_text"
        print(is_password_usable(password))
        hashed_password = make_password(password)
        print("Hashed password is:", hashed_password)
        print(check_password(password, hashed_password))
        print(check_password("plain_text ", hashed_password))

        print(datetime.datetime.now())

        return result



class ExampleView(DemoAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = {'POST': serializers.ExampleSerializer,
                          'PUT': serializers.ExampleSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        return dict(foo="aaaa", bar=0)


    @request_wrapper
    def put(self, request, valid_data):
        return valid_data



class ConstantsView(DemoAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = {'POST': serializers.ConstantsPostSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        const = constant.Constant().add(**valid_data)
        result = dict(key=const.key, value=const.value,
                      description=const.description)
        return result


    @request_wrapper
    def get(self, request, valid_data):
        total, consts = constant.Constant().list()
        result = dict(total=total, entries=[])
        for const in consts:
            result['entries'].append(dict(key=const.key,
                                          value=const.value,
                                          description=const.description))
        return result



class ConstantView(DemoAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = {'PUT': serializers.ConstantPutSerializer}


    @request_wrapper
    def get(self, request, key, valid_data=None):
        value = constant.Constant().get(key)
        result = dict(key=key, value=value)
        return result


    @request_wrapper
    def put(self, request, key, valid_data=None):
        const = constant.Constant().update(key, **valid_data)
        result = dict(key=const.key, value=const.value,
                      description=const.description)
        return result


    @request_wrapper
    def delete(self, request, key, valid_data=None):
        constant.Constant().delete(key)
        return dict()



class StudentsView(DemoAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = {'GET': serializers.StudentsListSerializer,
                          'POST': serializers.StudentsPostSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        student = Student().add(**valid_data)
        result = dict(student_id=student.student_id,
                      gender=student.gender,
                      name=student.name,
                      is_activated=student.is_activated,
                      create_time=student.create_time,
                      update_time=student.update_time)
        return result


    @request_wrapper
    def get(self, request, valid_data):
        options = valid_data.get('options', None)
        total, students = Student().list(options=options)
        result = dict(total=total, entries=[])
        for student in students:
            result['entries'].append(dict(student_id=student.student_id,
                                          gender=student.gender,
                                          name=student.name,
                                          is_activated=student.is_activated,
                                          create_time=student.create_time,
                                          update_time=student.update_time))
        return result



class StudentView(DemoAPIView):
    permission_classes = (AllowAny,)


    @request_wrapper
    def get(self, request, student_id, valid_data=None):
        student = Student().get(student_id)
        result = dict(student_id=student.student_id,
                      gender=student.gender,
                      name=student.name,
                      is_activated=student.is_activated,
                      create_time=student.create_time,
                      update_time=student.update_time)
        return result
