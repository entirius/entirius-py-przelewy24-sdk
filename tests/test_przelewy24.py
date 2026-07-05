# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from przelewy24_sdk.services.client import Przelewy24


def test_import():
    assert Przelewy24.__name__ == "Przelewy24"
