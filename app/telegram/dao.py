from tortoise import Model, fields


class RedArticleUser(Model):
    user = fields.ForeignKeyField('account.User', on_delete=fields.CASCADE)
    article_title = fields.CharField(max_length=64)
