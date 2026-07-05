# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

CRC_KEY = getattr(settings, "PRZELEWY24_CRC_KEY", None)

API_URL = "https://secure.przelewy24.pl/api/v1"
SANDBOX_API_URL = "https://sandbox.przelewy24.pl/api/v1"

REDIREDCT_URL = "https://secure.przelewy24.pl/trnRequest/"
REDIREDCT_URL_SANDBOX = "https://sandbox.przelewy24.pl/trnRequest/"
