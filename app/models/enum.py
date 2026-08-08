from enum import Enum


class PaymentStatusEnum(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class CurrencyEnum(str, Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
