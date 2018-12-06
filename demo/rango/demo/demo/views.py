import datetime
from rest_framework.generics import GenericAPIView

from rango.frame import errors
from rango.frame.views import LoggedAPIView
from rango.frame.views import request_wrapper
from rango.frame.permissions import AllowAny, IsActivated, IsSTokenAuthenticated
from rango.frame.contrib.user import DBUserFactory
from rango.frame.contrib.token import DBTokenFactory
from rango.frame.contrib.constant import DBConstantFactory

from .student import Student
from .cclass import Class
from . import serializers
from .consts import DemoConst



class DemoViewMixin(LoggedAPIView):
    common_permission_classes = (IsActivated, )


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.const_accessor = DBConstantFactory().create()
        self.token_accessor = DBTokenFactory().create()



class DemoAPIView(DemoViewMixin, GenericAPIView):
    pass



class ExampleView(DemoAPIView):
    serializer_classes = {'POST': serializers.ExampleSerializer,
                          'PUT': serializers.ExampleSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        return dict(foo="aaaa", bar=0)


    @request_wrapper
    def put(self, request, valid_data):
        return valid_data



class ClassesView(DemoAPIView):
    get_permission_classes = (IsSTokenAuthenticated,)
    post_permission_classes = (IsSTokenAuthenticated,)
    serializer_classes = {'GET': serializers.ClassesListSerializer,
                          'POST': serializers.ClassesPostSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        cclass = Class().add(**valid_data)
        result = dict(class_id=cclass.class_id,
                      class_no=cclass.class_no,
                      is_activated=cclass.is_activated,
                      create_time=cclass.create_time,
                      update_time=cclass.update_time)
        return result


    @request_wrapper
    def get(self, request, valid_data):
        options = valid_data.get('options', None)
        total, classes = Class().list(options=options)
        result = dict(total=total, entries=[])
        for cclass in classes:
            result['entries'].append(dict(class_id=cclass.class_id,
                                          class_no=cclass.class_no,
                                          is_activated=cclass.is_activated,
                                          create_time=cclass.create_time,
                                          update_time=cclass.update_time))
        return result



class StudentsView(DemoAPIView):
    get_permission_classes = (IsSTokenAuthenticated,)
    post_permission_classes = (IsSTokenAuthenticated,)
    serializer_classes = {'GET': serializers.StudentsListSerializer,
                          'POST': serializers.StudentsPostSerializer}


    @request_wrapper
    def post(self, request, class_id, valid_data):
        valid_data['class_id'] = class_id
        student = Student().add(**valid_data)
        result = dict(student_id=student.student_id,
                      gender=student.gender,
                      name=student.name,
                      is_activated=student.is_activated,
                      create_time=student.create_time,
                      update_time=student.update_time)
        return result


    @request_wrapper
    def get(self, request, class_id, valid_data):
        filters = dict(class_id=None if class_id == '-' else class_id)
        options = valid_data.get('options', None)
        total, students = Student().list(filters=filters, options=options)
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
    get_permission_classes = (IsSTokenAuthenticated,)


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


    @request_wrapper
    def delete(self, request, student_id, valid_data=None):
        student = Student().get(student_id)
        student.delete(student_id)



class UsersView(DemoAPIView):
    post_permission_classes = ()
    get_permission_classes = ()
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
    post_permission_classes = ()
    delete_permission_classes = (IsSTokenAuthenticated,)


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
