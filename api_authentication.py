import requests
import api_const
import sys
sys.path.insert(1, '..\\util')
sys.path.insert(2, 'C:\\OscarScripts\\util')
import os
from calendar_datetime import get_today_wkday
from calendar_datetime import get_current_time
import logging

def get_auth_token(instance):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_file = dir_path + "/data/mdstaff_api_authentication.txt"
    log_file = dir_path + api_const.log_file
    output_file_obj = open(output_file, "w")

    wkday = get_today_wkday()

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)

    username = api_const.username
    
    if instance == api_const.inpatient_instance:
        # inpatient nursing
        password = api_const.inpatient_password
        facility_id = api_const.inpatient_facility_id

    elif instance == api_const.ambulatory_instance:
        # ambulatory nursing
        password = api_const.ambulatory_password
        facility_id = api_const.ambulatory_facility_id

    credentials = {
        "grant_type" : "password",
        "username" : username,
        "password" : password,
        "instance" : instance,
        "facilityID" : facility_id
    }

    logger.info(wkday + ". Starting authentication")
    print(username, password, instance, facility_id)
    output_file_obj.write(username + " " + password + " " + instance + " " + \
                          facility_id + "\n\n")
    mdstaff_auth_url = "https://api.mdstaff.com/webapi/api/tokens"
    auth_response = requests.post(mdstaff_auth_url, data = credentials)

    # Read token from auth response
    auth_response_json = auth_response.json()
    auth_token = auth_response_json["access_token"]
    auth_token_type = auth_response_json["token_type"]
    auth_expire = auth_response_json["expires_in"]

    output_file_obj.write("access_token:\n" + auth_token + "\n\n")
    print("Token:\n" + auth_token + "\n")
    output_file_obj.write("token_type:\n" + auth_token_type + "\n\n")
    output_file_obj.write("expires_in:\n" + str(auth_expire) + "\n\n")

    current_time = get_current_time()
    print("Current time: " + current_time)
    output_file_obj.write("current time:\n" + current_time + "\n\n")

    return auth_token



def main():
    auth_token = get_auth_token(instance)


if __name__ == "__main__":
    main()