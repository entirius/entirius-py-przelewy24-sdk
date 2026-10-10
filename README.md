# entirius-py-przelewy24-sdk

A Python client for the Przelewy24 payment gateway REST API, part of Entirius, the open-source modular ecommerce platform.
It registers and verifies transactions, lists payment methods and signs requests behind one `Przelewy24` class.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-przelewy24-sdk.svg)](https://pypi.org/project/entirius-py-przelewy24-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-przelewy24-sdk.svg)](https://pypi.org/project/entirius-py-przelewy24-sdk/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-przelewy24-sdk/blob/develop/LICENSE)

## What it does

- Registers a transaction from a typed `TransactionRequest` DTO (`create_transaction()`).
- Verifies a paid transaction from a `VerifyRequest` DTO (`verify_transaction()`).
- Checks the credentials against the API (`test_access()`).
- Lists the payment methods for a language, amount and currency (`get_payment_methods()`).
- Signs register and verify requests with the CRC key (`calculate_sign()`, `calculate_verify_sign()`).

## Installation

```shell
uv add entirius-py-przelewy24-sdk
pip install entirius-py-przelewy24-sdk
```

The import name is `przelewy24_sdk`.

The SDK reads one Django setting, `PRZELEWY24_CRC_KEY` (the CRC key of the Przelewy24 account, default `None`),
which signs the register and verify requests. It is not a Django app: no `INSTALLED_APPS` entry is needed.

## Quick start

```python
from przelewy24_sdk.services.client import Przelewy24

przelewy24 = Przelewy24(client_id="...", client_secret="...", sandbox=True)
przelewy24.test_access()
```

## Requirements

- Python 3.11 or newer.
- Django 4.2 or newer, with settings configured before the package is imported.
- `requests` and `entirius-py-process-logger` (installed as dependencies).
- A Przelewy24 merchant account (client id, client secret, CRC key); a sandbox account for testing.

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-przelewy24-sdk/blob/develop/CHANGELOG.md

## Part of Entirius

This SDK is one of the payment gateway clients used by the Entirius backend service (Volkanos) and its modules.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Checkout module: https://github.com/entirius/entirius-django-checkout
- Sibling gateway SDKs: https://github.com/entirius/entirius-py-payu-sdk, https://github.com/entirius/entirius-py-autopay-sdk, https://github.com/entirius/entirius-py-paynow-sdk

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: https://github.com/entirius/entirius-py-przelewy24-sdk/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-przelewy24-sdk/blob/develop/LICENSE.
