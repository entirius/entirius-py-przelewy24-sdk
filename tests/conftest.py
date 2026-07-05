# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

# przelewy24_sdk.settings reads CRC_KEY from Django settings at import time;
# configure a minimal Django so the package imports in tests / CI.
if not settings.configured:
    settings.configure(PRZELEWY24_CRC_KEY="test-crc-key")
