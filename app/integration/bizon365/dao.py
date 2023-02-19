from tortoise import fields, models


class WebinarRoom(models.Model):
    """ Комнаты """
    id = fields.CharField(pk=True, max_length=1024)
    title = fields.CharField(max_length=2048)
    is_autowebinar = fields.BooleanField()
    closest_date = fields.DatetimeField(null=True)
