from rango.frame import errors
from rango.frame.utils import pagination
from .models import Student as StudentM



class Student:


    def get(self, student_id):
        try:
            return StudentM.objects.get(student_id=student_id)
        except StudentM.DoesNotExist:
            msg = 'Student of student_id {} not found.'.format(student_id)
            raise errors.DataNotFoundError(msg)


    def add(self, name, gender=0, is_activated=False):
        params = dict(gender=gender, name=name, is_activated=is_activated)
        params = {k: v for k, v in params.items() if v is not None}
        return StudentM.objects.create(**params)


    def update(self, student_id, gender, name, is_activated):
        params = dict(gender=gender, name=name, is_activated=is_activated)
        params = {k: v for k, v in params.items() if v is not None}

        count = StudentM.objects.filter(student_id=student_id).update(**params)
        if count <= 0:
            msg = 'Student of student_id {} not found.'.format(student_id)
            raise errors.DataNotFoundError(msg)


    def delete(self, student_id):
        self.get(student_id).delete()


    def list(self, filters=None, options=None):
        query_set = StudentM.objects.all()
        if filters:
            params = {k: v for k, v in filters.items() if v is not None}
            query_set = set.filter(**params)
        total = len(query_set)
        query_set = pagination.order_and_pagination(query_set, options)
        return total, query_set
