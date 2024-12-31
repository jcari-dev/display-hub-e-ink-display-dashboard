from tortoise import fields
from tortoise.models import Model


class EmailSettings(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=250)
