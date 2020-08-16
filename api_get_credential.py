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
import datetime
from api_authentication import get_auth_token
import api_get_headers
import socket


def get_credential(instance, providerid_list):
    # provider_list list should be passed as a list of mdstaff providerid

    hostname = socket.gethostname().lower().strip()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    today_date = get_today_date_yyyymmdd()
    begin_time_obj = datetime.datetime.now()

    output_file = dir_path + "/data/credential_licnums_" + instance + ".txt"
    log_file = ""
    wkday = get_today_wkday()

    if instance == "inpatient":
        instance = api_const.inpatient_instance
        if hostname == "hhssvninappt001" or hostname == "hhssvninappp001":
            log_file = "C:\\inetpub\\wwwroot\\oscarhur\\" + api_const.inpatient_log_file
        else:
            log_file = dir_path + api_const.inpatient_log_file

    elif instance == "ambulatory":
        instance = api_const.ambulatory_instance
        if hostname == "hhssvninappt001" or hostname == "hhssvninappp001":
            log_file = "C:\\inetpub\\wwwroot\\oscarhur\\" + api_const.ambulatory_log_file
        else:
            log_file = dir_path + api_const.ambulatory_log_file

    providerids_to_licnums_hash = {}
    providerids_to_licexps_hash = {}

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.info, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)

    logger.info(wkday + ". " + instance + ". Starting GET CREDENTIAL API")
    counter = 0

    with open(output_file, "w", newline = '') as output_fh:
        output_writer = csv.writer(output_fh, delimiter = '|')
        output_writer.writerow(["credential_id", "provider_id", "lic_num", "issued_date", \
                               "expiration_date"])

        for providerid in providerid_list:
            api_url = api_const.api_url + instance + "/providers/" + providerid + "/credential"
            logger.debug(wkday + ". " + api_url)

            counter = counter + 1

            # API authentication expires in about 15 minutes
            # So after each 1500 iterations, we will get authentication again
            if (counter % 1500 == 0) or counter == 1:
                auth_token = get_auth_token(instance)
                headers = api_get_headers.get_headers(auth_token)

            try:
                response = requests.get(api_url, headers = headers, timeout = 60)
                response.raise_for_status()

            except requests.exceptions.RequestException as err:
                logger.critical(wkday + ". " + instance + ". OOps: Something Else: " + str(err))
                logger.critical(wkday + ". " + instance + ". " + api_url)


            except requests.exceptions.HTTPError as errh:
                logger.critical(wkday + ". " + instance + ". Http Error: " + errh)
                logger.critical(wkday + ". " + instance + ". " + api_url)


            except requests.exceptions.ConnectionError as errc:
                logger.critical(wkday + ". " + instance + ". Error Connecting: " + errc)
                logger.critical(wkday + ". " + instance + ". " + api_url)


            except requests.exceptions.Timeout as errt:
                logger.critical(wkday + ". " + instance + ". Timeout Error: " + errt)
                logger.critical(wkday + ". " + instance + ". " + api_url)


            logger.debug(wkday + ". Get_credential api return code: " + str(response.status_code))
            response_json = response.json()

            try:
                credential = response_json[0]["CredentialID"]
            except:
                logger.critical(wkday + ". " + instance + ". This Provider ID credential not found: " + providerid)
                continue

            licnum = response_json[0]["LicenseNumber"]
            issued_date = response_json[0]["IssuedText"]
            licexp = response_json[0]["ExpiredText"]

            output_writer.writerow([credential, providerid, licnum, issued_date, licexp])

            providerids_to_licnums_hash[providerid] = licnum
            providerids_to_licexps_hash[providerid] = licexp

    end_time_obj = datetime.datetime.now()
    diff_time = (end_time_obj - begin_time_obj).total_seconds()
    diff_time = int(diff_time)

    logger.info(wkday + ". " + instance + ". Completing all staff licenses data")
    logger.info(wkday + ". " + instance + ".  Creating the table: " + output_file)
    logger.info(wkday + ". " + instance + ".  Run ends.  It took " + str(diff_time) + " second(s) to complete")

    return (providerids_to_licnums_hash, providerids_to_licexps_hash)

def main():
    providerids_to_licnums_hash, providerids_to_licexps_hash = get_credential(instance, providerid_list)


if __name__ == "__main__":
    main()