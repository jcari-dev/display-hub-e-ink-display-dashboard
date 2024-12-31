from tortoise import fields
from tortoise.models import Model


class TrafficSettings(Model):
    id = fields.IntField(pk=True)
    zipcode = fields.CharField(max_length=250)
    accident = fields.BooleanField()
    fog = fields.BooleanField()
    dangerous_conditions = fields.BooleanField()
    rain = fields.BooleanField()
    ice = fields.BooleanField()
    jam = fields.BooleanField()
    lane_closed = fields.BooleanField()
    road_closed = fields.BooleanField()
    heavy_traffic = fields.BooleanField()
    road_works = fields.BooleanField()
    narrow_lanes = fields.BooleanField()
    tow_trucks = fields.BooleanField()
    other = fields.BooleanField()
