import requests
import api_const
import csv
import logging
import sys
sys.path.insert(1, '../util/')
sys.path.insert(2, "C:/OscarScripts/util")
from calendar_datetime import get_today_date_yyyymmdd
from calendar_datetime import get_today_wkday
import os

def get_appointment(headers, instance, providerid_list):
    # mdstaff_id should be passed as a list

    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    output_file = dir_path + "/data/appointment_" + instance + "_" + \
                  today_date + ".txt"
    log_file = dir_path + api_const.log_file
    final_table = dir_path + "/data/mdstaff_appointment_" + instance + "_final.txt"

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". Starting Get Appointment API. Getting a list of AppointmentID. " \
                 + instance)

    providerids_to_apptids_hash = {}    

    with open(output_file, "w", newline = '') as output_fh:
        output_writer = csv.writer(output_fh, delimiter = '|')
        output_writer.writerow(["providerid", "apptid", "dept"])
        for providerid in providerid_list:
            api_url = api_const.api_url + instance + "/providers/" + providerid + "/appointment"
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

            response_json = response.json()
            for i in response_json:
                apptid = i["AppointmentID"]
                providerid = i["ProviderID"]
                providerids_to_apptids_hash[providerid] = apptid

            output_writer.writerow([providerid, apptid])
            
    copyfile(output_file, final_table)
    logger.info(wkday + ". Completing all staff appointment data")
    logger.info(wkday + ". Creating the table: " + final_table)
    return providerids_to_apptids_hash


def main():
    providerids_to_apptids_hash = \
               get_appointment(headers, instance, prvoviderid_list)


if __name__ == "__main__":
    main()