#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from package.crawl import crawl_finance_data

def main():
    if len(sys.argv) == 2:
        crawl_finance_data(sys.argv[1])
    else:
        print("$ python run.py stock_id")

if __name__ == "__main__":
    main()
