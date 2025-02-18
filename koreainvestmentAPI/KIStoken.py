import json
import requests
import yaml
from datetime import datetime
import pandas as pd

class API:
    def __init__(self, filepath = str) -> None:
        self.filepath = filepath
        with open(file=f"{filepath}/config.yaml", encoding='UTF-8') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        self.__APP_KEY__ = cfg['APP_KEY']
        self.__APP_SECRET__ = cfg['APP_SECRET']
        self.__CANO__ = cfg['CANO']
        self.__ACNT_PRDT_CD__ = cfg['ACNT_PRDT_CD']
        self.URL_BASE = ""
        # 날짜 계산
        self.today = datetime.now()
        self.date_format = "%Y%m%d"


    def __get_new_access_token(self):
        """토큰 발급"""
        headers = {"content-type":"application/json"}
        body = {
            "grant_type":"client_credentials",
            "appkey":self.__APP_KEY__, 
            "appsecret":self.__APP_SECRET__
        }
        PATH = "oauth2/tokenP"
        URL = f"{self.URL_BASE}/{PATH}"
        res = requests.post(URL, headers=headers, data=json.dumps(body)).json()
        try:
            self.__ACCESS_TOKEN__ = res["access_token"]
            self.save_access_token()
        except:
            print(res['error_description'])
            exit()

    def revoke_token(self):
        """토큰 폐기"""
        headers = {"content-type":"application/json"}
        body = {
                "appkey":self.__APP_KEY__, 
                "appsecret":self.__APP_SECRET__,
                "token" : self.__ACCESS_TOKEN__
                }
        PATH = "/oauth2/revokeP"
        URL = f"{self.URL_BASE}/{PATH}"
        res = requests.post(URL, headers=headers, data=json.dumps(body))
        print(res.json()["message"])

    def hashkey(self, datas):
        """암호화"""
        PATH = "uapi/hashkey"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
            'content-Type' : 'application/json',
            'appKey' : self.__APP_KEY__,
            'appSecret' : self.__APP_SECRET__
        }
        res = requests.post(URL, headers=headers, data=json.dumps(datas))
        hashkey = res.json()["HASH"]
        return hashkey
    
    def save_access_token(self):
        today_access_token = self.__ACCESS_TOKEN__
        date = self.today.strftime(self.date_format)

        data = {
            'date': [date],
            'token' : [today_access_token]
        }
        data = pd.DataFrame(data)

        data.to_csv(f"{self.filepath}/token.csv")

    def __load_access_token(self):
        df = pd.read_csv(
            filepath_or_buffer=f"{self.filepath}/token.csv",
            header=0,
            dtype={
                "date" : str,
                "token" : str
            }
        )
        if self.today.strftime(self.date_format) == df['date'][0]:
            self.__ACCESS_TOKEN__ = df['token'][0]
        else:
            self.__get_new_access_token()
