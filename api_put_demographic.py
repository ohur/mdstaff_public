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


def put_demographic(headers, instance):
    # mdstaff_id should be passed as a hash
    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_file = dir_path + api_const.log_file

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.info, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". Starting PUT DEMOGRAPHIC API")
    
    
    with open ("output_final2.txt", "r") as input_fh:
        csv_reader = csv.reader(input_fh, delimiter = "|")
        for row in csv_reader:
            providerid = row[5]
            firstname = row[3].strip().title()
            middlename = row[4].strip().title()
            lastname = row[2].strip().title()

            api_url = api_const.api_url + instance + "/demographic/" + providerid
    
            logger.info(wkday + ". API URL: " + api_url)
            
    
            
    
            data = '{"FirstName":"' + firstname + '", "MiddleName":"' + middlename + '","LastName":"' + lastname + '"}'
            print(data)
    
            try:
                response = requests.put(api_url, \
                                        headers = headers, \
                                        data = data, \
                                        timeout = (250, 500))
                response.raise_for_status()
    
            except requests.exceptions.RequestException as err:
                logger.critical(wkday + ". OOps: Something Else: " + str(err))
                logger.critical(wkday + ". " + api_url)
                logger.critical(wkday + ". " + data)
                continue
    
            except requests.exceptions.HTTPError as errh:
                logger.critical(wkday + ". Http Error: " + str(errh))
                logger.critical(wkday + ". " + api_url)
                logger.critical(wkday + ". " + data)
                continue
    
            except requests.exceptions.ConnectionError as errc:
                logger.critical(wkday + ". Error Connecting: " + str(errc))
                logger.critical(wkday + ". " + api_url)
                logger.critical(wkday + ". " + data)
                continue
    
            except requests.exceptions.Timeout as errt:
                logger.critical(wkday + ". Timeout Error: " + str(errt))
                logger.critical(wkday + ". " + api_url)
                logger.critical(wkday + ". " + data)
                continue
    
            response_json = response.json()
    
            logger.info("Return code: " + str(response.status_code))
    


def email_data():
    sccids_to_emails_hash = {}
    with open("SantaClara_66403_20200709-1002.txt", "r") as input_fh:
        csv_reader = csv.reader(input_fh, delimiter = "|")
        for row in csv_reader:
            email = row[15]
            sccid = row[4]
            sccids_to_emails_hash[sccid] = email
    return providerids_to_lnames_hash, providerids_to_fnames_hash, providerids_to_mnames_hash



def main():

    put_demographic(headers, \
                    instance)



if __name__ == "__main__":
    main()