from koreainvestmentAPI.Rebalancing import rebalancing

if __name__ == "__main__":
    base_filepath = "strategy"
    main = rebalancing(f"{base_filepath}/config")
    main.load_portfolio(f'{base_filepath}/portfolio/KR_Portfolio.csv')
    main.get_asset_balance()
    main.set_using_current()
    main.make_trade_plan()
    main.trade()
    print("===========================")
    print("자산 재분배가 완료되었습니다.")
    print("===========================")
    main.get_asset_balance()
    main.get_cash_balance()
