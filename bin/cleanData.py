#!/usr/bin/env python

import os
from pathlib import Path
import time
import argparse
import json
from datetime import datetime, timezone

unixNow = time.time()
secInDay = 60 * 60 * 24

timeFstr = "%Y-%m-%d %H:%M:%S.%f %z"

def cleanMJD(mjd, dataRoot, logRoot, product, keepFor=30):
    """Clean an MJD worth of files,
       if the files are at utah.

       mjd: int, mjd to clean

       dataRoot: str, path to top level data dir

       logRoot: str, path to top level dir of utah files

       product: str, product to clean

       keepFor: int, days to keep files on disk
    """
    
    productRoot = os.path.join(dataRoot, product)
    productMjd = os.path.join(productRoot, str(mjd))
    timeStamp = os.path.getmtime(productMjd)
    if (unixNow - timeStamp) / secInDay < keepFor:
        print(f"skipping {productMjd}; too recent to clean")
        return

    countFiles = len(list(Path(productMjd).rglob("*")))

    todayDir = os.path.join(logRoot, str(mjd))
    prodJson = os.path.join(todayDir, f"{product}-{mjd}.json")

    utahFileList = json.load(open(prodJson))

    count = 0
    skipped = list()
    for f in utahFileList:
        localPath = os.path.join(dataRoot, f["location"])
        uTimeStamp = f["mtime"].replace("MDT","-0600").replace("MST","-0700")
        utahTime = datetime.strptime(uTimeStamp, timeFstr)
        try:
            timeStamp = os.path.getmtime(localPath)
            tzStamped = datetime.fromtimestamp(timeStamp, timezone.utc)
            delta = utahTime - tzStamped
        except FileNotFoundError:
            print(f"local file {f['location']} not found")
            continue
        if delta.microseconds == 0:
            os.remove(localPath)
            count += 1
        else:
            skipped.append(f["location"])
    print(f"removed {count} of {countFiles} files in {productMjd}")
    for fname in skipped:
        print(f"WARN: skipped {fname}")


def checkMJDs(dataRoot, logRoot, product, keepFor=30):
    """check for new mjds

       dataRoot: str, path to top level data dir

       logRoot: str, path to top level dir of utah files

       product: str, product to clean
    """

    mjds = os.listdir(logRoot)
    for mjd in mjds:
        productRoot = os.path.join(dataRoot, product)
        productMjd = os.path.join(productRoot, str(mjd))
        try:
            timeStamp = os.path.getmtime(productMjd)
        except FileNotFoundError:
            continue
        if (unixNow - timeStamp) / secInDay < keepFor:
            continue

        files = list(Path(productMjd).rglob("*"))

        if len(files) > 0:
            cleanMJD(mjd, dataRoot, logRoot, product, keepFor=keepFor)


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
                        required=False, help="data root",
                        default=None)
    parser.add_argument("-l", "--log", dest="log", type=str,
                        required=False, help="path to logs from utah",
                        default="/data/sas/summaries")
    parser.add_argument("-k", "--keep", dest="keep", type=int,
                        required=False, help="days to keep files on disk",
                        default=30)

    args = parser.parse_args()
    mjd = args.mjd
    product = args.prod
    root = args.root
    logRoot = args.log
    keep = args.keep

    if not root:
        dataRoot = "/data"
    else:
        dataRoot = root

    # logPath = os.path.join(log, prod)

    if mjd:
        cleanMJD(mjd, dataRoot, logRoot, product, keepFor=keep)
    else:
        checkMJDs(dataRoot, logRoot, product, keepFor=keep)
