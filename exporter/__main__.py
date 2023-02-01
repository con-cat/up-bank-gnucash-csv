import app
import datetime


accounts = app.client.accounts()
account = accounts[0]

transactions = app.get_transactions_for_account(
    account,
    start_date=datetime.date(2023, 1, 1),
    end_date=datetime.date(2023, 1, 31),
)

for transaction in transactions:
    print(transaction)
