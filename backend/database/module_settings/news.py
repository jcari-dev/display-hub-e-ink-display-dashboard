from tortoise import fields
from tortoise.models import Model


class NewsSettings(Model):
    id = fields.IntField(pk=True)
    language = fields.CharField(max_length=15)
