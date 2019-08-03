#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from datetime import date

import package.index as index
from package.file import create_folder
from package.file import get_company_info_file_path
from package.file import output_company_info_to_csv
from package.file import output_finance_report_to_csv
from package.query import post_company_info
from package.query import post_company_finance_report
from package.template import get_finance_template_type_id


def get_company_type_id(stock_id):
    df = pd.read_csv(get_company_info_file_path(stock_id))
    return get_finance_template_type_id(df.產業類別[0])
    
def crawl_company_info(stock_id):
    info = post_company_info(stock_id)
    output_company_info_to_csv(stock_id, info)
    return

def crawl_company_finance_report(stock_id):
    # get history year index
    this_year = date.today().year - 1911
    years = list(range(this_year-index._ref_year_index, this_year))
    print("crawl {} yearly history data: {}".format(stock_id, years))
    
    # get company type id
    type_id = get_company_type_id(stock_id)
    
    dfs = list()
    for year in years:
        if type_id == 0:
            data = post_company_finance_report(0, stock_id, year)
        elif type_id == 1:
            data = post_company_finance_report(1, stock_id, year)
        else:
            print("warn: invalid company type id {}".format(type_id))
        dfs.append(data)

    output_finance_report_to_csv(stock_id, pd.concat(dfs))
    return

def crawl_finance_data(stock_id):
    create_folder(stock_id)
    print("start crawling {} data...".format(stock_id))
    crawl_company_info(stock_id)
    crawl_company_finance_report(stock_id)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        crawl_finance_data(sys.argv[1])
    else:
        print("$ python crawl.py stock_id")
