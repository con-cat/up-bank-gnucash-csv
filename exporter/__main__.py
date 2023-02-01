import app
import argparse
import datetime


parser = argparse.ArgumentParser(
    prog="up-bank-gnucash-csv",
    description="Export transactions from Up Bank as CSVs formatted for GnuCash",
)
parser.add_argument(
    "--start",
    type=datetime.date.fromisoformat,
    help="Start date to query, YYYY-MM-DD format",
    required=True,
)
parser.add_argument(
    "--end",
    type=datetime.date.fromisoformat,
    help="End date to query, YYYY-MM-DD format",
    required=True,
)


def write_csvs() -> None:
    args = parser.parse_args()
    try:
        app.client.ping()
    except upbankapi.UpBankException as e:
        print(f"Error connecting to the API: {e}")
        return

    accounts = app.client.accounts()
    print(f"💁‍♀️ Writing CSVs for {len(accounts)} accounts.")

    for account in accounts:
        transactions = app.get_transactions_for_account(
            account,
            start_date=args.start,
            end_date=args.end,
        )
        # TODO: account name in filename: strip out emojis and replace spaces
        filename = f"{account.name}_{args.start.isoformat()}_{args.end.isoformat()}.csv"
        app.write_csv(filename=filename, transactions=transactions)
        print(f"📄 CSV written: {filename}")

    print("All done 🎉")


write_csvs()
