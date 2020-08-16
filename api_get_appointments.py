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
from api_authentication import get_auth_token
import api_get_headers
import socket

def get_appointments(instance, providerid_list):
    # mdstaff_id should be passed as a list

    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    providerids_to_apptids_hash = {}
    providerids_to_depts_hash = {}
    providerids_to_divs_hash = {}

    log_file = ""
    hostname = socket.gethostname().lower().strip()

    output_file = "appointment_" + instance + ".txt"
    output_file = dir_path + "/data/" + output_file

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
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". " + instance + ". Starting Get Appointment API.")

    with open(output_file, "w", newline = '') as output_fh:
        output_writer = csv.writer(output_fh, delimiter = '|')
        output_writer.writerow(["providerid", "apptid", "dept", "div"])

        counter = 0

        for providerid in providerid_list:
            api_url = api_const.api_url + instance + "/providers/" + providerid + "/appointment"
            logger.debug(wkday + ". " + api_url)
            counter = counter + 1

             # API authentication expires in about 15 minutes
             # So after each 1700 iterations, we will get authentication again
            if (counter % 1700 == 0) or counter == 1:
                auth_token = get_auth_token(instance)
                headers = api_get_headers.get_headers(auth_token)

            try:
                response = requests.get(api_url, headers = headers, timeout = 60)
                response.raise_for_status()

            except requests.exceptions.RequestException as err:
                logging.critical(wkday + ". " + instance + ". OOps: Something Else: " + str(err))
                logging.critical(wkday + ". " + instance + ". " + api_url)

            except requests.exceptions.HTTPError as errh:
                logging.critical(wkday + ". " + instance + ". Http Error: " + errh)
                logging.critical(wkday + ". " + instance + ". " + api_url)

            except requests.exceptions.ConnectionError as errc:
                logging.critical(wkday + ". " + instance + ". Error Connecting: " + errc)
                logging.critical(wkday + ". " + instance + ". " + api_url)

            except requests.exceptions.Timeout as errt:
                logging.critical(wkday + ". " + instance + ". Timeout Error: " + errt)
                logging.critical(wkday + ". " + instance + ". " + api_url)

            response_json = response.json()
            for i in response_json:
                apptid = i["AppointmentID"]
                providerid = i["ProviderID"]
                dept = i["DepartmentID_1"]
                division = i["DivisionID"]
                providerids_to_apptids_hash[providerid] = apptid
                providerids_to_depts_hash[providerid] = dept
                providerids_to_divs_hash[providerid] = division

            output_writer.writerow([providerid, apptid, dept, division])

    logger.info(wkday + ". " + instance + ". Completing all staff appointment data")
    logger.info(wkday + ". " + instance + ". Creating the table: " + output_file)
    return providerids_to_apptids_hash, providerids_to_depts_hash, providerids_to_divs_hash


def main():
    providerids_to_apptids_hash, providerids_to_depts_hash, providerids_to_divs_hash = \
          get_appointments(instance, providerid_list)


if __name__ == "__main__":
    main()