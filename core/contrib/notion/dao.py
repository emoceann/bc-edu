from tortoise import Model, fields


class CommentsNotion(Model):
    page_id = fields.UUIDField(pk=True)
    comment_id = fields.UUIDField()
    message = fields.CharField(max_length=2048)
    user_email = fields.ForeignKeyField('account.User', to_field='email', on_delete=fields.CASCADE)
