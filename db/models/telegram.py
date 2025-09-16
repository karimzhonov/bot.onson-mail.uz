from typing import Any

from tortoise import Model, fields, BaseDBAsyncClient
from tortoise.models import MODEL
from config import REFERRAL_AMOUNT


class TelegramUser(Model):
    id = fields.BigIntField(primary_key=True)
    auth_date = fields.BigIntField(null=True)
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    hash = fields.TextField()
    username = fields.CharField(max_length=255, null=True)
    balance = fields.FloatField(default=0)

    def __str__(self):
        return str(self.username or self.id)

    async def operation_referral(self):
        await BalanceHistory.create(
            user=self,
            amount=REFERRAL_AMOUNT,
            text='Рефералная программа'
        )


class BalanceHistory(Model):
    id = fields.IntField(primary_key=True)
    amount = fields.FloatField()
    create_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField('telegram.TelegramUser')
    text = fields.CharField(max_length=255)


class ReferralLink(Model):
    id = fields.IntField(primary_key=True)
    owner = fields.ForeignKeyField('telegram.TelegramUser')
    user_id = fields.IntField(unique=True)

    @classmethod
    async def create(
        cls: type[MODEL], using_db: BaseDBAsyncClient | None = None, **kwargs: Any
    ) -> MODEL:
        instance = await super().create(using_db, **kwargs)
        await instance.owner.operation_referral()
        return instance