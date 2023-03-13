from enum import Enum
from tortoise import fields, Model


class TimeEnum(Enum):
    seven = '19:00 по мск'
    three = '15:00 по мск'
    nine = '12:00 по мск'


class User(Model):
    """ Модель юзера бота """

    id = fields.BigIntField(pk=True)
    hash = fields.CharField(max_length=255)
    username = fields.CharField(max_length=1024, null=True)
    full_name = fields.CharField(max_length=1024, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    language_code = fields.CharField(max_length=8, null=True)
    is_admin = fields.BooleanField(default=False)
    email = fields.CharField(max_length=255, null=True)
    phone_number = fields.CharField(max_length=16, null=True)
    webinar_time = fields.CharEnumField(enum_type=TimeEnum, null=True, max_length=1024)
    test_finished = fields.BooleanField(default=False)
    knowledgebase_red = fields.BooleanField(default=False)
    newbie = fields.BooleanField(default=False)
    experienced = fields.BooleanField(default=False)
    coins = fields.IntField(default=0)
    rank = fields.CharField(max_length=10, null=True)
