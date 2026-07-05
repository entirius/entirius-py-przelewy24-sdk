# przelewy24-sdk

Przelewy24 payment gateway SDK — transaction registration and verification over the Przelewy24 REST API.

## Installation

```shell
pip install entirius-py-przelewy24-sdk
```

Reads `PRZELEWY24_CRC_KEY` from Django settings.

## Usage

```python
from przelewy24_sdk.services.client import Przelewy24

przelewy24 = Przelewy24(...)
```

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
