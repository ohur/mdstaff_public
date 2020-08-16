import requests
import api_const
import csv
import logging
import sys
import os
sys.path.insert(1, '../util/')
sys.path.insert(2, "C:/OscarScripts/util")
from calendar_datetime import get_today_date_yyyymmdd
from calendar_datetime import get_today_wkday
import socket


def get_lookups(headers, instance, lookup_type):
    dir_path = os.path.dirname(os.path.realpath(__file__))    
    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()

    output_file = dir_path + "/data/" + instance + "_" + \
                  lookup_type + "_" + ".txt"
    log_file = "" 
    hostname = socket.gethostname().lower().strip()
    
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

    table_hash = {}

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". " + instance + ". Starting GET LOOKUPS API " + lookup_type)

    api_url = api_const.api_url + instance + "/lookups/" + lookup_type
    logger.info(wkday + ". " + instance + ". API URL: " + api_url)

    response = requests.get(api_url, headers = headers)
    response_json = response.json()

    with open (output_file, "w", newline = "") as output_fh:
        csv_writer = csv.writer(output_fh, delimiter = "|")
        for i in response_json:
            id_code = i["ID"]
            description = i["Description"]            
            csv_writer.writerow([description, id_code])
            table_hash[id_code] = description

    return table_hash


def main():
    hash_dict = get_lookups(headers, instance, lookup_type)


if __name__ == "__main__":
    main()