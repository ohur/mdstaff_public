import requests
import mdstaff_api_const
import csv


def get_sccid(headers, provider_list):    
    # mdstaff id list should be passed as a list
    mdstaff_names = {}
    mdstaff_sccids = {}          
    
    
    for mdstaff_id in provider_list:
        api_url = mdstaff_api_const.api_url + "demographic/" + mdstaff_id
        print(api_url)
        response = requests.get(api_url, headers = headers)
        print("get_demographic api return code: " + str(response.status_code))
        response_json = response.json()
        name = response_json["FormattedName"]
        sccid = response_json["OtherID"]
        mdstaff_names[mdstaff_id] = name
        mdstaff_sccids[mdstaff_id] = sccid  
        output_file_obj.write(mdstaff_id + "|" + sccid + "|" + name + "\n")
    
    output_file_obj.close()   
    return (mdstaff_names, mdstaff_sccids)

def main():    
    get_sccid(headers, mdstaff_id_list)

if __name__ == "__main__":
    main()