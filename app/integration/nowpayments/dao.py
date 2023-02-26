from tortoise import Model, fields


class Payment(Model):
    payment_id = fields.BigIntField()
    payment_status = fields.CharField(max_length=10)
    price_amount = fields.DecimalField()
    price_currency = fields.CharField(max_length=3)
    pay_amount = fields.DecimalField()
    pay_currency = fields.CharField(max_length=6)
    user_id = fields.ForeignKeyField('account.User', on_delete=fields.CASCADE)
    created_at = fields.DatetimeField()
    updated_at = fields.DatetimeField()
