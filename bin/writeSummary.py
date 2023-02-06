#!/usr/bin/env python

import os
import argparse


def listMJD(mjd, path):
    """create file list for mjd dir

       mjd: int, mjd to clean

       path: str, path to top level prod dir
    """

    todayDir = os.path.join(path, str(mjd))

    files = os.listdir(todayDir)

    fileString = " \n".join(files)

    return fileString


def checkForNew(path, cachePath):
    """check for new mjds

       path: str, path to top level prod dir

       cachePath: str, path to file summaries
    """

    mjds = os.listdir(path)
    for mjd in mjds:
        fpath = os.path.join(cachePath, mjd)
        if not os.path.isfile(fpath):
            with open(fpath, "w") as sumFile:
                print(listMJD(mjd, path), file=sumFile)


if __name__ == "__main__":
    usage = "write_mjd_summary"
    description = "write all files for a given prod-mjd to summary file"
    parser = argparse.ArgumentParser(description=description, usage=usage)
    parser.add_argument("-p", "--product", dest="prod", type=str,
                        required=True, help="product to check")
    parser.add_argument("-o", "--obs", dest="obs", type=str,
                        required=True, help="product to check")

    args = parser.parse_args()
    prod = args.prod
    obs = args.obs

    sas_path = "/uufs/chpc.utah.edu/common/home/sdss50/sdsswork/data"
    staging_path = os.path.join(sas_path, "staging", obs , prod)
    summaries_path = os.path.join(sas_path, "summaries", obs , prod)
    checkForNew(staging_path, summaries_path)
