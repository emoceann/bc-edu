from tortoise import Model, fields


class Payment(Model):
    payment_id = fields.BigIntField()
    payment_status = fields.CharField(max_length=10)
    price_amount = fields.DecimalField(max_digits=16, decimal_places=2)
    price_currency = fields.CharField(max_length=3)
    pay_amount = fields.DecimalField(max_digits=16, decimal_places=2)
    pay_currency = fields.CharField(max_length=6)
    user_id = fields.ForeignKeyField('account.User', on_delete=fields.CASCADE)
    created_at = fields.DatetimeField()
    updated_at = fields.DatetimeField()
