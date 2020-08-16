import requests
import api_const
import sys
sys.path.insert(1, '..\\util')
sys.path.insert(2, "C:\\OscarScripts\\util")
from calendar_datetime import get_today_date_yyyymmdd
from calendar_datetime import get_today_wkday
import logging
import os
import csv
import datetime
import re
from api_authentication import get_auth_token
import api_get_headers
import socket


def get_demographic(instance, providerid_list):
    # provider_list is passed as a list of providerID from MDStaff

    providerids_to_names_hash = {}
    providerids_to_sccuids_hash = {}

    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()
    begin_time_obj = datetime.datetime.now()
    
    hostname = socket.gethostname().lower().strip()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_file = ""
    output_file = dir_path + "/data/demographic_providerids_" + instance + ".txt"
        
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

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.info, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". " + instance + ". Starting Get Demographic API.")

    with open(output_file, "w", newline = '') as output_fh:
        output_writer = csv.writer(output_fh, delimiter = '|')
        output_writer.writerow(["provider_id", "vmcid", "name", "email_addr"])

        logger.info(wkday + ". " + instance + ". Getting each staff demographic data")

        counter = 0
        for providerid in providerid_list:
            api_url = api_const.api_url + "/" + instance + "/demographic/" + providerid
            counter = counter + 1
            logger.debug(wkday + ". " + instance + ". API URL: " + api_url)

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
                continue

            except requests.exceptions.HTTPError as errh:
                logger.critical(wkday + ". " + instance + ". Http Error: " + errh)
                logger.critical(wkday + ". " + instance + ". " + api_url)
                continue

            except requests.exceptions.ConnectionError as errc:
                logger.critical(wkday + ". " + instance + ". Error Connecting: " + errc)
                logger.critical(wkday + ". " + instance + ". " + api_url)
                continue

            except requests.exceptions.Timeout as errt:
                logger.critical(wkday + ". " + instance + ". Timeout Error: " + errt)
                logger.critical(wkday + ". " + instance + ". " + api_url)
                continue

            response_json = response.json()
            name = response_json["FormattedName"]
            sccuid = response_json["OtherID"]
            email_addr = response_json["Email"]

            if sccuid == None:
                logger.critical(wkday + ". " + instance + ". " + name + " SCCUID is not found in MDStaff")
            else:
                sccuid = sccuid.strip()

            providerids_to_names_hash[providerid] = name
            providerids_to_sccuids_hash[providerid] = sccuid
            logger.debug(wkday + ". " + instance + ". Get demographics. " + ". " \
                         + providerids_to_names_hash[providerid])

            output_writer.writerow([providerid, str(sccuid), name, email_addr])

    logger.info(wkday + ". " + instance + ".  Creating the table: " + output_file)

    end_time_obj = datetime.datetime.now()
    diff_time = (end_time_obj - begin_time_obj).total_seconds()
    diff_time = int(diff_time)
    logger.info(wkday + ". " + instance + ". Completing all staff demographic data")
    logger.info(wkday + ". " + instance + ".  Run ends.  It took " + str(diff_time) + " second(s) to complete")

    return providerids_to_sccuids_hash, providerids_to_names_hash



def main():
    providerids_to_sccids_hash, providerids_to_names_hash = \
         get_demographic(instance, providerid_list)


if __name__ == "__main__":
    main()