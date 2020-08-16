import requests
import api_const
import sys
sys.path.insert(1, '..\\util')
sys.path.insert(2, 'C:\\OscarScripts\\util')
from calendar_datetime import get_today_date_yyyymmdd
from calendar_datetime import get_today_wkday
import logging
import os
import csv
import socket

# this return a list of providerID in MDStaff with GET method

def get_providers(headers, instance):

    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_file = ""
    hostname = socket.gethostname().lower().strip()
    
    if instance == api_const.inpatient_instance:
        password = api_const.inpatient_password
        facility_id = api_const.inpatient_facility_id
        if hostname == "hhssvninappt001" or hostname == "hhssvninappp001":
            log_file = "C:\\inetpub\\wwwroot\\oscarhur\\" + api_const.inpatient_log_file
        else:
            log_file = dir_path + api_const.inpatient_log_file

    elif instance == api_const.ambulatory_instance:
        password = api_const.ambulatory_password
        facility_id = api_const.ambulatory_facility_id
        if hostname == "hhssvninappt001" or hostname == "hhssvninappp001":
            log_file = "C:\\inetpub\\wwwroot\\oscarhur\\" + api_const.ambulatory_log_file
        else:
            log_file = dir_path + api_const.ambulatory_log_file

    output_file = dir_path + "/data/providerid_list_" + instance + ".txt"
    log_file = dir_path + log_file

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". " + instance + ". Starting Get Provider API. Getting a list of ProviderID.")

    # an array of mdstaff providerid
    providerid_list = []

    api_url = api_const.api_url + instance
    api_url = api_url + "/providers/facility"
    logger.info(wkday + ". " + instance + ". API URL: " + api_url)

    response = requests.get(api_url, headers = headers)
    response_json = response.json()

    with open(output_file, "w", newline = '') as output_fh:
        output_writer = csv.writer(output_fh, delimiter = '|')
        for i in response_json:
            output_writer.writerow([i["ProviderID"], i["Name"]])
            providerid_list.append(i["ProviderID"])

    logger.info(wkday + ". " + instance + ". Return code: " + str(response.status_code))
    return providerid_list



def main():
    mdstaff_providerids = get_providers(headers, instance)


if __name__ == "__main__":
    main()