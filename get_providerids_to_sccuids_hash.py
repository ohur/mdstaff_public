import csv
import sys
sys.path.insert(1, '../util/')
sys.path.insert(2, "C:/OscarScripts/util")
from calendar_datetime import get_today_wkday
import os
import logging
import api_const

def get_providerids_to_sccuids_hash(data_file = "demographic_providerids_sccin_final.txt"):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_file = dir_path + api_const.log_file
   
    if data_file == "demographic_providerids_sccin_final.txt":
        data_file = dir_path + "/data/" + data_file    
    
    wkday = get_today_wkday()   

    logging.basicConfig(
        filename = log_file, \
        filemode = 'a', \
        level = logging.INFO, \
        format = "%(levelname)s %(name)s %(asctime)s %(lineno)s - %(message)s ")
    logger = logging.getLogger(__name__)
    logger.info(wkday + ". Getting ProviderID and SCCID Mapping Table from " + data_file)

    # to get a hash of mdstaff and sccid, with sccid as the key and mdstaff as values
    id_hash = {}

    with open(data_file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter = "|")
        next(reader)
        for row in reader:
            providerid = row[0]
            sccuid = row[1]
            id_hash[providerid] = sccuid

    return(id_hash)


def main():
    id_hash = get_providerids_to_sccuids_hash(data_file = "demographic_providerids_sccin_final.txt")


if __name__ == "__main__":
    main()