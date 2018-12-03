import datetime
from rango.frame.views import request_wrapper
from rango.frame import errors
from rango.frame.utils import time
from rango.frame.contrib.user import DBUserFactory
from .student import Student
from .common import DemoAPIView
from . import serializers
from .consts import DemoConst



class PingView(DemoAPIView):


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
    serializer_classes = {'POST': serializers.ExampleSerializer,
                          'PUT': serializers.ExampleSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        return dict(foo="aaaa", bar=0)


    @request_wrapper
    def put(self, request, valid_data):
        return valid_data



class ConstantsView(DemoAPIView):
    serializer_classes = {'POST': serializers.ConstantsPostSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        const = self.const_accessor.add(**valid_data)
        result = dict(key=const.key, value=const.value,
                      description=const.description)
        return result


    @request_wrapper
    def get(self, request, valid_data=None):
        total, constants = self.const_accessor.list()
        result = dict(total=total, entries=[])

        for const in constants:
            result['entries'].append(dict(key=const.key,
                                          value=const.value,
                                          description=const.description))
        print(result)
        return result



class ConstantView(DemoAPIView):
    serializer_classes = {'PUT': serializers.ConstantPutSerializer}


    @request_wrapper
    def get(self, request, key, valid_data=None):
        value = self.const_accessor.get(key)
        result = dict(key=key, value=value)
        return result


    @request_wrapper
    def put(self, request, key, valid_data=None):
        const = self.const_accessor.update(key, **valid_data)
        result = dict(key=const.key, value=const.value,
                      description=const.description)
        return result


    @request_wrapper
    def delete(self, request, key, valid_data=None):
        self.const_accessor.delete(key)
        return dict()



class StudentsView(DemoAPIView):
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



class UsersView(DemoAPIView):
    serializer_classes = {'GET': serializers.UsersListSerializer,
                          'POST': serializers.UsersPostSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        user_accessor = DBUserFactory().create()
        user = user_accessor.add(**valid_data)
        result = dict(user_id=user.user_id,
                      account=user.account,
                      is_activated=user.is_activated,
                      create_time=user.create_time,
                      update_time=user.update_time)
        return result


    @request_wrapper
    def get(self, request, valid_data):
        user_accessor = DBUserFactory().create()
        options = valid_data.get('options', None)
        total, users = user_accessor.list(options=options)
        result = dict(total=total, entries=[])
        for user in users:
            result['entries'].append(dict(user_id=user.user_id,
                                          account=user.account,
                                          is_activated=user.is_activated,
                                          create_time=user.create_time,
                                          update_time=user.update_time))
        return result



class LoginView(DemoAPIView):
    serializer_classes = {'POST': serializers.LoginSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        account = valid_data['account']
        password = valid_data['password']

        const = DemoConst(self.const_accessor)
        expiry_seconds = const.expiry_seconds

        user_accessor = DBUserFactory().create()
        user = user_accessor.get(account=account)
        if not user_accessor.check_password(password=password, account=account):
            raise errors.PasswordError

        expiry_time = datetime.datetime.now() + \
            datetime.timedelta(seconds=expiry_seconds)
        stoken = self.token_accessor.add(user=user, expiry_time=expiry_time)
        result = dict(token=stoken.token, secret=stoken.secret,
                      host=stoken.host, expiry_time=stoken.expiry_time,
                      create_time=stoken.create_time)
        return result


    @request_wrapper
    def delete(self, request, valid_data=None):
        stoken = request.stoken
        stoken.delete()
