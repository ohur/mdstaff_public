import csv
import sys
sys.path.insert(1, '../util/')
sys.path.insert(2, "C:/OscarScripts/util")
from calendar_datetime import get_today_wkday
import os
import logging
import api_const

def get_providerids_to_apptids_hash(instance):

    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_file = "/data/mdstaff_appointment_" + instance + "_final.txt"
    #data_file = "/data/mdstaff_appointment_" + instance + "_temp.txt"    
    data_file = dir_path + data_file
    log_file = dir_path + api_const.log_file

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". Getting ID Mapping Table from " + data_file)

    # to get a hash of mdstaff and sccid, with sccid as the key
    id_hash = {}

    with open(data_file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter = "|")
        next(reader)
        for row in reader:
            apptid = row[1]
            providerid = row[0]
            id_hash[providerid] = apptid

    return(id_hash)


def main():
    id_hash = get_providerids_to_apptids_hash(instance)


if __name__ == "__main__":
    main()