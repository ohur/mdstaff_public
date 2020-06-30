
def get_headers(auth_token):
    auth_token_header_value = "Bearer %s" % auth_token

    headers = {
        "Accept": "application/json",
        "Authorization": auth_token_header_value
    }

    return headers


def main():
    headers = get_headers(auth_token)


if __name__ == "__main__":
    main()
