from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import (
    JSONField as DjangoJSONField,
    ArrayField as DjangoArrayField,
)
import os
import json
import pandas as pd


FILE_NAME_QUESTIONNAIRES = 'db_stub.json'
FILE_NAME_DOMAIN_MAPPING = 'domain_mapping.json'
PATH = 'polls'


class Question(models.Model):
    question_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')
    question_id  = models.CharField(max_length=50)
    domain = models.CharField(max_length=100)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500)
    count = models.IntegerField(default=0)
    value = models.IntegerField()


class Screener(models.Model):
    screen_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    disorder = models.CharField(max_length=100)
    question_id  = models.CharField(max_length=50)


class Assessment(models.Model):
    domain = models.CharField(max_length=100)
    tot_score = models.IntegerField()
    assessment_level_2 = models.CharField(max_length=100)


class JSONField(DjangoJSONField):
    if 'sqlite' in settings.DATABASES['default']['ENGINE']:
        class JSONField(models.Field):
            def db_type(self, connection):
                return 'text'

            def from_db_value(self, value, expression, connection):
                if value is not None:
                    return self.to_python(value)
                return value

            def to_python(self, value):
                if value is not None:
                    try:
                        return json.loads(value)
                    except (TypeError, ValueError):
                        return value
                return value

            def get_prep_value(self, value):
                if value is not None:
                    return str(json.dumps(value))
                return value

            def value_to_string(self, obj):
                return self.value_from_object(obj)


class ArrayField(DjangoArrayField):
    if 'sqlite' in settings.DATABASES['default']['ENGINE']:

        class ArrayField(JSONField):
            def __init__(self, base_field, size=None, **kwargs):
                """Care for DjanroArrayField's kwargs."""
                self.base_field = base_field
                self.size = size
                return super().__init__(**kwargs)

            def deconstruct(self):
                """Need to create migrations properly."""
                name, path, args, kwargs = super().deconstruct()
                kwargs.update({
                    'base_field': self.base_field.clone(),
                    'size': self.size,
                })
                return name, path, args, kwargs


def Diagnostic_Data(path=PATH):

    with open(os.path.join(path, FILE_NAME_QUESTIONNAIRES), "r") as io_text:
      jsn_data = json.load(io_text)

    return [jsn_data]


def Domain_Mapping(path=PATH):
    with open(os.path.join(path, FILE_NAME_DOMAIN_MAPPING), "r") as io_text:
      jsn_data = json.load(io_text)

    domain_mapping = dict()
    for d in jsn_data['domain_mapping']:
        if d['domain'] not in domain_mapping:
           domain_mapping[d['domain']] = {'question_id': [d['question_id']], 'value':0}
        else:
           domain_mapping[d['domain']]['question_id'].append(d['question_id'])
    return domain_mapping


def Diagnostic_Rules():
    rules = {'domain': ['depression','mania','anxiety','substance_use'], 'tot_score': [2,2,2,1],
         'assessment_level_2': ['PHQ-9','ASRM','PHQ-9','ASSIST']}
    df = pd.DataFrame(rules)

    return df
