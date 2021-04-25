from os import path
import os
import yaml

import requests as req
import pandas as pd

# import time
import logging
logger = logging.getLogger(__name__)

import datetime


class covidReportUtil:
    def __init__(self, application_id):
        self._application_id = application_id

    
    def get_job_config(self):
        config_file = os.path.join(os.path.dirname('.'), 'config', f'{self._application_id}.yml')
        with open(config_file) as f_cfg:
            loader = yaml.load(f_cfg, Loader=yaml.UnsafeLoader)
            conf = loader.get(self._application_id)
        return conf
    
    
    def open_excel_file(self, file_path):
        return pd.read_excel(file_path, dtype=str)


    def get_date_and_iso_from_dataframe(self, df):
        return [{'date': r['date'][:10], 'iso': r['iso']} for r in df.to_dict('records')]
    
    def is_valid_date(self, date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except:
            return False
        
    
    def is_valid_iso_country(self, iso_country, iso_country_list):
        if iso_country in iso_country_list:
            return True
        else:
            return False
            

    def get_valid_list_by_date(self, params):
        valid_list = []
        invalid_list = []
        for param in params:
            if self.is_valid_date(param['date']):
                valid_list.append(param)
            else:
                invalid_list.append(param)
        return (valid_list, invalid_list)
    

    def is_valid_row(self, param, iso_country_list):
        if self.is_valid_date(param['date']) and self.is_valid_iso_country(param['iso'], iso_country_list):
            return True
        else:
            return False
        
        
    def call_api(self, api_url, param):
        resp = req.get(api_url, param)
        if resp.json().get('error', '') != '':
            logger.error(f'error processing with arguments: {api_url, param, resp.json()}')
            return None
        return resp.json()

    
    def get_api_result(self, resp_data, stat_column, except_province='Recovered'):
        if resp_data == None:
            return None
        if not except_province:
            return dict((d['region']['province'], d[stat_column]) for d in resp_data['data'])
        else:
            return dict((d['region']['province'], d[stat_column]) for d in resp_data['data'] if d['region']['province'] != except_province)

