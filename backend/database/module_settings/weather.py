from tortoise import fields
from tortoise.models import Model


class WeatherSettings(Model):
    id = fields.IntField(pk=True)
    scale = fields.CharField(max_length=1)
    zipcode = fields.CharField(max_length=5)
    timezone = fields.CharField(max_length=30)
