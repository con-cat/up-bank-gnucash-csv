import app
import datetime


start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 1, 31)
accounts = app.client.accounts()
account = accounts[0]

transactions = app.get_transactions_for_account(
    account,
    start_date=datetime.date(2023, 1, 1),
    end_date=datetime.date(2023, 1, 31),
)

filename = f"{account.name}_{start_date.isoformat()}_{end_date.isoformat()}.csv"

app.write_csv(filename=filename, transactions=transactions)
print(f"CSV written: {filename}")
