# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging

from requests import Response

logger = logging.getLogger(__name__)


def validate_przelewy24_response(response: Response) -> (bool, dict):
    response_body = json.loads(response.text)

    if response.status_code == 200:
        return True, response_body

    if response.status_code == 400:
        validation, error_message = validate_przelewy24_response_body_when_error(response_body)
        if validation:
            logger.error(error_message)
            raise ValueError(error_message)

    if response.status_code == 401:
        validation, error_message = validate_przelewy24_response_body_when_error(response_body)
        if validation:
            logger.error(error_message)
            raise ConnectionError(error_message)

    if response.status_code == 403:
        validation, error_message = validate_przelewy24_response_body_when_error(response_body)
        if validation:
            logger.error(error_message)
            raise PermissionError(error_message)

    if response.status_code == 404:
        validation, error_message = validate_przelewy24_response_body_when_error(response_body)
        if validation:
            logger.error(error_message)
            raise ValueError(error_message)

    if response.status_code == 500:
        validation, error_message = validate_przelewy24_response_body_when_error(response_body)
        if validation:
            logger.error(error_message)
            raise SystemError(error_message)

    return False, response_body


def validate_przelewy24_response_body_when_error(response_body: dict) -> (bool, str):
    if "error" in response_body and "code" in response_body:
        error_message = [response_body["error"]]
        code = response_body["code"] if "code" in response_body else ""
        if code != "":
            error_message.append(str(code))
        details = response_body["details"] if "details" in response_body else {}
        error_message.append(f"details: {details}")
        return True, " | ".join(error_message)
    return False, ""


def validate_przelewy24_auth_success(response_body: dict) -> bool:
    if "data" in response_body and "token" in response_body["data"]:
        return True
    return False


def validate_przelewy24_access_test(response_body: dict) -> bool:
    if "data" in response_body and response_body["data"] is True:
        return True
    return False


def validate_przelewy24_get_method(response_body: dict) -> bool:
    if "data" in response_body and response_body["data"]:
        return True
    return False


def validate_przelewy24_create_transaction(response_body: dict) -> bool:
    if "data" in response_body and "status" in response_body["data"] and response_body["data"]["status"] == "success":
        return True
    return False


def validate_przelewy24_get_transaction(response_body: dict) -> bool:
    if "id" in response_body and "status" in response_body:
        return True
    return False
