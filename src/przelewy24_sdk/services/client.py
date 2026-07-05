# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
from dataclasses import asdict

import requests
from process_logger import ProcessLogger, ProcessLoggerMixin
from requests.auth import HTTPBasicAuth

from przelewy24_sdk import settings
from przelewy24_sdk.dto.payment import TransactionRequest, VerifyRequest
from przelewy24_sdk.utils.sanitize import sanitize
from przelewy24_sdk.validators.exceptions import Przelewy24Error
from przelewy24_sdk.validators.response import (
    validate_przelewy24_access_test,
    validate_przelewy24_auth_success,
    validate_przelewy24_create_transaction,
    validate_przelewy24_get_method,
    validate_przelewy24_response,
)

logger = logging.getLogger(__name__)


class Przelewy24(ProcessLoggerMixin):
    client_id: str
    client_secret: str
    sandbox: bool
    authorization = None

    def __init__(self, client_id: str, client_secret: str, sandbox: bool, authorization=None):
        self.sandbox = sandbox
        self.authorization = authorization
        self.client_id = client_id
        self.client_secret = client_secret

    logger = ProcessLogger("PRZELEWY24_SDK")

    @staticmethod
    def _get_api_url(sandbox):
        if sandbox:
            return settings.SANDBOX_API_URL
        else:
            return settings.API_URL

    def create_transaction(self, transaction_data: TransactionRequest):
        """Creates transaction in przelewy24. If success you will recieve Przelewy24 token to validate transaction"""
        try:
            data = json.dumps(sanitize(asdict(transaction_data)))
            self.logger.add_log_param("request_params", data)
        except Exception:
            self.logger.error("Przelewy24 API response failed on registration")
            logger.error("Przelewy24 API response failed on registration")
            raise Przelewy24Error("Przelewy24 response is not correct.")

        response = requests.request(
            method="POST",
            url=self._get_api_url(self.sandbox) + "/transaction/register",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={"Content-Type": "application/json"},
            data=data,
        )
        validation, response_body = validate_przelewy24_response(response)
        self.logger.add_log_param("response_body", response_body)

        if validation:
            success = validate_przelewy24_auth_success(response_body)
            if success:
                token = response_body["data"]["token"]
                # Przekieruj klienta do panelu transakcyjnego P24
                try:
                    if self.sandbox:
                        redirect_url = settings.REDIREDCT_URL_SANDBOX
                    else:
                        redirect_url = settings.REDIREDCT_URL
                except Exception as e:
                    self.logger.error(e)
                    logger.error(e)
                    raise Przelewy24Error("Przelewy24 redirect_url is not valid")
                redirect_url_panel = f"{redirect_url}{token}"

                return response_body, redirect_url_panel
            else:
                self.logger.error("Przelewy24 API response failed on registration")
                logger.error("Przelewy24 API response failed on registration")
                raise Przelewy24Error("Przelewy24 response is not correct.")
        else:
            self.logger.error("Przelewy24 API response failed")
            logger.error("Przelewy24 API response failed")
            raise Przelewy24Error(f"The Przelewy24 API responded with an error. Message: {response_body.get('error')}")

    def verify_transaction(self, verify_data: VerifyRequest) -> dict:
        """Verify transaction in przelewy24."""
        # Weryfikacja transakcji
        data = json.dumps(asdict(verify_data))
        self.logger.add_log_param("request_params", data)
        response = requests.request(
            method="PUT",
            url=self._get_api_url(self.sandbox) + "/transaction/verify",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={"Content-Type": "application/json"},
            data=data,
        )
        validation, response_body = validate_przelewy24_response(response)
        self.logger.add_log_param("response_body", response_body)
        if validation:
            logger.info(f"success: {response_body}")
            success = validate_przelewy24_create_transaction(response_body)
            logger.info(f"success: {success}")
            if success:
                return response_body
            else:
                self.logger.error(level=1, msg="Przelewy24 API response failed on verification")
                logger.error("Przelewy24 API response failed on verification")
                raise Przelewy24Error("Przelewy24 response is not correct.")
        else:
            self.logger.error(level=1, msg="Przelewy24 API response failed")
            logger.error("Przelewy24 API response failed")
            raise Przelewy24Error(f"The Przelewy24 API responded with an error. Message: {response_body.get('error')}")

    def test_access(self) -> "Przelewy24":
        """Access test in przelewy24."""
        response = requests.request(
            method="GET",
            url=self._get_api_url(self.sandbox) + "/testAccess",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={"Content-Type": "application/json"},
            data={},
        )
        validation, response_body = validate_przelewy24_response(response)
        self.logger.add_log_param("response_body", response_body)
        if validation:
            success = validate_przelewy24_access_test(response_body)
            if success:
                return response_body
            else:
                self.logger.error("Przelewy24 API response failed")
                logger.error("Przelewy24 API response failed")
                raise Przelewy24Error("Przelewy24 response is not correct.")
        else:
            raise Przelewy24Error(f"The Przelewy24 API responded with an error. Message: {response_body.get('error')}")

    def get_payment_methods(self, language, amount, currency):
        params = {"amount": amount, "currency": currency}
        response = requests.request(
            method="GET",
            url=self._get_api_url(self.sandbox) + f"/payment/methods/{language}",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={"Content-Type": "application/json"},
            data=params,
        )
        validation, response_body = validate_przelewy24_response(response)
        if validation:
            success = validate_przelewy24_get_method(response_body)
            if success:
                return response_body
            else:
                self.logger.error("Przelewy24 API payment methods response failed")
                logger.error("Przelewy24 API payment methods response failed")
                raise Przelewy24Error("Przelewy24 payment methods response is not correct.")
        else:
            self.logger.error("Przelewy24 API payment methods response failed")
            logger.error("Przelewy24 API payment methods response failed")
            raise Przelewy24Error(
                f"The Przelewy24 API payment methods responded with an error. Message: {response_body.get('error')}"
            )
