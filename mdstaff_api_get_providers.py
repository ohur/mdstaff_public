import requests
import mdstaff_api_const
import sys
sys.path.insert(1, '..\\util')
sys.path.insert(2, 'C:\\OscarScripts\\util')
import calendar_datetime
import logging

def get_providers(headers):
    
    today_date = calendar_datetime.get_today_date_yyyymmdd()
    output_file = "data/mdstaff_provider_list_" + today_date + ".txt"
    output_file_obj = open(output_file, "w")
    
    logging.basicConfig(
        filename = 'data/mdstaff_api.log', \
        filemode = 'a', \
        level = logging.DEBUG, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
        
    current_time = calendar_datetime.get_current_time()
    logging.critical("Starting provider list.  Current Time = " + current_time)
    
    mdstaff_provider_id = []
    
    api_url = mdstaff_api_const.api_url + "providers" 
    response = requests.get(api_url, headers = headers)
    
    response_json = response.json()
    for i in response_json:
        mdstaff_provider_id.append(i["ProviderID"])
        output_file_obj.write(i["ProviderID"] + "\n")
        
    current_time = calendar_datetime.get_current_time()
    logging.critical("Completed provider list: Current Time = " + current_time)    
    return mdstaff_provider_id

def main():    
    get_providers(headers)

if __name__ == "__main__":
    main()
