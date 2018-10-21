import uuid
from django.db import models
from rango.frame.contrib.trash import move2trash



class Student(models.Model):
    student_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    gender = models.IntegerField(default=0)
    name = models.CharField(max_length=64)
    is_activated = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


    def __str__(self):
        return str(self.student_id)


    def delete(self, using=None, keep_parents=False):
        move2trash(self)
        super().delete(using, keep_parents)
