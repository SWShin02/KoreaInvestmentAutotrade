import sys
from koreainvestmentAPI.Rebalancing import rebalancing

if __name__ == "__main__":
    # Check if --real flag is provided to run real trade
    dry_run = True
    if "--real" in sys.argv:
        dry_run = False

    base_filepath = "my_account"
    main = rebalancing(f"{base_filepath}/config")
    main.load_portfolio(f'{base_filepath}/portfolio/KR_Portfolio.csv')
    main.get_asset_balance()
    main.set_using_current(500000)
    main.make_trade_plan(slowdown=True)
    main.trade(dry_run=dry_run)
    print("===========================")
    if dry_run: print("자산 재분배 모의 실행(Dry-run)이 완료되었습니다.")
    else:       print("자산 재분배가 완료되었습니다.")
    print("===========================")
    main.get_asset_balance()
    main.get_cash_balance()