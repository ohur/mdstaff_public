import mdstaff_api_authentication
import mdstaff_api_get_get_headers
import mdstaff_api_get_post_headers
import mdstaff_api_get_providers
import mdstaff_api_get_demographic

def main():    
    auth_token = mdstaff_api_authentication.get_auth_token()
    headers = mdstaff_api_get_get_headers.get_get_headers(auth_token)
    #provider_list = mdstaff_api_get_providers.get_providers(headers)
    #mdstaff_api_get_demographic.get_demographic(headers, provider_list)

if __name__ == "__main__":
    main()

