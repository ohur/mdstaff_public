import requests
import api_const
import csv
import sys
sys.path.insert(1, '../util/')
sys.path.insert(2, "C:/OscarScripts/util")
from calendar_datetime import get_today_date_yyyymmdd
from calendar_datetime import get_today_wkday
import os
import logging

def put_credential(headers, instance, credentialid_to_providerid_hash, credentialid_to_licnum_hash):
    # credential_data should be passed as a hash of providerID and credentialID,
    # with credentialID as the key
    # lic_data should be passed as a hash of data to be modified and credentialID
    # with credentialID as the key

    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_file = dir_path + api_const.log_file

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". Starting PUT CREDENTIAL API")

    for credential_id, licnum in credentialid_to_licnum_hash.items():
        print(credential_id, licnum)
        provider_id = credentialid_to_providerid_hash[credential_id]
        print(provider_id)

        api_url = api_const.api_url + instance + "/providers/" + provider_id \
                  + "/credential/" + credential_id
        logger.info(wkday + ". " + api_url)

        data = '{"LicenseNumber": "' + licnum + '"}'

        response = requests.put(api_url, headers = headers, data = data)
        logger.info(wkday + ". Put_credential api return code: " + str(response.status_code))
        response_json = response.json()
        logger.info(wkday + ". New license number: " + response_json["LicenseNumber"])


def main():
    put_credential(headers, instance, credentialid_to_providerid_hash, credentialid_to_licnum_hash)

if __name__ == "__main__":
    main()