import requests
import api_const
import sys
sys.path.insert(1, '..\\util')
sys.path.insert(2, "C:\\OscarScripts\\util")
from calendar_datetime import get_today_date_yyyymmdd
from calendar_datetime import get_today_wkday
from shutil import copyfile
import logging
import os
import csv
import datetime
import re


def get_demographic(headers, instance, providerid_list):
    # provider_list is passed as a list of providerID from MDStaff

    providerids_to_names_hash = {}
    providerids_to_sccuids_hash = {}

    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()
    begin_time_obj = datetime.datetime.now()

    dir_path = os.path.dirname(os.path.realpath(__file__))

    output_file = dir_path + "/data/demographic_providerids_" + instance + "_"+ today_date + ".txt"
    final_table = dir_path + "/data/demographic_providerids_" + instance + "_final.txt"
    log_file = dir_path + api_const.log_file

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.info, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". Starting Get Demographic API.")

    with open(output_file, "w", newline = '') as output_fh:
        output_writer = csv.writer(output_fh, delimiter = '|')
        output_writer.writerow(["provider_id", "vmcid", "name", "email_addr"])

        logger.info(wkday + ". Getting each staff demographic data")

        for providerid in providerid_list:
            api_url = api_const.api_url + "/" + instance + "/demographic/" + providerid

            logger.debug(wkday + ". API URL: " + api_url)

            try:
                response = requests.get(api_url, headers = headers, timeout = 60)
                response.raise_for_status()

            except requests.exceptions.RequestException as err:
                logger.critical(wkday + ". OOps: Something Else: " + str(err))
                logger.critical(wkday + ". " + api_url)
                continue

            except requests.exceptions.HTTPError as errh:
                logger.critical(wkday + ". Http Error: " + errh)
                logger.critical(wkday + ". " + api_url)
                continue

            except requests.exceptions.ConnectionError as errc:
                logger.critical(wkday + ". Error Connecting: " + errc)
                logger.critical(wkday + ". " + api_url)
                continue

            except requests.exceptions.Timeout as errt:
                logger.critical(wkday + ". Timeout Error: " + errt)
                logger.critical(wkday + ". " + api_url)
                continue

            response_json = response.json()
            name = response_json["FormattedName"]
            sccuid = response_json["OtherID"]
            email_addr = response_json["Email"]

            if sccuid == None:
                logger.critical(wkday + ". " + name + " SCCUID is not found in MDStaff")
            else:
                sccuid = sccuid.strip()

            providerids_to_names_hash[providerid] = name
            providerids_to_sccuids_hash[providerid] = sccuid
            logger.debug(wkday + ". Get demographics. " + ". " \
                         + providerids_to_names_hash[providerid])

            output_writer.writerow([providerid, str(sccuid), name, email_addr])

    copyfile(output_file, final_table)
    logger.info(wkday + ".  Creating the table: " + output_file)
    logger.info(wkday + ".  Creating the table: " + final_table)

    end_time_obj = datetime.datetime.now()
    diff_time = (end_time_obj - begin_time_obj).total_seconds()
    diff_time = int(diff_time)
    logger.info(wkday + ". Completing all staff demographic data")
    logger.info(wkday + ".  Run ends.  It took " + str(diff_time) + " second(s) to complete")

    return providerids_to_sccuids_hash, providerids_to_names_hash



def main():
    providerids_to_sccids_hash, providerids_to_names_hash = \
         get_demographic(headers, instance, providerid_list)

if __name__ == "__main__":
    main()