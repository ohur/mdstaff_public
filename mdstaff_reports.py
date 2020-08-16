from api_authentication import get_auth_token
from api_get_credential import get_credential
from api_get_providers import get_providers
from api_get_demographic import get_demographic
from api_get_appointments import get_appointments
from api_get_lookups import get_lookups
import api_get_headers
import os
import sys
import logging
sys.path.insert(1, '../util/')
sys.path.insert(2, "C:/OscarScripts/util")
from calendar_datetime import get_today_date_yyyymmdd
from calendar_datetime import get_today_wkday
import datetime
import csv
import api_const
import subprocess
import getpass
import socket
from shutil import copyfile

# this is to run daily for inpatient and ambulatory
# checking if today data is available first, if not
# get the list of provider ID
# from the provider ID, get the credential ID
# from the provider ID, get the appointment ID
# write a MDStaff reports and put it in shared H network drive

def mdstaff_reports(instance):

    hostname = socket.gethostname().lower().strip()
    username = getpass.getuser()

    begin_time_obj = datetime.datetime.now()
    today_date = get_today_date_yyyymmdd()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if instance == "inpatient":
        instance = api_const.inpatient_instance
        if hostname == "hhssvninappt001" or hostname == "hhssvninappp001":
            log_file = "C:\\inetpub\\wwwroot\\oscarhur\\" + api_const.inpatient_log_file
        else:
            log_file = dir_path + api_const.inpatient_log_file

    elif instance == "ambulatory":
        instance = api_const.ambulatory_instance
        if hostname == "hhssvninappt001" or hostname == "hhssvninappp001":
            log_file = "C:\\inetpub\\wwwroot\\oscarhur\\" + api_const.ambulatory_log_file
        else:
            log_file = dir_path + api_const.ambulatory_log_file

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    wkday = get_today_wkday()

    logger.info("=================")
    logger.info(wkday + ". " + instance + ". Starting MDStaff API.  By " + username + " from " + hostname)

    auth_token = get_auth_token(instance)
    get_headers = api_get_headers.get_headers(auth_token)

    # to get a hash of providerid vs sccid
    # with 'get providers' and 'get demographic'

    providerid_list = get_providers(get_headers, instance)

    providerids_to_sccuids_hash = {}
    providerids_to_names_hash = {}
    providerids_to_apptids_hash = {}

    providerids_to_sccuids_hash, providerids_to_names_hash = \
                   get_demographic(instance, providerid_list)

    # get the lic data
    # get hashes of lic data (num and exp date) with SCCUID

    providerids_to_licnums_hash, providerids_to_licexps_hash = \
                               get_credential(instance, providerid_list)

    # get the appointment data
    # for department and division data of the staff

    providerids_to_apptids_hash, providerids_to_depts_hash, providerids_to_divs_hash = \
        get_appointments(instance, providerid_list)

    # get department and division names from lookup table

    dept_hash = {}
    div_hash = {}

    auth_token = get_auth_token(instance)
    get_headers = api_get_headers.get_headers(auth_token)
    dept_hash = get_lookups(get_headers, instance, "department")

    if instance == api_const.inpatient_instance:
        # get the division data of VMC, OCH, SLRH
        div_hash = get_lookups(get_headers, instance, "division")

    # writing the reports through API
    #

    output_file = dir_path + "/data/mdstaff_report_" + instance + ".txt"
    logger.info(wkday + ". " + instance + ".  Writing report " + output_file)
    with open (output_file, "w", newline = "") as output_file_fh:
        csv_writer =csv.writer(output_file_fh, delimiter = "|")
        csv_writer.writerow(["sccuid", "fullname", "licnum", "licexp", "division", "dept"])

        for providerid, sccuid in providerids_to_sccuids_hash.items():
            fullname = providerids_to_names_hash[providerid]
            div = ""

            try:
                licnum = providerids_to_licnums_hash[providerid]
            except:
                logger.critical(wkday + ". " + instance + ".  Lic Num not found for " + \
                                fullname + " " + sccuid)

            try:
                licexp = providerids_to_licexps_hash[providerid]
            except:
                logger.critical(wkday + ". " + instance + ".  Lic Expiration not found for " + \
                                fullname + " " + sccuid)

            if instance == api_const.inpatient_instance:
                try:
                    div_code = providerids_to_divs_hash[providerid]
                    div = div_hash[div_code]
                except:
                    logger.critical(wkday + ". " + instance + ".  Division not found for " + \
                                fullname + " " + sccuid)

            try:
                dept_code = providerids_to_depts_hash[providerid]
                dept = dept_hash[dept_code]
            except:
                dept = ""
                logger.critical(wkday + ". " + instance + ".  Dept data not found for " + \
                                fullname)

            csv_writer.writerow([sccuid, fullname, licnum, licexp, div, dept])

    if hostname == "hhssvninappt001" or hostname == "hhssvninappp001":

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        subprocess.call(r'net use h: /del')
        subprocess.call(r'net use h: \\hhsisiAOB\hipaa$')
        shared_drive = "H:\\FTP-root\\Virtual_Folders\\NURSING\\mdstaff\\data\\"
        shared_file = shared_drive + "mdstaff_report_" + instance + "_" + today_date  + ".txt"
        copyfile(output_file, shared_file)
        logger.info(wkday + ". " + instance + ".  Report copied to " + shared_drive + "/" + output_file)

    end_time_obj = datetime.datetime.now()
    diff_time = (end_time_obj - begin_time_obj).total_seconds()
    diff_time_sec = int(diff_time)
    diff_time_min = diff_time_sec / 60
    diff_time_min = str(round(diff_time_min, 2))
    logger.info(wkday + ". " + instance + ".  MDStaff License Report created " + output_file)
    logger.info(wkday + ". " + instance +  ".  Run ends.  It took " + str(diff_time_sec) + \
                " seconds or " + diff_time_min + " minutes to complete")
    logger.info("=================")


def main():
    mdstaff_reports(instance)

if __name__ == "__main__":
    main()

