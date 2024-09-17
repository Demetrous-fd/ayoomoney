from types import TracebackType
from typing import Self, Type

from httpx import AsyncClient, Response, Client

from ayoomoney.types import (
    AccountInfo,
    OperationDetails,
    OperationStatus,
    OperationHistory,
    PaymentSource,
    PaymentForm,
    OperationHistoryParams
)
import ayoomoney


class _BaseWallet:
    BASE_URL = "https://yoomoney.ru"

    def __init__(self, access_token: str, headers: dict | None = None):
        if headers is None:
            headers = {}

        self._headers = {
            "Authorization": f"Bearer {access_token}",
            **headers
        }

    def _process_account_info(self, response: Response) -> AccountInfo | None:
        if not response.is_success:
            if response.status_code == 401:
                raise ayoomoney.errors.InvalidTokenError
            return

        return AccountInfo.model_validate_json(response.content)

    def _process_get_operation_details(self, response: Response) -> OperationDetails | None:
        if not response.is_success:
            if response.status_code == 401:
                raise ayoomoney.errors.InvalidTokenError
            return

        return OperationDetails.model_validate_json(response.content)

    def _process_get_operation_history(self, response: Response) -> OperationHistory | None:
        if not response.is_success:
            if response.status_code == 401:
                raise ayoomoney.errors.InvalidTokenError
            return

        history = OperationHistory.model_validate_json(response.content)
        return history

    def _process_create_payment_form(self, unique_label: str, response: Response) -> PaymentForm:
        if response.status_code == 401:
            raise ayoomoney.errors.InvalidTokenError

        return PaymentForm(
            link_for_customer=str(response.url),
            payment_label=unique_label
        )

    def _process_check_payment_on_successful(self, history: OperationHistory) -> bool:
        if history is None or len(history.operations) <= 0:
            return False

        operation = history.operations[0]
        return operation.status == OperationStatus.SUCCESS


class YooMoneyWallet(_BaseWallet):
    def __init__(self, access_token: str, headers: dict | None = None):
        super().__init__(access_token, headers)
        self.client = Client(
            base_url=self.BASE_URL,
            headers=self._headers
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        self.close()

    def close(self):
        self.client.close()

    def account_info(self) -> AccountInfo | None:
        url = "/api/account-info"
        response = self.client.post(url)
        return self._process_account_info(response)

    def get_operation_details(self, operation_id: str) -> OperationDetails | None:
        url = "/api/operation-details"
        response = self.client.post(url, data={"operation_id": operation_id})
        return self._process_get_operation_details(response)

    def get_operation_history(self, params: OperationHistoryParams | None = None) -> OperationHistory | None:
        if params is None:
            params = OperationHistoryParams()

        url = "/api/operation-history"
        params = params.model_dump(exclude_none=True, by_alias=True)
        response = self.client.post(url, data=params)
        return self._process_get_operation_history(response)

    def create_payment_form(
            self,
            amount_rub: int,
            unique_label: str,
            success_redirect_url: str | None = None,
            payment_source: PaymentSource = PaymentSource.BANK_CARD
    ) -> PaymentForm:
        account_info = self.account_info()
        url = "/quickpay/confirm.xml"
        params = {
            "receiver": account_info.account,
            "quickpay-form": "button",
            "paymentType": payment_source.value,
            "sum": amount_rub,
            "successURL": success_redirect_url,
            "label": unique_label
        }
        params = {k: v for k, v in params.items() if v}
        response = self.client.post(url, params=params)
        return self._process_create_payment_form(unique_label, response)

    def check_payment_on_successful(self, label: str) -> bool:
        params = OperationHistoryParams(label=label)
        history = self.get_operation_history(params)
        return self._process_check_payment_on_successful(history)

    def revoke_token(self) -> bool:
        url = "/api/revoke"
        response = self.client.post(url)
        return response.is_success


class YooMoneyWalletAsync(_BaseWallet):
    def __init__(self, access_token: str, headers: dict | None = None):
        super().__init__(access_token, headers)
        self.client = AsyncClient(
            base_url=self.BASE_URL,
            headers=self._headers
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        await self.close()

    async def close(self):
        await self.client.aclose()

    async def account_info(self) -> AccountInfo | None:
        url = "/api/account-info"
        response = await self.client.post(url)
        return self._process_account_info(response)

    async def get_operation_details(self, operation_id: str) -> OperationDetails | None:
        url = "/api/operation-details"
        response = await self.client.post(url, data={"operation_id": operation_id})
        return self._process_get_operation_details(response)

    async def get_operation_history(self, params: OperationHistoryParams | None = None) -> OperationHistory | None:
        if params is None:
            params = OperationHistoryParams()

        url = "/api/operation-history"
        params = params.model_dump(exclude_none=True, by_alias=True)
        response = await self.client.post(url, data=params)
        return self._process_get_operation_history(response)

    async def create_payment_form(
            self,
            amount_rub: int,
            unique_label: str,
            success_redirect_url: str | None = None,
            payment_source: PaymentSource = PaymentSource.BANK_CARD
    ) -> PaymentForm:
        account_info = await self.account_info()
        url = "/quickpay/confirm.xml"
        params = {
            "receiver": account_info.account,
            "quickpay-form": "button",
            "paymentType": payment_source.value,
            "sum": amount_rub,
            "successURL": success_redirect_url,
            "label": unique_label
        }
        params = {k: v for k, v in params.items() if v}
        response = await self.client.post(url, params=params)
        return self._process_create_payment_form(unique_label, response)

    async def check_payment_on_successful(self, label: str) -> bool:
        params = OperationHistoryParams(label=label)
        history = await self.get_operation_history(params)
        return self._process_check_payment_on_successful(history)

    async def revoke_token(self) -> bool:
        url = "/api/revoke"
        response = await self.client.post(url)
        return response.is_success
