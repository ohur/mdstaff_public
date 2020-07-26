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


def get_facilities(headers, instance):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_file = dir_path + api_const.log_file
    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()
    
    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". Starting GET FACILITIES API")   
    
    api_url = api_const.api_url + instance + "/facilities"
    logger.info(wkday + ". API URL: " + api_url)    
    
    response = requests.get(api_url, headers = headers)    
    response_json = response.json()

    for i in response_json:
        uid = i["Uid"]
        if i["Code"] == "VHCDOWNTOWNCLINIC":
            continue        
        
    logger.info(wkday + ". Facility UID is " + uid)
    return (uid)


def main():
    facility_id = get_facilities(headers, instance)


if __name__ == "__main__":
    main()