import datetime
from rest_framework.response import Response
from rango.frame.views import request_wrapper
from .student import Student
from .common import DemoAPIView
from .permissions import AllowAny
from . import serializers



class PingView(DemoAPIView):
    permission_classes = (AllowAny,)


    @request_wrapper()
    def get(self, request, valid_data):
        result = dict(time=datetime.datetime.now())
        return Response(result)



class ExampleView(DemoAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = {'POST': serializers.ExampleSerializer,
                          'PUT': serializers.ExampleSerializer}


    @request_wrapper()
    def post(self, request, valid_data):
        return Response(valid_data)


    @request_wrapper()
    def put(self, request, valid_data):
        return Response(valid_data)



class StudentsView(DemoAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = {'POST': serializers.StudentPostSerializer}


    @request_wrapper()
    def post(self, request, valid_data):
        student = Student().add(**valid_data)
        result = dict(student_id=student.student_id,
                      gender=student.gender,
                      name=student.name,
                      is_activated=student.is_activated,
                      create_time=student.create_time,
                      update_time=student.update_time)
        return Response(result)



class StudentView(DemoAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = {'GET': serializers.StudentGetSerializer}


    def get(self, request, student_id):
        student = Student().get(student_id)
        result = dict(student_id=student.student_id,
                      gender=student.gender,
                      name=student.name,
                      is_activated=student.is_activated,
                      create_time=student.create_time,
                      update_time=student.update_time)
        return Response(result)
