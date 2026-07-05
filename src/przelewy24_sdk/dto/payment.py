# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import asdict, dataclass, is_dataclass
from decimal import Decimal


@dataclass
class DTO:
    def to_dict(self):
        return asdict(self, dict_factory=lambda x: x.to_dict() if is_dataclass(x) else x)


@dataclass
class Shipping(DTO):
    type: int
    address: str
    zip: str
    city: str
    country: str


@dataclass
class Additional(DTO):
    shipping: Shipping


@dataclass
class Cart(DTO):
    sellerId: str
    sellerCategory: str
    name: str | None = None
    description: str | None = None
    quantity: Decimal = Decimal(0)
    price: Decimal = Decimal(0)
    number: str | None = None


@dataclass
class TransactionRequest(DTO):
    merchantId: int
    posId: int
    sessionId: str
    amount: int
    currency: str
    description: str
    email: str
    country: str
    language: str
    urlReturn: str
    sign: str
    client: str | None = None
    address: str | None = None
    zip: str | None = None
    city: str | None = None
    phone: str | None = None
    method: int | None = None
    urlStatus: str | None = None
    timeLimit: int | None = None
    channel: int | None = None
    waitForResult: bool = None
    regulationAccept: bool = None
    shipping: int | None = None
    transferLabel: str | None = None
    mobileLib: int | None = None
    sdkVersion: str | None = None
    encoding: str | None = None
    methodRefId: str | None = None
    cart: list[Cart] = None
    additional: Additional | None = None


@dataclass
class VerifyRequest(DTO):
    merchantId: int
    posId: int
    sessionId: str
    amount: int
    currency: str
    orderId: int
    sign: str
