from datetime import datetime
from decimal import Decimal
from typing import Literal
from hashlib import sha1

from pydantic import BaseModel, Field, field_serializer

from .enums import NotificationType
from .utils import convert_datetime_to_iso_8601


class NotificationBase(BaseModel):
    notification_type: NotificationType = Field(...)
    operation_id: str = Field(...)
    amount: Decimal = Field(..., decimal_places=2)
    withdraw_amount: Decimal | None = Field(None, decimal_places=2)
    currency: Literal["643"] = Field(...)
    execution_datetime: datetime = Field(..., alias="datetime")
    sender: str = Field(default="")
    codepro: bool = Field(...)
    label: str = Field(default="")
    sha1_hash: str = Field(...)
    test_notification: bool | None = Field(default=None)
    unaccepted: bool = Field(default=False)

    @field_serializer("execution_datetime")
    def convert_datetime_to_iso8601(self, v: datetime, _info) -> str:
        return convert_datetime_to_iso_8601(v, True)

    @field_serializer("codepro")
    def convert_bool_for_correct_hashing(self, v: bool, _info) -> str:
        return str(v).lower()

    def check_sha1_hash(self, notification_secret: str) -> bool:
        result_string = "&".join([
            self.notification_type,
            self.operation_id,
            str(self.amount),
            self.currency,
            convert_datetime_to_iso_8601(self.execution_datetime, True).replace(".000+00:00", "Z"),
            self.sender,
            f"{self.codepro}".lower(),
            notification_secret,
            self.label,
        ])
        hash_string = sha1(result_string.encode("utf8"))
        hash_string = hash_string.hexdigest()
        return self.sha1_hash == hash_string


class NotificationExtend(NotificationBase):
    lastname: str | None = Field(default=None)
    firstname: str | None = Field(default=None)
    fathersname: str | None = Field(default=None)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    city: str | None = Field(default=None)
    street: str | None = Field(default=None)
    building: str | None = Field(default=None)
    suite: str | None = Field(default=None)
    flat: str | None = Field(default=None)
    zip: str | None = Field(default=None)
