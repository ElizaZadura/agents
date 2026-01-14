# Module: accounts.py

## Class: Account

### Attributes:
- `username`: str - The username of the account holder.
- `balance`: float - The current balance of the account.
- `holdings`: dict - A dictionary mapping stock symbols to the number of shares owned. 
- `transactions`: list - A list of tuples representing past transactions. Each tuple will contain (transaction_type, symbol, quantity, price, total).

### Methods:

#### `__init__(self, username: str) -> None`
- Description: Initializes a new Account instance with a username, a zero balance, empty holdings, and an empty transactions list.
  
#### `deposit(self, amount: float) -> None`
- Description: Deposits the specified amount into the account's balance.
- Parameters:
  - `amount`: float - The amount of funds to deposit (must be positive).

#### `withdraw(self, amount: float) -> None`
- Description: Withdraws the specified amount from the account's balance if sufficient funds are available.
- Parameters:
  - `amount`: float - The amount to withdraw (must be non-negative and not exceed the current balance).
- Raises:
  - `ValueError`: if the withdrawal would result in a negative balance.

#### `buy_shares(self, symbol: str, quantity: int) -> None`
- Description: Allows the user to buy shares of a given stock using the current price retrieved from `get_share_price()`.
- Parameters:
  - `symbol`: str - The stock symbol to buy shares of.
  - `quantity`: int - The number of shares to buy (must be positive and affordable).
- Raises:
  - `ValueError`: if the quantity exceeds available funds or is non-positive.

#### `sell_shares(self, symbol: str, quantity: int) -> None`
- Description: Allows the user to sell shares of a given stock.
- Parameters:
  - `symbol`: str - The stock symbol to sell shares of.
  - `quantity`: int - The number of shares to sell (must be positive and cannot exceed shares owned).
- Raises:
  - `ValueError`: if the quantity exceeds owned shares or is non-positive.

#### `get_portfolio_value(self) -> float`
- Description: Calculates and returns the total value of the user's portfolio, based on current share prices for owned stocks.
- Returns:
  - float - The total value of the portfolio.

#### `get_profit_loss(self) -> float`
- Description: Calculates the profit or loss made from the initial deposit based on the current balance and portfolio value.
- Returns:
  - float - The profit or loss amount.

#### `get_holdings(self) -> dict`
- Description: Returns a dictionary representation of the user's holdings, showing the quantities of each owned stock.
- Returns:
  - dict - A dictionary containing stock symbols and their respective quantities owned.

#### `get_transactions(self) -> list`
- Description: Returns a list of all transactions made by the user, providing a history of all buying and selling actions.
- Returns:
  - list - A list of tuples representing each transaction performed.

## Function: get_share_price(symbol: str) -> float

### Description:
- A stand-alone function to fetch the current price of a given stock symbol. For testing purposes, it returns fixed prices for "AAPL", "TSLA", and "GOOGL".

### Parameters:
- `symbol`: str - The stock symbol for which the share price is requested.

### Returns:
- float - The current share price for the given symbol (fixed values for testing).

### Example Implementation:
```python
def get_share_price(symbol: str) -> float:
    prices = {
        'AAPL': 150.00,  # Fixed price for AAPL
        'TSLA': 700.00,  # Fixed price for TSLA
        'GOOGL': 2800.00  # Fixed price for GOOGL
    }
    return prices.get(symbol, 0)  # Returns 0 if symbol is not recognized
```

### Testing:
- The module is to be self-contained, allowing for unit tests to validate each method of the `Account` class. Simple UI components can be built around the `Account` class to facilitate user interactions for account management. All exceptions should be handled appropriately to maintain robustness.