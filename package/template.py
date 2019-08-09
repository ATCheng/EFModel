#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd

# post company info and finance reposts data
post_company_data_items = ['encodeURIComponent', 'step', 'firstin', 'off',
    'isnew',
    'co_id',
    'year',
    'TYPEK',
    'queryName',
    'inpuType',
    't05st29_c_ifrs',
    't05st30_c_ifrs',
    'check_2858']

#### company info file saved items
company_info_items = ['股票代號', '產業類別']
#### company finance report file saved items
composite_income_items = [
    #'年度',
    #####
                            #'流動資產',
                            #'非流動資產',
                            #'流動負債',
                            #'非流動負債',
    #####
                            #'股本',
                            #'權益總計',
                            #'每股淨值',
    #'股東權益報酬',
    ####
    '營業收入',
    '營業成本',
    '營業毛利',
    '營業費用',
    '營業利益',
    '業外收支',
    '稅前淨利',
    '所得稅',
    '本期淨利',
    '本期綜合損益',
    '業主淨利',
    '基本每股盈餘']

def create_post_company_basic_data(stock_id):
    data = dict.fromkeys(post_company_data_items)
    data['encodeURIComponent'] = 1
    data['step'] = 1
    data['firstin'] = 1
    data['off'] = 1
    data['TYPEK'] = 'all'
    data['queryName'] = stock_id
    data['co_id'] = stock_id
    data['inpuType'] = stock_id
    print("created post data {}".format(data))
    return data

def create_post_company_data(stock_id, year, step):
    data = dict.fromkeys(post_company_data_items)

    data['encodeURIComponent'] = 1
    data['firstin'] = 1
    data['isnew'] = 'false'
    data['co_id'] = int(stock_id)
    data['year'] = year
    # after 101, post IFRSs
    if year > 101:
        data['step'] = step
        if step == 1:
            data['off'] = 1
            data['TYPEK'] = 'all'
            data['queryName'] = stock_id
            data['inpuType'] = stock_id
            data['t05st29_c_ifrs'] = 'N'
            data['t05st30_c_ifrs'] = 'N'
        elif step == 2:
            data['TYPEK'] = 'sii'
        else:
            print("warn: post step 3 data is not supported.")
    # pre 101, pre IFRSs
    else:
        # preIFRSs, step is all 1
        data['step'] = 1
        data['off'] = 1
        #data['TYPEK'] = 'all'
        data['t05st29_c_ifrs'] = 'N'
        data['t05st30_c_ifrs'] = 'N'
        data['queryName'] = stock_id
        data['inpuType'] = stock_id
        if step == 2:
            data['check2858'] = 'Y'

    print("created post data {}".format(data))
    return data


def get_post_finance_data(company_type_id, stock_id, year):
    if company_type_id == 0:
        print("{} is a normal type company".format(stock_id))
        data = dict.fromkeys(post_company_data_items)
        data['encodeURIComponent'] = 1
        data['step'] = 1
        data['firstin'] = 1
        data['off'] = 1
        data['TYPEK'] = 'all'
        data['queryName'] = stock_id
        data['co_id'] = stock_id
        data['inpuType'] = stock_id
        data['isnew'] = 'false'
        data['year'] = year
        data['season'] = 4
        print("created post data {}".format(data))
    elif company_type_id == 1:
        print("{} is a financial insurance company".format(stock_id))
        data = dict.fromkeys(post_company_data_items)
        data['encodeURIComponent'] = 1
        data['step'] = 1
        data['firstin'] = 1
        data['co_id'] = stock_id
        data['isnew'] = 'false'
        data['year'] = year
        data['season'] = 4
        data['check2858'] = 'Y'
        print("created post data {}".format(data)) 
    else:
        print("warn: invalid company type id {}".format(company_type_id))
    return data

def create_info_df(stock_id, company_type):
    data = [[stock_id, company_type]]
    df = pd.DataFrame(data, columns = company_info_items)
    print("create company info dataframe template: \n{}".format(df))
    return df
    
def create_composite_income_df(year):
    data = pd.DataFrame(index = [year], columns = composite_income_items)
    print("create composite income report dataframe template: {}".format(data))
    return data
    
def get_finance_template_type_id(company_type):
    if company_type == "金融保險業":
        return 1
    else:
        return 0

if __name__ == "__main__":
    get_post_data(2382)
    
