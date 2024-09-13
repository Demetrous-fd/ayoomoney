from httpx import AsyncClient, Response, Client

from ayoomoney.types import (
    AccountInfo,
    OperationDetails,
    OperationStatus,
    OperationHistory,
    PaymentSource,
    PaymentForm
)


class _BaseWallet:
    BASE_URL = "https://yoomoney.ru"

    def __init__(self, access_token: str, headers: dict | None = None):
        if headers is None:
            headers = {}

        self.__headers = {
            "Authorization": f"Bearer {access_token}",
            **headers
        }

    def _process_account_info(self, response: Response) -> AccountInfo | None:
        if not response.is_success:
            return

        return AccountInfo.model_validate_json(response.content)

    def _process_get_operation_details(self, response: Response) -> OperationDetails | None:
        if not response.is_success:
            return

        return OperationDetails.model_validate_json(response.content)

    def _process_get_operation_history(self, response: Response) -> OperationHistory | None:
        if not response.is_success:
            return

        history = OperationHistory.model_validate_json(response.content)
        return history

    def _process_check_payment_on_successful(self, history: OperationHistory) -> bool:
        if history is None or len(history.operations) <= 0:
            return False

        operation = history.operations[0]
        return operation.status == OperationStatus.SUCCESS


class YooMoneyWallet(_BaseWallet):
    def __init__(self, access_token: str, headers: dict | None = None):
        super(_BaseWallet).__init__(access_token, headers)
        self.client = Client(
            base_url=self.BASE_URL,
            headers=self.__headers
        )

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

    def get_operation_history(self, records_count: int = 30, **params) -> OperationHistory | None:
        url = "/api/operation-history"
        params = {
            "records": records_count,
            **params
        }
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
            "paymentType": payment_source,
            "sum": amount_rub,
            "successURL": success_redirect_url,
            "label": unique_label
        }
        params = {k: v for k, v in params.items() if v}
        response = self.client.post(url, params=params)

        return PaymentForm(
            link_for_customer=str(response.url),
            payment_label=unique_label
        )

    def check_payment_on_successful(self, label: str) -> bool:
        history = self.get_operation_history(label=label)
        return self._process_check_payment_on_successful(history)

    def revoke_token(self) -> bool:
        url = "/api/revoke"
        response = self.client.post(url)
        return response.is_success


class YooMoneyWalletAsync(_BaseWallet):
    def __init__(self, access_token: str, headers: dict | None = None):
        super(_BaseWallet).__init__(access_token, headers)
        self.client = AsyncClient(
            base_url=self.BASE_URL,
            headers=self.__headers
        )

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

    async def get_operation_history(self, records_count: int = 30, **params) -> OperationHistory | None:
        url = "/api/operation-history"
        params = {
            "records": records_count,
            **params
        }
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
            "paymentType": payment_source,
            "sum": amount_rub,
            "successURL": success_redirect_url,
            "label": unique_label
        }
        params = {k: v for k, v in params.items() if v}
        response = await self.client.post(url, params=params)

        return PaymentForm(
            link_for_customer=str(response.url),
            payment_label=unique_label
        )

    async def check_payment_on_successful(self, label: str) -> bool:
        history = await self.get_operation_history(label=label)
        return self._process_check_payment_on_successful(history)

    async def revoke_token(self) -> bool:
        url = "/api/revoke"
        response = await self.client.post(url)
        return response.is_success
