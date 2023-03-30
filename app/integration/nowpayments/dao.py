from tortoise import Model, fields


class NowPayment(Model):
    payment_id = fields.BigIntField(pk=True)
    payment_status = fields.CharField(max_length=10)
    price_amount = fields.DecimalField(max_digits=16, decimal_places=10)
    price_currency = fields.CharField(max_length=3)
    pay_amount = fields.DecimalField(max_digits=16, decimal_places=10)
    pay_currency = fields.CharField(max_length=10)
    user = fields.ForeignKeyField('account.User', on_delete=fields.CASCADE)
    created_at = fields.DatetimeField()
    updated_at = fields.DatetimeField()
