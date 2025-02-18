import json
import requests
import time
from koreainvestmentAPI.KIStoken import API
from datetime import timedelta

class API(API):
    def __init__(self, filepath=str) -> None:
        super().__init__(filepath)
        self.URL_BASE = "https://openapi.koreainvestment.com:9443"

        # access token 불러오기
        try:
            self.__load_access_token()
        except:
            self.__get_new_access_token()
        
    
    def get_current_price(self, code):
        """현재가 조회"""
        PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {"Content-Type":"application/json", 
                "authorization": f"Bearer {self.__ACCESS_TOKEN__}",
                "appKey":self.__APP_KEY__,
                "appSecret":self.__APP_SECRET__,
                "tr_id":"FHKST01010100"}
        params = {
        "fid_cond_mrkt_div_code":"J",
        "fid_input_iscd":code,
        }
        res = requests.get(URL, headers=headers, params=params)
        result = res.json()['output']['stck_prpr']
        result = int(result)
        return result
    
    def get_asset_balance(self):
        PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {"Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN__}",
            "appKey":self.__APP_KEY__,
            "appSecret":self.__APP_SECRET__,
            "tr_id": "TTTC8434R",
            "custtype":"P",
        }
        params = {
            "CANO": self.__CANO__,
            "ACNT_PRDT_CD": self.__ACNT_PRDT_CD__,
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "02",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "01",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        res = requests.get(URL, headers=headers, params=params).json()

        """===================주식 잔고조회========================"""
        stock_list = res['output1']
        stock_dict = {}
        print(f"====주식 보유잔고====")
        for stock in stock_list:
            if int(stock['hldg_qty']) > 0:
                stock_dict[stock['pdno']] = int(stock['hldg_qty'])
                print(f"{stock['prdt_name']}({stock['pdno']}): {stock['hldg_qty']}주")
                time.sleep(0.1)
        """stock_dict[종목코드] = 주식수"""

        """=======================총 평가금액 조회===================""" 
        evaluation = res["output2"]
        total_evaluation = int(evaluation[0]['tot_evlu_amt'])
        print(f"평가가치 : {total_evaluation} 원")

        return stock_dict, total_evaluation
    
    def get_cash_balance(self):
        """현금 잔고조회"""
        PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {"Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN__}",
            "appKey":self.__APP_KEY__,
            "appSecret":self.__APP_SECRET__,
            "tr_id": "TTTC8434R",
            "custtype":"P",
        }
        params = {
            "CANO": self.__CANO__,
            "ACNT_PRDT_CD": self.__ACNT_PRDT_CD__,
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "02",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "01",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        res = requests.get(URL, headers=headers, params=params)
        cash = int(res.json()['output2'][0]['prvs_rcdl_excc_amt'])
        print(f"주문 가능 현금 잔고: {cash}원")
        return cash
    
    def buy(self, code, qty)-> None:
        """주식 시장가 매수"""  
        PATH = "uapi/domestic-stock/v1/trading/order-cash"
        URL = f"{self.URL_BASE}/{PATH}"

        self.get_cash_balance()

        data = {
            "CANO": self.__CANO__,
            "ACNT_PRDT_CD": self.__ACNT_PRDT_CD__,
            "PDNO": code,
            "ORD_DVSN": "01",
            "ORD_QTY": str(qty),
            "ORD_UNPR": "0",
        }
        headers = {"Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN__}",
            "appKey":self.__APP_KEY__,
            "appSecret":self.__APP_SECRET__,
            "tr_id": "TTTC0802U",
            "custtype":"P",
            "hashkey" : ""
        }

        while True:
            headers["hashkey"] = self.hashkey(data)
            res = requests.post(URL, headers=headers, data=json.dumps(data)).json()
            print(res['msg1'])
            
            if res['rt_cd'] == '0':
                print(f"[매수 성공]{res['msg1']}")
                return True
            elif res['msg1'] == "주문가능금액을 초과 했습니다":
                data["ORD_QTY"] = str(int(data["ORD_QTY"])-1)
            elif res['msg1'] == "주문수량을 확인 하여 주십시요.": break
            else:
                print(f"[매수 실패]{res['msg1']}")
                exit()
            
    def sell(self, code, qty)-> None:
        """주식 시장가 매도"""
        PATH = "uapi/domestic-stock/v1/trading/order-cash"
        URL = f"{self.URL_BASE}/{PATH}"
        data = {
            "CANO": self.__CANO__,
            "ACNT_PRDT_CD": self.__ACNT_PRDT_CD__,
            "PDNO": code,
            "ORD_DVSN": "01",
            "ORD_QTY": str(qty),
            "ORD_UNPR": "0",
        }
        headers = {"Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN__}",
            "appKey":self.__APP_KEY__,
            "appSecret":self.__APP_SECRET__,
            "tr_id":"TTTC0801U",
            "custtype":"P",
            "hashkey" : self.hashkey(data)
        }
        res = requests.post(URL, headers=headers, data=json.dumps(data)).json()
        if res['rt_cd'] == '0':
            print(f"[매도 성공]{res['msg1']}")
            return True
        else:
            print(f"[매도 실패]{res['msg1']}")
            exit()
    
    def search_most_popular_stocks(self):
        #오늘의 거래대금 상위 종목 확인
        PATH = "/uapi/domestic-stock/v1/quotations/volume-rank"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN__}",
            "appKey":self.__APP_KEY__,
            "appSecret":self.__APP_SECRET__,
            "tr_id":"FHPST01710000",
            "custtype":"P"
        }
        params = {
            "FID_COND_MRKT_DIV_CODE" : "J",
            "FID_COND_SCR_DIV_CODE" : "20171",
            "FID_INPUT_ISCD" : "0000",
            "FID_DIV_CLS_CODE" : "1",
            "FID_BLNG_CLS_CODE" : "3",
            "FID_TRGT_CLS_CODE" : "111111111",
            "FID_TRGT_EXLS_CLS_CODE" : "111111",
            "FID_INPUT_PRICE_1" : "",
            "FID_INPUT_PRICE_2" : "",
            "FID_VOL_CNT" : "100000",
            "FID_INPUT_DATE_1" : ""
        }
        res = requests.get(URL, headers=headers, params=params).json()['output'][0:min(15,len(res))]
        stock_list = []
        for i in range(15):
            stock_list.append(res[i]["mksc_shrn_iscd"])
        return stock_list
    
    def estimate_individuals(self, code=str):
        #개인 투자자 순매수량 추정
        PATH = "/uapi/domestic-stock/v1/quotations/inquire-member"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {self.__ACCESS_TOKEN__}",
            "appKey":self.__APP_KEY__,
            "appSecret":self.__APP_SECRET__,
            "tr_id":"FHKST01010600",
            "custtype":"P"
        }
        params = {
            "FID_COND_MRKT_DIV_CODE" : "J",
            "FID_INPUT_ISCD" : code
        }
        res = requests.get(URL, headers=headers, params=params).json()['output']
        buying_amount = 0
        selling_amount = 0
        for i in range(1,6):
            name = res[f'seln_mbcr_name{i}']
            if name == "키움증권" or name == "미래에셋증권":
                selling_amount += res[f'total_seln_qty{i}']
            
            name = res[f'shnu_mbcr_name{i}']
            if name == "키움증권" or name == "미래에셋증권":
                buying_amount += res[f'total_shnu_qty{i}']
        buying_rate = buying_amount/selling_amount - 1

        return buying_rate

    def search_6months_highest(self,code=str):
        # 6개월 최고가 + 날짜 조회
        PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {"Content-Type":"application/json", 
                "authorization": f"Bearer {self.__ACCESS_TOKEN__}",
                "appKey":self.__APP_KEY__,
                "appSecret":self.__APP_SECRET__,
                "tr_id":"FHKST01010100"}
        params = {
        "fid_cond_mrkt_div_code":"J",
        "fid_input_iscd":code,
        }
        res = requests.get(URL, headers=headers, params=params).json()['output']
        highest_price = int(res['d250_hgpr'])
        highest_price_date = res['d250_hgpr_date']
        return highest_price, highest_price_date
    
    def search_6months_lowest(self,code=str):
        # 6개월 최저가 + 날짜 조회
        PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
            "Content-Type":"application/json", 
            "authorization": f"Bearer {self.__ACCESS_TOKEN__}",
            "appKey":self.__APP_KEY__,
            "appSecret":self.__APP_SECRET__,
            "tr_id":"FHKST01010100"
            }
        params = {
            "fid_cond_mrkt_div_code":"J",
            "fid_input_iscd":code,
        }
        res = requests.get(URL, headers=headers, params=params).json()['output']
        lowest_price = int(res['d250_lwpr'])
        lowest_price_date = res['d250_lwpr_date']
        return lowest_price, lowest_price_date
    
    def serach_todays_price_rate(self,code=str):
        # 오늘의 주가 상승률 조회
        PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
            "Content-Type":"application/json", 
            "authorization": f"Bearer {self.__ACCESS_TOKEN__}",
            "appKey":self.__APP_KEY__,
            "appSecret":self.__APP_SECRET__,
            "tr_id":"FHKST01010100"
            }
        params = {
            "fid_cond_mrkt_div_code":"J",
            "fid_input_iscd":code,
        }
        res = requests.get(URL, headers=headers, params=params).json()['output']
        price_rate = float(res['prdy_ctrt'])
        return price_rate
    
    def judge_yesterday_gap(self, code=str):
        # 어제 갭상승 or 갭하락 여부 판단
        # 1. 날짜 계산
        yesterday = self.today - timedelta(days=1); yesterday = yesterday.strftime(self.date_format)
        day_before_yesterday = self.today - timedelta(days=2); day_before_yesterday = day_before_yesterday.strftime(self.date_format)
        # 2. 어제 그제 최저가 최고가 조회
        PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
            "Content-Type":"application/json", 
            "authorization": f"Bearer {self.__ACCESS_TOKEN__}",
            "appKey":self.__APP_KEY__,
            "appSecret":self.__APP_SECRET__,
            "tr_id":"FHKST01010100"
            }
        params = {
            "fid_cond_mrkt_div_code":"J",
            "fid_input_iscd":code,
            "FID_INPUT_DATE_1" : day_before_yesterday,
            "FID_INPUT_DATE_2" : yesterday,
            "FID_PERIOD_DIV_CODE" : "D",
            "FID_ORG_ADJ_PRC" : "0"
        }
        res = requests.get(URL, headers=headers, params=params).json()['output2']
        yesterday_data = res[0]
        day_before_yesterday_data = res[1]

        # 3. 데이터 추출
        yesterday_highest_price = yesterday_data['stck_hgpr']
        yesterday_lowest_price = yesterday_data['stck_lwpr']

        day_before_yesterday_highest_price = day_before_yesterday_data['stck_hgpr']
        day_before_yesterday_lowest_price = day_before_yesterday_data['stck_lwpr']

        status = ""
        # 4. 갭 상승 여부 확인
        if yesterday_lowest_price > day_before_yesterday_highest_price*1.01:
            status = "i"
        elif yesterday_highest_price < day_before_yesterday_lowest_price*0.99:
            status = "d"
        else:
            status = "n"
        
        # 갭 상승이면 i, 하락이면 d, 아무것도 아니면 n 반환
        
        return status
    
    def get_yesterday_close_price(self, code=str):
        # 전일 종가 조회
        yesterday = self.today - timedelta(days=1); yesterday = yesterday.strftime(self.date_format)
        PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        URL = f"{self.URL_BASE}/{PATH}"
        headers = {
            "Content-Type":"application/json", 
            "authorization": f"Bearer {self.__ACCESS_TOKEN__}",
            "appKey":self.__APP_KEY__,
            "appSecret":self.__APP_SECRET__,
            "tr_id":"FHKST01010100"
            }
        params = {
            "fid_cond_mrkt_div_code":"J",
            "fid_input_iscd":code,
            "FID_INPUT_DATE_1" : yesterday,
            "FID_INPUT_DATE_2" : yesterday,
            "FID_PERIOD_DIV_CODE" : "D",
            "FID_ORG_ADJ_PRC" : "0"
        }
        res = requests.get(URL, headers=headers, params=params).json()['output2'][0]
        return res['stck_clpr']