import requests
import mdstaff_api_const
import sys
sys.path.insert(1, '../util/')
import calendar_datetime
from shutil import copyfile
import logging

def get_demographic(headers, provider_list):
    # mdstaff id list should be passed as a list
    mdstaff_names = {}
    mdstaff_sccids = {}

    today_date = calendar_datetime.get_today_date_yyyymmdd()
    output_file = "data/mdstaff_id_table_" + today_date + ".txt"
    
    current_time = calendar_datetime.get_current_time()
    
    logging.basicConfig(
        filename = 'data/mdstaff_api.log', \
        filemode = 'a', \
        level = logging.DEBUG, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
        
    logging.debug("Starting get demographic.  Current time = " + current_time)
    
    output_file_obj = open(output_file, "w")
    output_file_obj.write("mdstaff_id|vmcid|name\n")
    counter = 1

    for mdstaff_id in provider_list:
        api_url = mdstaff_api_const.api_url + "demographic/" + mdstaff_id
        logging.debug(api_url)
        response = requests.get(api_url, headers = headers)
        logging.debug(str(counter) + ": Get_demographic api return code: " + \
              str(response.status_code))

        response_json = response.json()
        name = response_json["FormattedName"]
        sccid = response_json["OtherID"]
        mdstaff_names[mdstaff_id] = name
        mdstaff_sccids[mdstaff_id] = sccid
        counter = counter + 1
        
        output_file_obj.write(mdstaff_id + "|" + str(sccid) + "|" + name + "\n")

    output_file_obj.close()
    current_time = calendar_datetime.get_current_time()
    logging.debug("Completing get demographic.  Current time = " + current_time)
    copyfile(output_file, "mdstaff_id_table_final.txt")
    
def merge_id_table():
    
    today_date = calendar_datetime.get_today_date_yyyymmdd()
    output_file = "id_crosswalk"
    

def main():
    get_demographic(headers, mdstaff_id_list)

if __name__ == "__main__":
    main()