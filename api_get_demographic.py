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

def get_demographic(headers, instance, providerid_list):
    # provider_list is passed as a list of providerID from MDStaff

    providerids_to_names_hash = {}
    providerids_to_sccids_hash = {}

    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    output_file = dir_path + "/data/demographic_" + instance + "_"+ today_date + ".txt"
    final_table = dir_path + "/data/mdstaff_demographic_" + instance + "_final.txt"
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
        counter = 1
        logger.info(wkday + ". Getting each staff demographic data")
    
        for providerid in providerid_list:
            api_url = api_const.api_url + "/" + instance + "/demographic/" + providerid
    
            logger.debug(wkday + ". API URL: " + api_url)
           
            try:
                response = requests.get(api_url, headers = headers, timeout = 60)
                response.raise_for_status()

            except requests.exceptions.RequestException as err:
                logging.critical(wkday + ". OOps: Something Else: " + str(err))
                logging.critical(wkday + ". " + api_url)
                continue

            except requests.exceptions.HTTPError as errh:
                logging.critical(wkday + ". Http Error: " + errh)
                logging.critical(wkday + ". " + api_url)
                continue

            except requests.exceptions.ConnectionError as errc:
                logging.critical(wkday + ". Error Connecting: " + errc)
                logging.critical(wkday + ". " + api_url)
                continue

            except requests.exceptions.Timeout as errt:
                logging.critical(wkday + ". Timeout Error: " + errt)
                logging.critical(wkday + ". " + api_url)
                continue
    
            response_json = response.json()
            name = response_json["FormattedName"]
            sccid = response_json["OtherID"]
            email_addr = response_json["Email"]
            providerids_to_names_hash[providerid] = name
            providerids_to_sccids_hash[providerid] = sccid
            logger.info(wkday + ". Get demographics. " + str(counter) + ". " \
                         + providerids_to_names_hash[providerid])
    
            counter = counter + 1
    
            output_writer.writerow([providerid, str(sccid), name, email_addr])

    

    logging.info(wkday + ". Completing all staff demographic data")
    copyfile(output_file, final_table)
    logging.info(wkday + ".  Creating the table: " + final_table)
    return providerids_to_sccids_hash, providerids_to_names_hash



def main():
    providerids_to_sccids_hash, providerids_to_names_hash = \
         get_demographic(headers, instance, providerid_list)

if __name__ == "__main__":
    main()