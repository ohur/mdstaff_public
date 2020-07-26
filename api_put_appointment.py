import requests
import api_const
import csv
import sys
sys.path.insert(1, '../util/')
sys.path.insert(2, "C:/OscarScripts/util")
from calendar_datetime import get_today_date_yyyymmdd
from calendar_datetime import get_today_wkday
import os
import logging
from api_get_lookups import get_lookups

def put_appointment(put_headers, \
                    get_headers, \
                    instance, \
                    providerids_to_apptids_hash, \
                    providerids_to_sccids_hash, \
                    providerids_to_names_hash):
    # credential_data should be passed as a hash of providerID and credentialID,
    # with credentialID as the key
    # lic_data should be passed as a hash of data to be modified and credentialID
    # with credentialID as the key

    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_file = dir_path + api_const.log_file

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". Starting PUT APPOINTMENT API")

    # for mdstaff nursing PUT appointment is to add dept and division data only
    sccids_to_depts_hash = {}
    dept = ""

    with open("SantaClara_66403_20200709-1002.txt", "r") as input_fh:
        csv_reader = csv.reader(input_fh, delimiter = "|")
        for row in csv_reader:
            sccid = row[4]
            dept = str(row[5])
            sccids_to_depts_hash[sccid] = dept

    deptcodes_to_deptids_hash = get_lookups(get_headers, instance, "department")
    divnames_to_divids_hash = get_lookups(get_headers, instance, "division")
    print(deptcodes_to_deptids_hash)

    for providerid, apptid in providerids_to_apptids_hash.items():
        print(providerid, apptid)
        sccid = providerids_to_sccids_hash[providerid]
        staff_name = providerids_to_names_hash[providerid]

        try:
            dept = sccids_to_depts_hash[sccid]
            deptid = deptcodes_to_deptids_hash[dept]

        except:
            logger.critical(wkday + ". " + staff_name + " not found in PeopleSoft.")
            continue

        if int(dept) < 8400:
            divname = "VMC"
        elif int(dept) > 8400 and int(dept) < 8600:
            divname = "OCH"
        else:
            divname = "SLRH"
        
        logger.info(wkday + ". " + staff_name + ". " + divname + " & " + dept)

        division = divnames_to_divids_hash[divname]

        api_url = api_const.api_url + instance + "/providers/" + providerid \
                  + "/appointment/" + apptid
        logger.info(wkday + ". " + staff_name + ". " + api_url)

        data = '{"DepartmentID_1": "' + deptid + '","DivisionID":"' + division + '"}'
        
        try:
            response = requests.put(api_url, \
                                    headers = put_headers, \
                                    data = data, \
                                    timeout = (250, 500))
            response.raise_for_status()

        except requests.exceptions.RequestException as err:
            logging.critical(wkday + ". OOps: Something Else: " + str(err))
            logging.critical(wkday + ". " + api_url)
            logging.critical(wkday + ". " + data)
            continue

        except requests.exceptions.HTTPError as errh:
            logging.critical(wkday + ". Http Error: " + str(errh))
            logging.critical(wkday + ". " + api_url)
            logging.critical(wkday + ". " + data)
            continue

        except requests.exceptions.ConnectionError as errc:
            logging.critical(wkday + ". Error Connecting: " + str(errc))
            logging.critical(wkday + ". " + api_url)
            logging.critical(wkday + ". " + data)
            continue

        except requests.exceptions.Timeout as errt:
            logging.critical(wkday + ". Timeout Error: " + str(errt))
            logging.critical(wkday + ". " + api_url)
            logging.critical(wkday + ". " + data)
            contiue

        response_json = response.json()

        logger.info(wkday + ". " + staff_name + ". " + "Put Appointment return code: " + \
                    str(response.status_code))


def main():
    put_appointment(put_headers, \
                    get_headers, \
                    instance,
                    providerids_to_apptids_hash, \
                    providerids_to_sccids_hash, \
                    providerids_to_names_hash)


if __name__ == "__main__":
    main()