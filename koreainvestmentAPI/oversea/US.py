import json
import requests
import time
import yaml
from ...kis_token import API

class API(API):
    def __init__(self, config_file=str) -> None:
        super().__init__(config_file)
        self.URL_BASE = "https://openapi.koreainvestment.com:9443"
        self.get_access_token()

    def get_current_price(self, market=str, code=str):
        """현재가 조회"""
        PATH = "uapi/overseas-price/v1/quotations/price"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
                "Content-Type":"application/json", 
                "authorization": f"Bearer {self.__ACCESS_TOKEN}",
                "appKey":self.__APP_KEY,
                "appSecret":self.__APP_SECRET,
                "tr_id":"HHDFS00000300"
                }
        params = {
            "AUTH": "",
            "EXCD":market,
            "SYMB":code,
        }
        res = requests.get(URL, headers=headers, params=params)
        return float(res.json()['output']['last'])
    
    def get_asset_balance(self):
        """주식 잔고조회"""
        PATH = "uapi/overseas-stock/v1/trading/inquire-balance"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {"Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN}",
            "appKey":self.__APP_KEY,
            "appSecret":self.__APP_SECRET,
            "tr_id": "TTTS3012R",
            "custtype":"P"
        }
        params = {
            "CANO": self.__CANO,
            "ACNT_PRDT_CD": self.__ACNT_PRDT_CD,
            "OVRS_EXCG_CD": "NASD",
            "TR_CRCY_CD": "USD",
            "CTX_AREA_FK200": "",
            "CTX_AREA_NK200": ""
        }
        res = requests.get(URL, headers=headers, params=params)
        stock_list = res.json()['output1']
        stock_dict = {}
        for stock in stock_list:
            if int(stock['ovrs_cblc_qty']) > 0:
                stock_dict[stock['ovrs_pdno']] = stock['ovrs_cblc_qty']
        
        return stock_dict
    
    def get_cash_balance(self):
        """현금 잔고조회"""
        PATH = "uapi/overseas-stock/v1/trading/inquire-present-balance"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN}",
            "appKey":self.__APP_KEY,
            "appSecret":self.__APP_SECRET,
            "tr_id" : "CTRP6504R",
            "custtype" : "P"
            }
        params = {
            "CANO" : self.__CANO,
            "ACNT_PRDT_CD" : self.__ACNT_PRDT_CD,
            "WCRC_FRCR_DVSN_CD" : "02",
            "NATN_CD" : "840",
            "TR_MKET_CD" : "00",
            "INQR_DVSN_CD" : "01"
        }
        res = requests.get(URL, headers=headers, params=params).json()
        print(res['msg1'])
        cash = res['output3']['dncl_amt']
        return float(cash)
    
    def get_total_evaluation(self):
        PATH = "uapi/overseas-stock/v1/trading/inquire-present-balance"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN}",
            "appKey":self.__APP_KEY,
            "appSecret":self.__APP_SECRET,
            "tr_id" : "CTRP6504R",
            "custtype" : "P"
            }
        params = {
            "CANO" : self.__CANO,
            "ACNT_PRDT_CD" : self.__ACNT_PRDT_CD,
            "WCRC_FRCR_DVSN_CD" : "02",
            "NATN_CD" : "840",
            "TR_MKET_CD" : "00",
            "INQR_DVSN_CD" : "01"
        }
        res = requests.get(URL, headers=headers, params=params)
        total_evaluation = res.json()['output3']['tot_asst_amt']
        print(f"총 자산 : {total_evaluation}")
        return total_evaluation
    
    def buy(self, market=str, code=str, qty=int):
        """미국 주식 시장가 매수"""
        PATH = "uapi/overseas-stock/v1/trading/order"
        URL = f"{self.URL_BASE}/{PATH}"
        price = self.get_current_price(market=market, code=code)
        cash = self.get_cash_balance()
        while qty*price > cash:
            qty -= 1
        if qty == 0:
            print('[매수 실패] : 잔고 부족')
            return False
        data = {
            "CANO": self.__CANO,
            "ACNT_PRDT_CD": self.__ACNT_PRDT_CD,
            "OVRS_EXCG_CD": market,
            "PDNO": code,
            "ORD_DVSN": "00",
            "ORD_QTY": str(qty),
            "OVRS_ORD_UNPR": f"{round(price,2)}",
            "ORD_SVR_DVSN_CD": "0"
        }
        headers = {"Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN}",
            "appKey": self.__APP_KEY,
            "appSecret": self.__APP_SECRET,
            "tr_id": "TTTT1002U",
            "custtype":"P",
            "hashkey" : self.hashkey(data)
        }
        res = requests.post(URL, headers=headers, data=json.dumps(data))
        res = res.json()
        if res['rt_cd'] == '0':
            print(f"[매수 성공] {code} {res['msg1']}")
            return True
        else:
            print(f"[매수 실패] {code} {res['msg1']}") 
            return False
        
    def sell(self, market=str, code=str, qty=int):
        """미국 주식 지정가 매도"""
        PATH = "uapi/overseas-stock/v1/trading/order"
        URL = f"{self.URL_BASE}/{PATH}"
        price = self.get_current_price
        data = {
            "CANO": self.__CANO,
            "ACNT_PRDT_CD": self.__ACNT_PRDT_CD,
            "OVRS_EXCG_CD": market,
            "PDNO": code,
            "ORD_DVSN": "00",
            "ORD_QTY": str(qty),
            "OVRS_ORD_UNPR": f"{round(price,2)}",
            "ORD_SVR_DVSN_CD": "0"
        }
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN}",
            "appKey":self.__APP_KEY,
            "appSecret":self.__APP_SECRET,
            "tr_id": "TTTT1006U",
            "custtype":"P",
            "hashkey" : self.hashkey(data)
        }
        res = requests.post(URL, headers=headers, data=json.dumps(data))
        res = res.json()
        if res['rt_cd'] == '0':
            print(f"[매도 성공]{res['msg1']}")
            return True
        else:
            print(f"[매도 실패]{res['msg1']}")
            return False
    
    def get_exchange_rate(self):
        """환율 조회"""
        PATH = "uapi/overseas-stock/v1/trading/inquire-present-balance"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
                "Content-Type":"application/json", 
                "authorization": f"Bearer {self.__ACCESS_TOKEN}",
                "appKey":self.__APP_KEY,
                "appSecret":self.__APP_SECRET,
                "tr_id":"CTRP6504R"}
        params = {
            "CANO": self.__CANO,
            "ACNT_PRDT_CD": self.__ACNT_PRDT_CD,
            "OVRS_EXCG_CD": "NASD",
            "WCRC_FRCR_DVSN_CD": "01",
            "NATN_CD": "840",
            "TR_MKET_CD": "01",
            "INQR_DVSN_CD": "00"
        }
        res = requests.get(URL, headers=headers, params=params)
        try :
            exchange_rate = float(res.json()['output2'][0]['frst_bltn_exrt'])
        except:
            exchange_rate = 1300.
        return exchange_rate