from django.forms import Field, BooleanField, NullBooleanField, CharField
from django.forms import IntegerField, FloatField, DecimalField
from django.forms import DateField, TimeField, DateTimeField
from django.forms import DurationField, RegexField, EmailField, FileField
from django.forms import ImageField, URLField, ChoiceField, TypedChoiceField
from django.forms import MultipleChoiceField, TypedMultipleChoiceField
from django.forms import ComboField, MultiValueField, FileField
from django.forms import SplitDateTimeField, GenericIPAddressField, SlugField
from django.forms import UUIDField



class FieldEx(Field):
    IGNORED_FIELD = 'IGNORED_FIELD'



    def __init__(self, output_only=False, **kwargs):
        super().__init__(**kwargs)
        self.output_only = output_only


    def clean(self, value):
        value = super().clean(value)
        if self.output_only is True:
            value = self.IGNORED_FIELD
        return value



class BooleanFieldEx(FieldEx, BooleanField):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def clean(self, value):
        print("==========")
        print(value)
        return super().clean(value)


    def to_python(self, value):
        print("==========")
        return super().to_python(value)


    def validate(self, value):
        print("==========")
        return super().validate(value)
