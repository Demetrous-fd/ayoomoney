from datetime import datetime
from os import environ

from ayoomoney.types import OperationHistoryParams, OperationHistoryParamType
from ayoomoney.wallet import YooMoneyWalletAsync


async def main():
    async with YooMoneyWalletAsync(access_token=environ.get("ACCESS_TOKEN")) as wallet:
        payments_from = datetime.strptime("15.09.2024", "%d.%m.%Y")
        params = OperationHistoryParams(
            # label="lazydeus-1",  # Получение определенного платежа по метке

            from_datetime=payments_from,  # Получение операций после 15.09.2024 00:00
            # till_datetime=payments_from  # Получение операций до 15.09.2024 00:00

            operation_type=["deposition", OperationHistoryParamType.PAYMENT],
            # Типы операций, можно использовать OperationHistoryParamType или вводить значения вручную

            records=3,  # limit, Количество операций за один запрос, по умолчанию 30
            start_record=0,  # offset, https://yoomoney.ru/docs/wallet/user-account/operation-history#filtering-logic

            details=True  # Показывать подробные детали операции. types.Operation -> types.OperationDetails
        )
        history = await wallet.get_operation_history(params)
        for operation in history.operations:
            print(type(operation), operation)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
