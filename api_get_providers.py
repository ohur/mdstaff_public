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

# this return a list of providerID in MDStaff with GET method

def get_providers(headers, instance):

    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_file = dir_path + "/data/providerid_list_" + instance + "_" \
                  + today_date + ".txt"
    log_file = dir_path + api_const.log_file    

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". Starting Get Provider API. Getting a list of ProviderID. " \
                 + instance)

    # an array of mdstaff providerid
    providerid_list = []

    if instance == api_const.inpatient_instance:
        api_url = api_const.api_url + instance

    elif instance == api_const.ambulatory_instance:
        api_url = api_const.api_url + mdstafinstance

    api_url = api_url + "/providers/facility"
    logger.info(wkday + ". API URL: " + api_url)

    response = requests.get(api_url, headers = headers)
    response_json = response.json()

    with open(output_file, "w", newline = '') as output_fh:
        output_writer = csv.writer(output_fh, delimiter = '|')
        for i in response_json:
            output_writer.writerow([i["ProviderID"], i["Name"]])
            providerid_list.append(i["ProviderID"])

    logger.info(wkday + ". Return code: " + str(response.status_code))
    return providerid_list



def main():
    mdstaff_provider_ids = get_providers(headers)


if __name__ == "__main__":
    main()