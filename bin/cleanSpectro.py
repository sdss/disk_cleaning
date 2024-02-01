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

def cleanMJD(mjd, dataRoot, archiveRoot, product, keepFor=30):
    """Clean an MJD worth of files,
       if the files are at utah.

       mjd: int, mjd to clean

       dataRoot: str, path to top level data dir

       archiveRoot: str, path to top level dir of archive files

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

    todayDir = os.path.join(archiveRoot, str(mjd))

    archiveList = os.listdir(todayDir)

    count = 0
    missing = 0
    for f in archiveList:
        localPath = os.path.join(productMjd, f)
        if os.path.isfile(localPath):
            # print(localPath)
            try:
                os.remove(localPath)
            except PermissionError:
                print("FAIL FYI", localPath)
            count += 1
        else:
            missing += 1
    print(f"removed {count} of {countFiles} files in {productMjd}")
    if missing:
        print(f"MISSING {missing} for {productMjd}")


def checkMJDs(dataRoot, archiveRoot, product, keepFor=30):
    """check for new mjds

       dataRoot: str, path to top level data dir

       archiveRoot: str, path to top level dir of archive files

       product: str, product to clean
    """

    mjds = os.listdir(archiveRoot)
    for mjd in mjds:
        try:
            if int(mjd) > 60000:
                continue
        except ValueError as E:
            print(f"IGNORING {mjd}, b/c {E}")
            continue
        productRoot = os.path.join(dataRoot, product)
        productMjd = os.path.join(productRoot, str(mjd))
        try:
            timeStamp = os.path.getmtime(productMjd)
        except FileNotFoundError:
            continue
        if (unixNow - timeStamp) / secInDay < keepFor:
            continue

        cleanMJD(mjd, dataRoot, archiveRoot, product, keepFor=keepFor)
            


if __name__ == "__main__":
    product = 'spectro'
    archiveRoot = '/archive/spectro'
    keep = 250

    dataRoot = "/data"

    checkMJDs(dataRoot, archiveRoot, product, keepFor=keep)
