import argparse
import csv
import datetime
import re

from upbankapi import Client, UpBankException, models

CSV_FIELDNAMES = ["date", "description", "deposit", "withdrawal"]
# TODO: check if Up Bank uses local time or Melbourne time
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo


class CSVExporter:
    def __init__(self) -> None:
        self.client = Client()
        parser = self.get_parser()
        args = parser.parse_args()
        self.start_date = args.start
        self.end_date = args.end
        self.select_account = not args.all_accounts

    def get_parser(self) -> argparse.ArgumentParser:
        """Get parser for command line arguments"""
        parser = argparse.ArgumentParser(
            prog="up-bank-gnucash-csv",
            description="A simple CLI to fetch data from the Up Bank API and output CSVs for GnuCash.",
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
        parser.add_argument(
            "-a",
            "--all-accounts",
            help="Automatically save CSVs for all available accounts",
            required=False,
            default=False,
            action="store_true",
        )
        return parser

    def create_csvs(self) -> None:
        """Write CSVs of transaction data for all accounts"""
        # Make sure we can connect to the API
        try:
            self.client.ping()
        except UpBankException as e:
            print(f"Error connecting to the API: {e}")
            return

        # Query for accounts
        available_accounts = self.client.accounts()
        if self.select_account:
            selected_account = self.prompt_for_account(available_accounts)
            accounts = [selected_account]
        else:
            accounts = available_accounts
            print(f"\n💁‍♀️ Writing CSVs for {len(accounts)} accounts.")

        for account in accounts:
            filename = self.get_filename_for_account(account)
            transactions = self.get_transactions_for_account(account)
            self.write_csv(filename, transactions)
            print(f"    📄 CSV saved: {filename}")

        print("\nAll done 🎉\n")

    def prompt_for_account(
        self, accounts: models.PaginatedList[models.Account]
    ) -> models.Account:
        """Ask the user which account they would like to export"""
        print("\n💁‍♀️ Available accounts:")
        for index, account in enumerate(accounts):
            print(f"    {index}: {account.name}")
        account_index = int(
            input("\nEnter the number next to the account you would like to export: ")
        )
        selected = accounts[account_index]
        print(f"\n💁‍♀️ Writing CSV for {selected.name}")
        return selected

    def get_filename_for_account(self, account: models.Account) -> str:
        """Return a CSV filename for the account and date range"""
        # Remove non-alphanumeric characters from the account name
        account_name = re.sub(r"\W+", "", account.name)
        return f"{account_name}_{self.start_date.isoformat()}_{self.end_date.isoformat()}.csv"

    def get_transactions_for_account(
        self, account: models.Account
    ) -> models.PaginatedList[models.Transaction]:
        since = datetime.datetime.combine(
            self.start_date,
            datetime.datetime.min.time(),
            tzinfo=LOCAL_TIMEZONE,
        )
        until = datetime.datetime.combine(
            self.end_date + datetime.timedelta(days=1),
            datetime.datetime.min.time(),
            tzinfo=LOCAL_TIMEZONE,
        )
        return account.transactions(since=since, until=until)

    def write_csv(
        self, filename: str, transactions: models.PaginatedList[models.Transaction]
    ) -> None:
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            for transaction in transactions:
                row = {
                    "date": transaction.created_at.date(),
                    "description": transaction.description,
                }
                if transaction.amount > 0:
                    row["deposit"] = transaction.amount
                else:
                    row["withdrawal"] = abs(transaction.amount)

                writer.writerow(row)
