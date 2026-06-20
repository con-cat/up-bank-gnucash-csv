import argparse
import datetime

from .app import CSVExporter


def get_parser() -> argparse.ArgumentParser:
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


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    exporter = CSVExporter(
        start_date=args.start,
        end_date=args.end,
        all_accounts=args.all_accounts,
    )
    exporter.create_csvs()