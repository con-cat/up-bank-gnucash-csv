from upbankapi import Client, models
import datetime

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

client = Client()


def test():
    try:
        user_id = client.ping()
        print(f"Authorized: {user_id}")
    except upbankapi.NotAuthorizedException:
        print("The token is invalid")


def get_transactions_for_account(
    account: models.Account, start_date: datetime.date, end_date: datetime.date
) -> models.PaginatedList[models.Transaction]:
    since = datetime.datetime.combine(
        start_date,
        datetime.datetime.min.time(),
        tzinfo=LOCAL_TIMEZONE,
    )
    until = datetime.datetime.combine(
        end_date + datetime.timedelta(days=1),
        datetime.datetime.min.time(),
        tzinfo=LOCAL_TIMEZONE,
    )
    return account.transactions(since=since, until=until)
