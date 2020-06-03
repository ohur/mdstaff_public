import requests
import mdstaff_api_const
import sys
sys.path.insert(1, '../util/')
import calendar_datetime

def get_auth_token(instance = "inpatient"):   
    
    output_file_obj = open("data/mdstaff_api_output.txt", "w") 
        
    if instance == "inpatient":
        username = mdstaff_api_const.inpatient_username
        password = mdstaff_api_const.inpatient_password        
        instance = mdstaff_api_const.inpatient_instance
        facility_id = mdstaff_api_const.inpatient_facility_id  
    
    credentials = {
        "grant_type" : "password",
        "username" : username,
        "password" : password,
        "instance" : instance,
        "facilityID" : facility_id            
    }
    
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
    
    
    current_time = calendar_datetime.get_current_time()
    print("Current time: " + current_time)
    output_file_obj.write("current time:\n" + current_time + "\n\n")
    
    
    return auth_token

def main():    
    auth_token = get_auth_token()    

if __name__ == "__main__":
    main()
