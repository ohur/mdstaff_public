
def put_headers(auth_token):
    auth_token_header_value = "Bearer %s" % auth_token

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": auth_token_header_value
    }

    return headers


def main():
    put_headers(auth_token)


if __name__ == "__main__":
    main()