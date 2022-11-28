#!/usr/bin/env python

import os
import time
import argparse

unixNow = time.time()
secInDay = 60 * 60 * 24


def cleanMJD(mjd, path, logPath, keepFor=30):
    """Clean an MJD worth of files,
       if the files are at utah.

       mjd: int, mjd to clean

       path: str, path to top level dir

       logPath: str, path to top level dir of utah files

       keepFor: int, days to keep files on disk
    """

    todayDir = os.path.join(path, str(mjd))

    if not os.path.isdir(todayDir):
        print(f"No data for {mjd}")
        return None

    files = os.listdir(todayDir)

    utahFileList = os.path.join(logPath, str(mjd))
    with open(utahFileList, "r") as of:
        lines = of.readlines()
        utahFiles = [l.strip() for l in lines]

    count = 0
    for f in files:
        if f not in utahFiles:
            # maybe email here?
            print("MISSING ", f)
            continue
        fullPath = os.path.join(todayDir, f)
        timeStamp = os.path.getmtime(fullPath)
        if (unixNow - timeStamp) / secInDay > keepFor:
            # os.remove(fullPath)
            # print(fullPath)
            count += 1
    print(f"removed {count} of {len(files)} files in {todayDir}")


def checkMJDs(path, logPath, keepFor=30):
    """check for new mjds

       path: str, path to top level prod dir

       cachePath: str, path to file summaries
    """

    mjds = os.listdir(path)
    for mjd in mjds:
        todayDir = os.path.join(path, str(mjd))

        timeStamp = os.path.getmtime(todayDir)
        if (unixNow - timeStamp) / secInDay < keepFor:
            continue

        files = os.listdir(todayDir)

        if len(files) > 0:
            cleanMJD(mjd, path, logPath, keepFor=keepFor)


if __name__ == "__main__":
    usage = "clean_mjd"
    description = "remove files for product if data at utah"
    parser = argparse.ArgumentParser(description=description, usage=usage)
    parser.add_argument("-m", "--mjd", dest="mjd", type=int,
                        required=False, help="mjd to clean",
                        default=None)
    parser.add_argument("-p", "--product", dest="prod", type=str,
                        required=True, help="product to clean")
    parser.add_argument("-r", "--root", dest="root", type=str,
                        required=False, help="product root, top level of mjds",
                        default=None)
    parser.add_argument("-l", "--log", dest="log", type=str,
                        required=False, help="path to logs from utah",
                        default="/data/logs/utahFiles")
    parser.add_argument("-k", "--keep", dest="keep", type=int,
                        required=False, help="days to keep files on disk",
                        default=30)

    args = parser.parse_args()
    mjd = args.mjd
    prod = args.prod
    root = args.root
    log = args.log
    keep = args.keep

    if not root:
        path = os.path.join("/data", prod)
    else:
        path = root

    logPath = os.path.join(log, prod)

    if mjd:
        cleanMJD(mjd, path, logPath, keepFor=keep)
    else:
        checkMJDs(path, logPath, keepFor=keep)
