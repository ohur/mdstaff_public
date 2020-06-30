import requests
import mdstaff_api_const
import sys
sys.path.insert(1, '..\\util')
sys.path.insert(2, "C:\\OscarScripts\\util")
from calendar_datetime import get_today_date_yyyymmdd
from calendar_datetime import get_today_wkday
from shutil import copyfile
import logging
import os
import csv

def get_demographic(headers, provider_list, instance):
    # mdstaff id list should be passed as a list
    mdstaff_names = {}
    mdstaff_sccids = {}
    
    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    if instance == mdstaff_api_const.inpatient_instance:
        output_file = dir_path + "/data/mdstaff_id_table_inpt" + today_date + ".txt"
        final_table = dir_path + "/data/mdstaff_id_table_inpt_final.txt"
        
    elif instance == mdstaff_api_const.ambulatory_instance:
        output_file = dir_path + "/data/mdstaff_id_table_amb" + today_date + ".txt"
        final_table = dir_path + "/data/mdstaff_id_table_amb_final.txt"
        
    log_file = dir_path + mdstaff_api_const.log_file
    
    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
        
    logging.info(wkday + ". Starting get demographic.")
    
    output_file_obj = open(output_file, "w")
    output_file_obj.write("mdstaff_id|vmcid|name\n")
    counter = 1
    logging.info(wkday + ". Getting each staff demographic data")

    for mdstaff_id in provider_list:
        api_url = mdstaff_api_const.api_url + "/" + instance + "/demographic/" + mdstaff_id
        
        logging.debug(wkday + ". API URL: " + api_url)
        response = requests.get(api_url, headers = headers)
        
        if response.status_code == 200:
            pass
        else:
            logging.critical(wkday + ". API URL: " + api_url)
            logging.critical(wkday + ". Get_demographic api return code: " + \
                             str(response.status_code))

        response_json = response.json()
        name = response_json["FormattedName"]
        sccid = response_json["OtherID"]
        email_add = response_json["Email"]
        mdstaff_names[mdstaff_id] = name
        mdstaff_sccids[mdstaff_id] = sccid
        counter = counter + 1
        
        output_file_obj.write(mdstaff_id + "|" + str(sccid) + "|" + name + "\n")

    output_file_obj.close()
    
    logging.info(wkday + ". Completing all staff demographic data")
    copyfile(output_file, final_table)
    
    return mdstaff_sccids, mdstaff_names
    
    
    
def merge_id_table():
    
    today_date = calendar_datetime.get_today_date_yyyymmdd()
    output_file = "id_crosswalk"
    

def main():
    get_demographic(headers, mdstaff_id_list)

if __name__ == "__main__":
    main()
