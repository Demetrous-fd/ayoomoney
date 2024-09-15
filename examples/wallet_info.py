from os import environ

from ayoomoney.types import AccountInfo, OperationHistory, OperationDetails
from ayoomoney.wallet import YooMoneyWalletAsync


async def main():
    async with YooMoneyWalletAsync(access_token=environ.get("ACCESS_TOKEN")) as wallet:
        account_info: AccountInfo = await wallet.account_info()
        """
        account='4100116938791262' balance=small =) currency='643' account_status='identified'
        account_type='personal' balance_details=BalanceDetail(total=X, available=X,
        deposition_pending=None, blocked=None, debt=None, hold=None) cards_linked=None
        """

        operation_history: OperationHistory = await wallet.get_operation_history()
        """
        [Operation(operation_id='000000', status='success',
        execution_datetime=datetime.datetime(2023, 3, 9, 13, 15, 10, tzinfo=datetime.timezone.utc),
        title='Пополнение с карты ****0000', pattern_id=None, direction='in',
        amount=00, label='000000', operation_type='deposition'), ...]
        """

        operation_details: OperationDetails = await wallet.get_operation_details(operation_id="000")
        """
        OperationDetails(amount=42, amount_due=None, error=None, operation_id='042', direction=<OperationDirection.IN: 'in'>,
        status=<OperationStatus.SUCCESS: 'success'>, pattern_id=None, fee=None, title='Пополнение с карты ****0000',
        sender=None, recipient=None, recipient_type=None, message=None, comment=None, codepro=None,
        label='unique-42', details='Пополнение с банковской карты, операция №42.\nБанковская карта: ****0000.',
        digital_goods=None, operation_type=<OperationType.DEPOSITION: 'deposition'>, 
        execution_datetime=datetime.datetime(2024, 9, 15, 0, 0, 0, tzinfo=TzInfo(UTC)))
        """


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
