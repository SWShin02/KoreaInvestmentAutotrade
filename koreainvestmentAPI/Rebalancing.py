from koreainvestmentAPI.KOR import API
import pandas as pd
import time
import numpy as np

class rebalancing(API):
        def __init__(self, filepath=...) -> None:
                super().__init__(filepath)

        def load_portfolio(self, filepath):
                self.portfolio = pd.read_csv(
                        filepath_or_buffer= f"{filepath}", 
                        header=0,
                        dtype={
                                'name' : str,
                                'code' : str,
                                'weight' : np.float16
                        }
                )                    
                self.portfolio['sell'] = False
                self.portfolio['buy'] = False
                self.portfolio['trade_qty'] = 0
                print(self.portfolio)
                self.number = self.portfolio['name'].size
          
        def get_asset_balance(self):
                self.asset_balance, self.total_evaluation= super().get_asset_balance()

        def set_using_current(self):
                self.cash_balance = self.get_cash_balance()

                # 추가할 현금
                added_cash = 1000000
                if self.cash_balance > added_cash:
                        self.total_evaluation -= self.cash_balance-added_cash

        def make_trade_plan(self):
                for i in range(self.number):
                        code = self.portfolio['code'][i]
                        current_price = self.get_current_price(code)

                        target_evaluation_of_theStock = self.total_evaluation * self.portfolio['weight'][i]
                        try:
                                current_evaluation_of_theStock =  current_price*self.asset_balance[code]
                        except:
                                current_evaluation_of_theStock = 0

                        target_qty = target_evaluation_of_theStock/current_price
                        target_qty = round(target_qty)
                        trade_qty = 0
                        try :
                                trade_qty = target_qty - self.asset_balance[code]
                        except :
                                trade_qty = target_qty

                        if trade_qty > 0:
                                self.portfolio.loc[i, "buy"] = True
                        elif trade_qty < 0 and current_evaluation_of_theStock/target_evaluation_of_theStock > 1.05:
                                self.portfolio.loc[i, "sell"] = True
                                trade_qty *= -1
                        # 분할 거래 (하루 거래 금액이 50만원 넘지 않게)
                        while trade_qty > 1 and current_price*trade_qty > 500000:
                                trade_qty -= 1

                        self.portfolio.loc[i, "trade_qty"] = trade_qty
                        time.sleep(0.3)
          
        def trade(self):
                # 포트폴리오에 없는 자산 매도
                portfolio_code_lst = self.portfolio['code'].to_list()
                for code in self.asset_balance.keys():
                        if code not in portfolio_code_lst:
                                print(f"종목코드 {code}가 포트폴리에 없으므로 매도합니다.")
                                self.sell(code=code, qty=self.asset_balance[code])

                # 목표량보다 많으면 매도
                for i in range(self.number):
                        asset = self.portfolio.loc[i]
                        if asset['sell']:
                                print(asset['name'])
                                self.sell(code=asset["code"],qty=asset['trade_qty'])
                                time.sleep(0.3)
                print("매도 완료")
                print("===========================")

                # 목표량보다 적으면 매수
                for i in range(self.number):
                        asset = self.portfolio.loc[i]
                        if asset['buy']:
                                print(asset['name'])
                                self.buy(code=asset["code"],qty=asset['trade_qty'])
                        time.sleep(0.3)
                print("매수 완료")