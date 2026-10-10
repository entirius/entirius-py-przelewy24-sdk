# AGENTS.md

Przelewy24 payment gateway SDK — distribution `entirius-py-przelewy24-sdk`, import `przelewy24_sdk`.

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the import package `przelewy24_sdk` — it is a public API contract.
- Default: do not commit — git is the user's call.
- No AI attribution in commits or PR descriptions.

## Architecture

`src/przelewy24_sdk/`: `services/client.py` holds the `Przelewy24` client (register and verify a transaction,
access test, payment methods) over the Przelewy24 REST API; signing lives in `utils/sign.py`, DTOs in `dto/`,
response checks in `validators/`. `settings.py` reads Django settings (`django.conf`) at import and holds the
public API URLs. Runtime dependencies: `requests`, `django`, `entirius-py-process-logger`.
Tests configure a minimal Django in `tests/conftest.py`.

## Settings

Read from Django settings in `settings.py`.

| Setting | Default | Meaning |
|---|---|---|
| `PRZELEWY24_CRC_KEY` | `None` | CRC key of the Przelewy24 account; signs register and verify requests (signing raises `ValueError` without it) |
