from os import path
import os
import yaml
import requests as req
import pandas as pd
import time
import datetime
from covidreport_util import covidReportUtil

import logging
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    application_id = 'covidreport'
    util = covidReportUtil(application_id)
    conf = util.get_job_config()

    # Set Config Variables from config file
    excel_driver_path = conf['excel_driver_path']
    api_url = conf['api_url']
    iso_country_path = conf['iso_country_path']
    excel_ouput_path = conf['excel_ouput_path']
    summary_columns = conf['summary_columns']

    # Read (date and iso) list file into dataframe
    df = util.open_excel_file(excel_driver_path)

    # Return (date and iso) records in dictionary form: {'date': 'yyyy-mm-dd', 'iso': 'USA'}
    params = util.get_date_and_iso_from_dataframe(df)

    # Read valid iso list file
    df_iso = util.open_excel_file(iso_country_path)
    iso_country_list = df_iso['iso_country'].to_list()


    # First filter out valid and unvalid lists
    # Invalid List - bad iso country code or invalid date format (YYYY-MM-DD)
    valid_list = []
    invalid_list = []
    for param in params:
        if util.is_valid_row(param, iso_country_list):
            valid_list.append(param)
        else:
            invalid_list.append(param)

    # Log invalid rows
    for v in invalid_list:
        logger.error(f'error processing with arguments: {v}')


    # For valid rows, get confirmed, deaths, recovered counts from api
    result_stats = []
    for v in valid_list:
        resp_data = util.call_api(api_url, v)
        if resp_data == None:
            logger.error(f'error processing with arguments: {v}')
        else:
            for c in summary_columns:
                v.update({c:sum(util.get_api_result(resp_data, c).values())})

        result_stats.append(v)


    # Write output to excel
    df_result = pd.DataFrame(result_stats)
    df_result.to_excel(excel_ouput_path, index=None)

