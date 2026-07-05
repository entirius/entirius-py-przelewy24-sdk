# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import hashlib
import json

from przelewy24_sdk import settings


def calculate_sign(session_id, merchant_id, amount, currency, crc_key: str = settings.CRC_KEY) -> str:
    # sprawdzanie klucza CRC
    if not crc_key:
        raise ValueError("CRC_KEY is not set. Set PRZELEWY24_CRC_KEY in settings.py file.")
    # Tworzenie słownika z parametrami
    params = {
        "sessionId": session_id,
        "merchantId": merchant_id,
        "amount": amount,
        "currency": currency,
        "crc": crc_key,
    }

    # Konwersja słownika na JSON z dodatkowymi atrybutami
    json_data = json.dumps(params, ensure_ascii=False, separators=(",", ":")).replace(" ", "")

    # Obliczanie sumy kontrolnej SHA384
    return hashlib.sha384(json_data.encode("utf-8")).hexdigest()


def calculate_verify_sign(
    session_id: str, order_id: int, amount: int, currency: str, crc_key: str = settings.CRC_KEY
) -> str:
    # sprawdzanie klucza CRC
    if not crc_key:
        raise ValueError("CRC_KEY is not set. Set PRZELEWY24_CRC_KEY in settings.py file.")
    # Tworzenie słownika z parametrami
    params = {
        "sessionId": session_id,
        "orderId": order_id,
        "amount": amount,
        "currency": currency,
        "crc": crc_key,
    }

    # Konwersja słownika na JSON z dodatkowymi atrybutami
    json_data = json.dumps(params, ensure_ascii=False, separators=(",", ":")).replace(" ", "")

    # Obliczanie sumy kontrolnej SHA384
    return hashlib.sha384(json_data.encode("utf-8")).hexdigest()
