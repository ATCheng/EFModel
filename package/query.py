#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import requests as request

from package.index import get_company_info_url
from package.index import get_finance_income_report_url
from package.index import get_finance_balance_report_url
from package.template import create_post_company_basic_data
from package.template import create_post_company_data
from package.template import create_info_df
from package.template import create_composite_income_df

def read_company_info(stock_id, dfs):
    for df in dfs:
        if df.empty:
            continue
    
        for row in df.itertuples():
            if str(row[1]) == "股票代號":
                stock_id = row[2]
                company_type = row[4]
                print("{}: {}, {}: {}".format(row[1], stock_id, row[3], company_type))
                info = create_info_df(stock_id, company_type)
                return info

def create_year_dataframe(lables, year, values):
    df = create_composite_income_df(year + 1911)
    
    is_pre = False
    pre_other_profit = 0
    pre_other_loss = 0
    for i in range(len(lables)):
        if lables[i].find("營業收入") == 0 or lables[i].find("淨收益") == 0:
            df.營業收入 = int(values[i])
            print("營業收入: {}".format(int(values[i])))
        elif lables[i].find("營業成本") == 0:
            df.營業成本 = int(values[i])
            print("營業成本: {}".format(int(values[i])))
        elif lables[i].find("營業毛利") == 0:
            df.營業毛利 = int(values[i])
            print("營業毛利: {}".format(int(values[i])))
        elif lables[i].find("營業費用") == 0:
            df.營業費用 = int(values[i])
            print("營業費用: {}".format(int(values[i])))
        elif lables[i].find("營業利益") == 0 or lables[i].find("營業淨利") == 0:
            df.營業利益 = int(values[i])
            print("營業利益: {}".format(int(values[i])))
        elif lables[i].find("營業外收入及支出") == 0:
            df.業外收支 = int(values[i])
            print("業外收支: {}".format(int(values[i])))
        elif lables[i].find("稅前淨利") == 0 or lables[i].find("繼續營業單位稅前淨利") == 0 or lables[i].find("繼續營業單位稅前合併淨利") == 0 or lables[i].find("繼續營業單位稅前損益") == 0:
            df.稅前淨利 = int(values[i])
            print("稅前淨利: {}".format(int(values[i])))
        elif lables[i].find("所得稅") == 0:
            df.所得稅 = abs(int(values[i]))
            print("所得稅: {}".format(abs(int(values[i]))))
        elif lables[i].find("本期淨利") == 0 or lables[i].find("繼續營業單位淨利") == 0 or lables[i].find("繼續營業單位稅後合併淨利") == 0 or lables[i].find("本期稅後淨利") == 0:
            df.本期淨利 = int(values[i])
            print("本期淨利: {}".format(int(values[i])))
        elif lables[i].find("本期綜合損益總額") == 0 or ((lables[i].find("合併總損益") == 0) and (lables[i].find("合併總損益歸屬予") == -1)):
            df.本期綜合損益 = int(values[i])
            print("本期綜合損益: {}".format(int(values[i])))
        elif lables[i].find("淨利（淨損）歸屬於母公司業主") == 0:
            df.業主淨利 = int(values[i])
            print("業主淨利: {}".format(int(values[i])))
        elif lables[i].find("母公司股東") == 0 and lables[i-1].find("合併總損益歸屬予") == 0:
            df.業主淨利 = int(values[i])
            print("業主淨利: {}".format(int(values[i])))
        elif lables[i].find("基本每股盈餘") == 0:
            df.基本每股盈餘 = values[i]
            print("基本每股盈餘: {}".format(values[i]))
        ### pre IFRSs
        elif lables[i].find("營業外收入及利益") == 0:
            is_pre = True
            pre_other_profit = int(values[i])
        elif lables[i].find("營業外費用及損失") == 0:
            pre_other_loss = int(values[i])
        else:
            continue

    if is_pre:
        other = pre_other_profit - pre_other_loss
        df.業外收支 = other
        print("業外收支: {}".format(other))

    if pd.isnull(df.loc[year+1911, "營業利益"]):
        profit = df.loc[year+1911, "營業收入"] - df.loc[year+1911, "營業費用"]
        df.營業利益 = profit
        print("營業利益: {}".format(profit))
    return df

def read_finance_data(stock_id, dfs, year):
    for df in dfs:
        if df.empty:
            continue

        columns = list(df.columns)
        if "{}年".format(year) in columns or "{}年度".format(year) in columns:
            data = create_year_dataframe(df[columns[0]].values, year, df[columns[3]].values)
            return data

def is_step2_needed(dfs):
    step2_needed = False

    for df in dfs:
        if step2_needed:
            break

        if df.empty:
            continue

        columns = list(df.columns)
        for column in columns:
            if "公司代號" in columns and "公司名稱" in columns:
                step2_needed = True
                break

    return step2_needed
                
def query_company_info(stock_id):
    url = get_company_info_url()
    data = create_post_company_basic_data(stock_id)
    print("post {} company info url: {}".format(stock_id, url))
    response = request.post(url, data)
    status = response.status_code
    print("status code: {}".format(status))
    if status != 200:
        return
    info = read_company_info(stock_id, pd.read_html(response.content))
    return info

def query_company_income_state(stock_id, year):
    url = get_finance_income_report_url(year)
    # step 1
    data = create_post_company_data(stock_id, year, 1)
    print("post {} finance report url: {}".format(stock_id, url))
    response = request.post(url, data)
    status = response.status_code
    print("status code: {}".format(status))
    if status != 200:
        return

    dfs = pd.read_html(response.content)
    if is_step2_needed(dfs):
        # step 2
        data = create_post_company_data(stock_id, year, 2)
        print("post {} finance report url: {}".format(stock_id, url))
        response = request.post(url, data)
        status = response.status_code
        print("status code: {}".format(status))
        if status != 200:
            return

    dfs = pd.read_html(response.content)
    results = read_finance_data(stock_id, dfs, year)
    return results
    
if __name__ == "__main__":
    query_company_info(2382)
    
