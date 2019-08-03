#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

_data_folder_path = "../data"
_company_info_file_name = "info.csv"
_finance_report_file_name = "history.csv"

def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__))

def create_data_folder():
    base = get_current_dir()
    data = "{}/{}".format(base, _data_folder_path)
    print("data folder path {}".format(data))
    is_exist = os.path.exists(data)
    if is_exist:
        print("data folder created")
    else:
        print("data folder not created")
        print("create data folder")
        os.mkdir(data)
        
def create_stock_folder(stock_id):
    base = get_current_dir()
    stock = "{}/{}/{}".format(base, _data_folder_path, stock_id)
    print("stock data path {}".format(stock))
    is_exist = os.path.exists(stock)
    if is_exist:
        print("stock id {} data folder created".format(stock_id))
    else:
        print("stock id {} data folder not created".format(stock_id))
        print("create stock id {} data folder".format(stock_id))
        os.mkdir(stock)
        
def get_stock_folder(stock_id):
    base = get_current_dir()
    stock = "{}/{}/{}".format(base, _data_folder_path, stock_id)
    print(stock)
    return stock
        
def create_folder(stock_id):
    create_data_folder()
    create_stock_folder(stock_id)
    
def get_file_path(stock_id, filename):
    path = "{}/{}".format(get_stock_folder(stock_id), filename)
    return path

def get_company_info_file_path(stock_id):
    path = "{}/{}".format(get_stock_folder(stock_id), _company_info_file_name)
    return path

def output_company_info_to_csv(stock_id, df):
    file_path = get_file_path(stock_id, _company_info_file_name)
    df.to_csv(file_path)
    print("save {}".format(file_path))
    return

def output_finance_report_to_csv(stock_id, df):
    file_path = get_file_path(stock_id, _finance_report_file_name)
    df.to_csv(file_path)
    print("save {}".format(file_path))
    return
        
if __name__ == "__main__":
    if len(sys.argv) == 2:
         create_folder(sys.argv[1])
    else:
        print("$ python file.py stock_id")
