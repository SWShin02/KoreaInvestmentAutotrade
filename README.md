# KoreainvestmentAutotrade

Automated trading and portfolio rebalancing system using the **Korea Investment & Securities (KIS) Open API**.

This project automates the process of fetching account balances, calculating target quantities based on a predefined portfolio, and executing buy/sell orders for both domestic (KR) and overseas (US) markets.

## Key Features

- **Automated Authentication**: Handles OAuth2 token issuance and caching to minimize redundant API calls.
- **Portfolio Rebalancing**: Automatically calculates the difference between your current holdings and target weights, generating a trade plan.
- **Multi-Market Support**: Dedicated modules for Domestic (South Korea) and Overseas (US) stock trading.
- **Account Management**: Support for multiple account configurations (e.g., `my_account`, `mom_account`).
- **Safety Measures**: Includes `time.sleep()` intervals to respect API rate limits and basic error handling.

## Prerequisites

- **Python 3.x**
- Required Libraries:
  ```bash
  pip install requests pandas pyyaml numpy
  ```
- **KIS API Account**: You must have an active account and API keys (App Key, App Secret) from the [Korea Investment & Securities API Portal](https://apiportal.koreainvestment.com).

## Configuration

### 1. Account Setup
Create a `config.yaml` file inside your account directory (e.g., `my_account/config/config.yaml` or as per your path logic):

```yaml
APP_KEY: "your_app_key"
APP_SECRET: "your_app_secret"
CANO: "your_8_digit_account_number"
ACNT_PRDT_CD: "01" # Typically 01 for stock accounts
```

### 2. Portfolio Definition
Define your target portfolio in a CSV file (e.g., `my_account/portfolio/KR_Portfolio.csv`):

```csv
name,code,weight
Samsung Electronics,005930,0.4
SK Hynix,000660,0.3
...
```
*Note: Weights should sum up to 1.0 (or your desired allocation).*

## Usage

### Domestic Rebalancing
To run the rebalancing process for domestic stocks:

```bash
python KR_AssetRebalancing.py
```

This script will:
1. Load your API credentials and portfolio.
2. Fetch current market prices and your account balance.
3. Calculate the necessary buy/sell orders.
4. Execute trades to align your account with the target weights.

## Project Structure

- `koreainvestmentAPI/`: Core API wrapper modules.
  - `KIStoken.py`: Authentication and token management.
  - `KOR.py`: Domestic trading functions.
  - `oversea/US.py`: Overseas (US) trading functions.
  - `Rebalancing.py`: Core logic for portfolio rebalancing.
- `trid/`: Transaction ID (TR_ID) configurations for different environments.
- `KR_AssetRebalancing.py`: Entry point for domestic rebalancing.

## Documentation & API Reference

For detailed information regarding the KIS Open API specifications, response codes, and TR_IDs, please visit the official documentation:

👉 **[Korea Investment & Securities API Portal](https://apiportal.koreainvestment.com)**

## Disclaimer

**Trading stocks involves significant risk.** This software is provided "as is" for educational and automation purposes. The authors are not responsible for any financial losses incurred through the use of this automated system. Always test your strategies in a virtual/test environment (Mock Investment) before using real capital.
