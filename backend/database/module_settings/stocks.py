from tortoise import fields
from tortoise.models import Model


class StocksSettings(Model):
    id = fields.IntField(pk=True)
    tickers = fields.CharField(max_length=250)
