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

def get_credential(headers, instance, provider_list):
    # provider_list list should be passed as a list of mdstaff providerid

    dir_path = os.path.dirname(os.path.realpath(__file__))
    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()

    log_file = dir_path + api_const.log_file
    output_file = dir_path + "/data/credential_id_table_" + instance + \
                  ".txt"

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.info, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)

    logger.info(wkday + ". Starting GET CREDENTIAL API")

    with open(output_file, "w", newline = '') as output_fh:
        output_writer = csv.writer(output_fh, delimiter = '|')
        output_writer.writerow(["credential_id", "provider_id"])
        credentialids = {}

        for mdstaff_id in provider_list:
            api_url = mdstaff_api_const.api_url + instance + "/providers/" + mdstaff_id + "/credential"
            logger.info(wkday + ". " + api_url)

            try:
                response = requests.get(api_url, headers = headers, timeout = 60)
                response.raise_for_status()

            except requests.exceptions.RequestException as err:
                logging.critical(wkday + ". OOps: Something Else: " + str(err))
                logging.critical(wkday + ". " + api_url)
                

            except requests.exceptions.HTTPError as errh:
                logging.critical(wkday + ". Http Error: " + errh)
                logging.critical(wkday + ". " + api_url)
                

            except requests.exceptions.ConnectionError as errc:
                logging.critical(wkday + ". Error Connecting: " + errc)
                logging.critical(wkday + ". " + api_url)
                

            except requests.exceptions.Timeout as errt:
                logging.critical(wkday + ". Timeout Error: " + errt)
                logging.critical(wkday + ". " + api_url)
                

            logger.debug(wkday + ". Get_credential api return code: " + str(response.status_code))
            response_json = response.json()

            try:
                credential = response_json[0]["CredentialID"]
            except:
                logger.critical(wkday + ". This Provider ID credential not found: " + mdstaff_id)
                continue

            provider_id = response_json[0]["ProviderID"]
            output_writer.writerow([credential, provider_id])


            providerids_to_credentialids_hash[mdstaff_id] = credential

    return (providerids_to_credentialids_hash)

def main():
    providerids_to_credentialids_hash = get_credential(headers, instance, provider_list)


if __name__ == "__main__":
    main()