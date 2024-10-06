import scrapy
from typing import Any
import unicodedata
import json
import pandas as pd
from urllib.parse import quote

class FinancialsSpider(scrapy.Spider):

    name = "financials"
    start_urls=[
        'https://www.nasdaq.com/market-activity/stocks/a/financials'
    ]
    headers = { 
            'Accept':'application/json',
            }

    def parse(self,response):
        df = pd.read_csv('nasdaq_screener.csv')
        for i in df['Symbol']:
            url = 'https://api.nasdaq.com/api/company/'+str(i).strip()+'/financials?frequency=1'        
            encoded_url = quote(url, safe=':/?=&')
            request = scrapy.Request(encoded_url,headers=self.headers,callback=self.parse_data)
            yield request

    def parse_data(self,response):
        raw_data = response.body
        data = json.loads(raw_data)['data']
        # print(data['symbol'])
        
        result={}
        result['symbol'] = data['symbol']
        headers = data['incomeStatementTable']['headers']
        h_values = list(headers.values())
        result[f'{h_values[0]}'] = h_values[1:]
        inc_stat_tb = data['incomeStatementTable']['rows']
        bal_sht = data['balanceSheetTable']['rows']
        for row in inc_stat_tb:
            r_values = list(row.values())
            print(r_values)
            result[f'{r_values[0]}'] = r_values[1:]
        for row in bal_sht:
            r_values = list(row.values())
            print(r_values)
            result[f'{r_values[0]}'] = r_values[1:]

        yield result

        

    # def parse_api(self,response):
    #     raw_data = response.body
    #     data = json.loads(raw_data)