from rango.frame import errors
from rango.frame.utils import pagination
from .models import Class as ClassM



class Class:


    def get(self, class_id):
        try:
            return ClassM.objects.get(class_id=class_id)
        except ClassM.DoesNotExist:
            msg = 'Class of class_id {} not found.'.format(class_id)
            raise errors.DataNotFoundError(msg)


    def add(self, class_no, is_activated=False):
        params = dict(class_no=class_no, is_activated=is_activated)
        params = {k: v for k, v in params.items() if v is not None}
        return ClassM.objects.create(**params)


    def update(self, class_id, class_no, is_activated):
        params = dict(class_no=class_no, is_activated=is_activated)
        params = {k: v for k, v in params.items() if v is not None}

        count = ClassM.objects.filter(class_id=class_id).update(**params)
        if count <= 0:
            msg = 'Class of class_id {} not found.'.format(class_id)
            raise errors.DataNotFoundError(msg)


    def delete(self, class_id):
        self.get(class_id).delete()


    def list(self, filters=None, options=None):
        query_set = ClassM.objects.all()
        if filters:
            params = {k: v for k, v in filters.items() if v is not None}
            query_set = set.filter(**params)
        total = len(query_set)
        query_set = pagination.order_and_pagination(query_set, options)
        return total, query_set
