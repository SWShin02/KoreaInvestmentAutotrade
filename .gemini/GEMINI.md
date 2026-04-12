# KoreainvestmentAutotrade

Automated trading system using the Korea Investment & Securities (KIS) Open API.

## Project Overview

This project is designed to automate stock trading and portfolio rebalancing for both domestic (South Korea) and overseas (US) markets. It provides a structured way to interact with the KIS API, manage account tokens, and execute trades based on a target portfolio defined in CSV format.

### Main Technologies
- **Python**: Core programming language.
- **Requests**: For API communication.
- **Pandas**: For portfolio management and data handling.
- **PyYAML**: For configuration and TR_ID management.
- **NumPy**: For numerical calculations in rebalancing.

## Architecture

- **`koreainvestmentAPI/`**: Core modules for the KIS API.
    - `KIStoken.py`: Base `API` class handling authentication, token issuance, and caching (`token.csv`).
    - `KOR.py`: `API` subclass for domestic stock trading (current price, balance, buy/sell, market analysis).
    - `Rebalancing.py`: `rebalancing` class inheriting from `KOR.API` to handle portfolio loading and trade plan generation.
    - `oversea/US.py`: `API` subclass for US stock trading (Note: check imports for consistency).
- **`my_account/` & `mom_account/`**: Account-specific data.
    - `config.yaml`: Contains `APP_KEY`, `APP_SECRET`, `CANO`, and `ACNT_PRDT_CD`.
    - `token.csv`: Cached access token to avoid redundant issuance.
    - `portfolio/`: Directory containing portfolio CSV files (e.g., `KR_Portfolio.csv`).
- **`trid/`**: YAML files storing Transaction IDs (TR_IDs) for different services and environments (Real/Test).

## Building and Running

### Prerequisites
- Python 3.x
- Dependencies: `pip install requests pandas pyyaml numpy`

### Execution
- **Domestic Rebalancing**:
  ```bash
  python KR_AssetRebalancing.py
  ```
  This script loads the configuration and portfolio for `my_account`, calculates the necessary trades, and executes them.

### TODO
- [ ] Implement `KR_SetPortfolio.py` to help users generate or update portfolio CSVs.
- [ ] Verify and fix the import statement in `koreainvestmentAPI/oversea/US.py`.
- [ ] Add support for automated overseas rebalancing.

## Development Conventions

- **Sensitive Data**: Never commit `config.yaml` or `token.csv`. These should be ignored by Git (already listed in `.gitignore`).
- **API Safety**: The system uses `time.sleep()` between API calls to avoid rate limiting.
- **Error Handling**: Many methods use `exit()` on failure; consider more robust error handling for long-running processes.
- **Code Style**: Inherit from the base `API` class for specific market implementations to reuse token management logic.
