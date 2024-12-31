from tortoise import fields
from tortoise.models import Model


class DisplaySettings(Model):
    id = fields.IntField(pk=True)
    refresh_rate = fields.IntField()
