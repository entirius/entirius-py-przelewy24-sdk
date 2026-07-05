# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from decimal import Decimal


def sanitize(obj) -> dict:
    # convert Decimals to strings
    if isinstance(obj, dict):
        for key, elem in obj.items():
            obj[key] = sanitize(elem)
        return obj
    elif isinstance(obj, list):
        for idx, elem in enumerate(obj):
            obj[idx] = sanitize(elem)
        return obj
    elif isinstance(obj, Decimal):
        return str(obj)
    else:
        return obj
