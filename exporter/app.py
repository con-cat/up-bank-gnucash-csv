import upbankapi

client = upbankapi.Client()


def test():
    try:
        user_id = client.ping()
        print(f"Authorized: {user_id}")
    except upbankapi.NotAuthorizedException:
        print("The token is invalid")
