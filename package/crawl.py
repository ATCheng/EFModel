#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from datetime import date

from package.index import get_history_ref_year_index
from package.file import create_folder
from package.query import query_company_info
from package.query import query_company_income_state
from package.file import get_company_info_file_path
from package.file import output_company_info_to_csv
from package.file import output_income_state_to_csv
from package.file import output_balance_sheet_to_csv
from package.template import get_finance_template_type_id


def get_company_type_id(stock_id):
    df = pd.read_csv(get_company_info_file_path(stock_id))
    return get_finance_template_type_id(df.產業類別[0])
    
def crawl_company_info(stock_id):
    print("crawl company information...")
    info = query_company_info(stock_id)
    output_company_info_to_csv(stock_id, info)

def crawl_company_income_state(stock_id):
    # get history year index
    this_year = date.today().year - 1911
    years = list(range(this_year - get_history_ref_year_index(), this_year))
    print("crawl {} yearly history data: {}".format(stock_id, years))
    
    dfs = list()
    for year in years:
        print("crawl {} composite income report...".format(year))
        data = query_company_income_state(stock_id, year)
        dfs.append(data)

    output_income_state_to_csv(stock_id, pd.concat(dfs, ignore_index=False, sort=False))

def crawl_company_balance_sheet(stock_id):
    #output_balance_sheet_to_csv(stock_id, )
    return

def crawl_finance_data(stock_id):
    create_folder(stock_id)
    print("start crawling {} data...".format(stock_id))
    crawl_company_info(stock_id)
    crawl_company_income_state(stock_id)
    crawl_company_balance_sheet(stock_id)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        crawl_finance_data(sys.argv[1])
    else:
        print("$ python crawl.py stock_id")
