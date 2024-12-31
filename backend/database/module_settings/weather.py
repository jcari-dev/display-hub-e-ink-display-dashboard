from tortoise import fields
from tortoise.models import Model


class WeatherSettings(Model):
    id = fields.IntField(pk=True)
    scale = fields.CharField(max_length=1,
                             choices=[
                                 ("C", "Celsius"),
                                 ("F", "Fahrenheit"),
                                 ("K", "Kelvin")
                             ])
    zipcode = fields.CharField(max_length=5)
    timezone = fields.CharField(
        max_length=30,
        choices=[
            ("America/Anchorage", "America/Anchorage"),
            ("America/Los_Angeles", "America/Los_Angeles"),
            ("America/Denver", "America/Denver"),
            ("America/Chicago", "America/Chicago"),
            ("America/New_York", "America/New_York"),
            ("America/Sao_Paulo", "America/Sao_Paulo"),
            ("Not set (GMT+0)", "Not set (GMT+0)"),
            ("GMT+0", "GMT+0"),
            ("Automatically detect time zone", "Automatically detect time zone"),
            ("Europe/London", "Europe/London"),
            ("Europe/Berlin", "Europe/Berlin"),
            ("Europe/Moscow", "Europe/Moscow"),
            ("Africa/Cairo", "Africa/Cairo"),
            ("Asia/Bangkok", "Asia/Bangkok"),
            ("Asia/Singapore", "Asia/Singapore"),
            ("Asia/Tokyo", "Asia/Tokyo"),
            ("Australia/Sydney", "Australia/Sydney"),
            ("Pacific/Auckland", "Pacific/Auckland"),
        ]
    )
