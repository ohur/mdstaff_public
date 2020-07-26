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


def get_lookups(headers, instance, lookups):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_file = dir_path + api_const.log_file
    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()

    output_file = dir_path + "/data/" + instance + "_" + \
                  lookups + "_" + today_date + ".txt"
    log_file = dir_path + api_const.log_file    
    

    table_hash = {}

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". Starting GET LOOKUPS API")

    api_url = api_const.api_url + instance + "/lookups/" + lookups
    logger.info(wkday + ". API URL: " + api_url)

    response = requests.get(api_url, headers = headers)
    response_json = response.json()

    with open (output_file, "w", newline = "") as output_fh:
        csv_writer = csv.writer(output_fh, delimiter = "|")
        for i in response_json:
            id_code = i["ID"]
            description = i["Description"]

            if lookups == "department":
            	description = description[0:4]
            csv_writer.writerow([description, id_code])
            table_hash[description] = id_code

    return table_hash


def main():
    hash_dict = get_lookups(headers, instance, lookups)


if __name__ == "__main__":
    main()