# -*- coding: utf-8 -*-
import json
import copy
import logging
from ..utils.json import JsonEncoder
from . import models


logger = logging.getLogger(__name__)



class Trash:


    def __init__(self, model):
        self._model = model


    def add(self, content, comment=''):
        models.Trash.objects.create(model=self._model,
                                    content=content,
                                    comment=comment)


    def gets(self):
        trashes = models.Trash.objects.filter(model=self._model)
        return trashes


def move2trash(obj):
    content = copy.copy(obj.__dict__)
    if '_state' in content.keys():
        del content['_state']
    content = json.dumps(content, cls=JsonEncoder)
    Trash(obj.__class__.__name__).add(content)
