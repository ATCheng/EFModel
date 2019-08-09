#!/usr/bin/python
# -*- coding: utf-8 -*-

_ref_year_index = 7

_company_info_url = "https://mops.twse.com.tw/mops/web/t05st03"
_company_finance_report_url = "https://mops.twse.com.tw/mops/web/t163sb01"

_finance_income_report_preIFRSs_url = "https://mops.twse.com.tw/mops/web/t05st21"
_finance_income_report_postIFRSs_url = "https://mops.twse.com.tw/mops/web/t163sb17"
_finance_balance_report_preIFRSs_url = "https://mops.twse.com.tw/mops/web/t05st20"
_finance_balance_report_postIFRSs_url = "https://mops.twse.com.tw/mops/web/t163sb18"

def get_history_ref_year_index():
    return _ref_year_index

def get_company_info_url():
    return _company_info_url;

def get_finance_income_report_url(year):
    if year > 101:
        return _finance_income_report_postIFRSs_url
    else:
        return _finance_income_report_preIFRSs_url

def get_finance_balance_report_url(year):
    if year > 101:
        return _finance_balance_report_postIFRSs_url
    else:
        return _finance_balance_report_preIFRSs_url
