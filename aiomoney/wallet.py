from pydantic import TypeAdapter
from httpx import AsyncClient

from aiomoney.types import AccountInfo, OperationDetails, Operation, PaymentSource, PaymentForm


class YooMoneyWallet:
    def __init__(self, access_token: str, headers: dict | None = None):
        if headers is None:
            headers = {}

        self.__headers = {
            "Authorization": f"Bearer {access_token}",
            **headers
        }

        self.client = AsyncClient(
            base_url="https://yoomoney.ru",
            headers=self.__headers
        )

    async def close(self):
        await self.client.aclose()

    @property
    async def account_info(self) -> AccountInfo | None:
        url = "/api/account-info"
        response = await self.client.post(url)

        if not response.is_success:
            return

        return AccountInfo.model_validate_json(response.content)

    async def get_operation_details(self, operation_id: str) -> OperationDetails | None:
        url = "/api/operation-details"
        response = await self.client.post(url, data={"operation_id": operation_id})

        if not response.is_success:
            return

        return OperationDetails.model_validate_json(response.content)

    async def get_operation_history(self, records_count: int = 30, **params) -> list[Operation]:
        result = []
        url = "/api/operation-history"
        params = {
            "records": records_count,
            **params
        }
        response = await self.client.post(url, data=params)

        if not response.is_success:
            return result

        data = response.json()
        if operations := data.get("operations"):
            adapter = TypeAdapter(list[Operation])
            result = adapter.validate_python(operations)

        return result

    async def create_payment_form(self,
                                  amount_rub: int,
                                  unique_label: str,
                                  success_redirect_url: str | None = None,
                                  payment_source: PaymentSource = PaymentSource.BANK_CARD
                                  ) -> PaymentForm:
        account_info = await self.account_info
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
        need_operations = await self.get_operation_history(label=label)
        if not need_operations:
            return False

        operation = need_operations[0]
        return operation.status == "success"

    async def revoke_token(self) -> bool:
        url = "/api/revoke"
        response = await self.client.post(url)
        return response.is_success
