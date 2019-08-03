#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import requests as request

import package.index as index
from package.template import get_post_info_data
from package.template import get_post_finance_data
from package.template import create_info_df
from package.template import create_finance_report_df

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

def read_finance_data(company_type_id, stock_id, dfs, year):
    result = create_finance_report_df(company_type_id)
    result.loc[0, '年度'] = year + 1911
    
    for df in dfs:
        if df.empty:
            continue

        for row in df.itertuples():
            ####
            # check finance report opinion
            ####
            if str(row[1]) == "合併財務報告-意見種類：":
                opinion_type = row[1]
                opinion_result = row[2]
                print("{}{}".format(opinion_type, opinion_result))

            ####
            # get finance income report items
            ####
            elif str(row[1]) == "營業收入":
                total_income = row[2]
                print("營業收入: {}".format(total_income))
                result.loc[0, '營業收入'] = total_income
            elif str(row[1]) == "營業成本":
                cost = row[2]
                print("營業成本: {}".format(cost))
                result.loc[0, '營業成本'] = cost
            elif str(row[1]) == "營業毛利（毛損）淨額":
                gross = row[2]
                print("營業毛利: {}".format(gross))
                result.loc[0, '營業毛利'] = gross
            elif str(row[1]) == "營業費用" == 0:
                fee = row[2]
                print("營業費用: {}".format(fee))   
                result.loc[0, '營業費用'] = fee
            elif str(row[1]) == "營業外收入及支出":
                other = row[2]
                print("營業外收入及支出: {}".format(other))  
                result.loc[0, '業外收支'] = other
            elif str(row[1]) == "稅前淨利（淨損）":
                pre_tax_profit = row[2]
                print("稅前淨利: {}".format(pre_tax_profit))    
                result.loc[0, '稅前淨利'] = pre_tax_profit
            elif str(row[1]) == "所得稅費用（利益）":
                tax = row[2]
                print("所得稅: {}".format(tax))     
                result.loc[0, '所得稅'] = tax
            elif str(row[1]) == "本期淨利（淨損）":
                net_profit = row[2]
                print("本期淨利: {}".format(net_profit))   
                result.loc[0, '本期淨利'] = net_profit
            elif str(row[1]) == "本期綜合損益總額":
                total_profit = row[2]
                print("本期綜合損益: {}".format(total_profit))  
                result.loc[0, '本期綜合損益'] = total_profit
            elif str(row[1]) == "淨利（淨損）歸屬於母公司業主":
                shareholder_profit = row[2]
                print("業主淨利: {}".format(shareholder_profit))   
                result.loc[0, '業主淨利'] = shareholder_profit
            elif str(row[1]) == "基本每股盈餘（元）":
                eps = row[2]
                print("基本每股盈餘: {}".format(eps))  
                result.loc[0, '基本每股盈餘'] = eps
            elif str(row[1]) == "權益總計":
                total_interests = row[2]
                print("權益總計: {}".format(total_interests))
                result.loc[0, '權益總計'] = total_interests
            elif str(row[1]) == "每股淨值（元）＝（權益－非控制權益）／（普通股股數＋特別股股數（權益項下）＋預收股款（權益項下）之約當發行股數－母公司暨子公司持有之母公司庫藏股股數－待註銷股本股數）":
                net_value_per_share = row[2]
                print("每股淨值（元）: {}".format(net_value_per_share))
                result.loc[0, '每股淨值'] = net_value_per_share
            elif str(row[1]) == "流動資產":
                flow_assets = row[2]
                print("流動資產: {}".format(flow_assets))
                result.loc[0, '流動資產'] = flow_assets
            elif str(row[1]) == "非流動資產":
                non_flow_assets = row[2]
                print("非流動資產: {}".format(non_flow_assets))
                result.loc[0, '非流動資產'] = non_flow_assets
            elif str(row[1]) == "流動負債":
                flow_liabilities = row[2]
                print("流動負債: {}".format(flow_liabilities))
                result.loc[0, '流動負債'] = flow_liabilities
            elif str(row[1]) == "非流動負債":
                non_flow_liabilities = row[2]
                print("非流動負債: {}".format(non_flow_liabilities))
                result.loc[0, '非流動負債'] = non_flow_liabilities
            elif str(row[1]) == "股本":
                total_share_value = row[2]
                print("股本: {}".format(total_share_value))
                result.loc[0, '股本'] = total_share_value
    return result
                
def post_company_info(stock_id):
    data = get_post_info_data(stock_id)
    print("post {} company info: {}".format(stock_id, index._company_info_url))
    response = request.post(index._company_info_url, data)
    status = response.status_code
    print("status code: {}".format(status))
    if status != 200:
        return
    info = read_company_info(stock_id, pd.read_html(response.content))
    return info

def post_company_finance_report(company_type_id, stock_id, year):
    data = get_post_finance_data(company_type_id, stock_id, year)
    print("post {} finance report: {}".format(stock_id, index._company_finance_report_url))
    response = request.post(index._company_finance_report_url, data)
    status = response.status_code
    print("status code: {}".format(status))
    if status != 200:
        return
    data = read_finance_data(company_type_id, stock_id, pd.read_html(response.content), year)
    return data
    
if __name__ == "__main__":
    post_company_info(2382)
    
