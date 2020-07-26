import csv
import sys
sys.path.insert(1, '../util/')
sys.path.insert(2, "C:/OscarScripts/util")
from calendar_datetime import get_today_wkday
import os
import logging
import api_const

def get_sccids_to_providerids_hash(data_file = "/data/mdstaff_id_table_inpt_final.txt"):

    wkday = get_today_wkday()
    dir_path = os.path.dirname(os.path.realpath(__file__))
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
            sccid = row[1]
            provider_id = row[0]
            id_hash[sccid] = provider_id

    return(id_hash)


def main():
    id_hash = get_sccids_to_providerids_hash()


if __name__ == "__main__":
    main()