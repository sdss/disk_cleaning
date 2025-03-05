#!/usr/bin/env python

import os
from pathlib import Path
import time

unixNow = time.time()
secInDay = 60 * 60 * 24

timeFstr = "%Y-%m-%d %H:%M:%S.%f %z"

def cleanProduct(productDir, keep_for=30):
    """Clean an MJD worth of files,
       if the files are at utah.

       product_root: str, root of product dir

       product: str, product to clean

       keepFor: int, days to keep files on disk
    """

    count = 0
    skipped = 0

    subdirs = list()
    print(f"cleaning {productDir}")
    
    for path in Path(productDir).glob("*"):
        if os.path.isdir(path):
            subdirs.append(path)
            continue
        timeStamp = os.path.getmtime(path)
        if (unixNow - timeStamp) / secInDay < keep_for:
            skipped += 1
            continue
        count +=1
        os.remove(localPath)
    print(f"cleaned {count} from {productDir}")
    
    return subdirs


if __name__ == "__main__":
    product_root = '/data/logs/'
    products = [
        "cerebro",
        "completionStatus",
        "flicamera",
        "hartmann",
        "jaeger",
        "roboscheduler",
        "timetracking",
        "yao",
        "actors",
        "tron",
        "cleanup"
    ]

    contains_products = []

    for product in products:
        productDir = os.path.join(product_root, product)
        sub_dirs = cleanProduct(productDir, keep_for=30)
        contains_products.extend(sub_dirs)

    while len(contains_products) > 0:
        remaining_products = []
        for productDir in contains_products:
            sub_dirs = cleanProduct(productDir, keep_for=30)
            remaining_products.extend(sub_dirs)
        contains_products = remaining_products
