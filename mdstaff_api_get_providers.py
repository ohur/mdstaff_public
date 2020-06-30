import requests
import mdstaff_api_const
import sys
sys.path.insert(1, '..\\util')
sys.path.insert(2, 'C:\\OscarScripts\\util')
from calendar_datetime import get_today_date_yyyymmdd
from calendar_datetime import get_today_wkday
import logging
import os

def get_providers(headers, instance):
    
    today_date = get_today_date_yyyymmdd()
    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_file = dir_path + "/data/mdstaff_provider_list_" + today_date + ".txt"
    log_file = dir_path + mdstaff_api_const.log_file
    
    output_file_obj = open(output_file, "w")
    
    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")        
        
    logging.info(wkday + ". Starting provider list. " + instance)
    
    mdstaff_provider_id = []
    
    if instance == mdstaff_api_const.inpatient_instance:
        api_url = mdstaff_api_const.api_url + "countyofsantaclarahealthinpatientnursing/"
        
    elif instance == mdstaff_api_const.ambulatory_instance:
        api_url = mdstaff_api_const.api_url + "scvmc-ambulatory-nursing-test/"     
      
    api_url = api_url + "providers/facility"
    logging.info(wkday + ". API URL: " + api_url)
   
    response = requests.get(api_url, headers = headers)
    
    response_json = response.json()
    
    for i in response_json:        
        mdstaff_provider_id.append(i["ProviderID"])
        output_file_obj.write(i["ProviderID"] + "|" + i["Name"] + "\n")
    
    logging.info(wkday + ". Return code: " + str(response.status_code))    
    return mdstaff_provider_id
    
    

def main():    
    get_providers(headers)


if __name__ == "__main__":
    main()
