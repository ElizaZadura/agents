# Account Management System Design

This document outlines the detailed design for a simple account management system for a trading simulation platform, to be implemented within a single Python module named `accounts.py`.

## Module: `accounts.py`

### External Dependency / Helper Function

The system relies on a function to fetch current share prices. A test implementation is provided within the module.

#### Function: `get_share_price`

**Description:**
Simulates fetching the current market price for a given stock symbol. In a real-world scenario, this function would interact with an external market data API. For this simulation, it returns fixed prices for a few predefined symbols. If an unknown symbol is provided, it returns 0.0, indicating the price could not be found or is invalid.

**Signature:**

get_share_price(symbol: str) -> float

**Implementation Notes:**
*   Uses a dictionary mapping common stock symbols (e.g., "AAPL", "TSLA", "GOOGL") to fixed float values.
*   Returns 0.0 for unknown symbols, which allows calling methods like buy/sell shares to handle such cases.

### Class: `Account`

**Description:**
Represents a user's trading account, managing their cash balance, stock holdings, transaction history, and calculating portfolio value and profit/loss. It enforces rules to prevent invalid financial operations such as overdrawing the cash balance or selling shares that are not owned or in insufficient quantities.

#### Attributes (Internal):

*   `_account_id` (str): A unique identifier for the account.
*   `_balance` (float): The current cash available in the account.
*   `_holdings` (dict[str, int]): A dictionary where keys are stock symbols (str) and values are the quantities (int) of shares held.
*   `_transactions` (list[dict]): A chronological list of dictionaries, each representing a transaction made on the account.
*   `_total_capital_contributed` (float): The net sum of all deposits minus all withdrawals, representing the user's total capital invested into the account. This value serves as the baseline for calculating overall profit/loss.

#### Methods:

##### `__init__`

**Description:**
Initializes a new trading account with a unique identifier and an optional initial deposit. It sets up the initial cash balance, an empty holdings dictionary, and an empty transaction log. The initial deposit, if positive, is recorded as the first transaction and establishes the starting point for total capital contributed.

**Signature:**

__init__(self, account_id: str, initial_deposit: float = 0.0)

**Parameters:**
*   `account_id`: A string representing the unique identifier for this account.
*   `initial_deposit`: A float representing the initial amount of funds to be deposited. Defaults to 0.0. Must be non-negative.

**Raises:**
*   `ValueError`: If `initial_deposit` is negative.

##### `_record_transaction`

**Description:**
An internal helper method responsible for creating and appending a dictionary representing a transaction to the account's internal transaction history list (`_transactions`). This method ensures that each operation affecting the account's state is logged with relevant details and a timestamp.

**Signature:**

_record_transaction(self, type: str, amount: float = 0.0, symbol: str = None, quantity: int = 0, price: float = 0.0, description: str = None)

**Parameters:**
*   `type`: A string indicating the transaction type (e.g., "deposit", "withdraw", "buy", "sell").
*   `amount`: A float representing the monetary value involved in the transaction (e.g., deposit amount, total cost of shares, total revenue from sale).
*   `symbol`: An optional string for the stock symbol involved in the transaction (relevant for "buy" and "sell" types).
*   `quantity`: An optional integer for the number of shares involved (relevant for "buy" and "sell" types).
*   `price`: An optional float for the price per share at the time of the transaction (relevant for "buy" and "sell" types).
*   `description`: An optional string for a custom, human-readable description of the transaction.

##### `get_account_id`

**Description:**
Returns the unique identifier assigned to this trading account upon creation.

**Signature:**

get_account_id(self) -> str

**Returns:**
*   A string representing the account's ID.

##### `get_balance`

**Description:**
Returns the current cash balance available in the account. This represents the liquid funds available for further transactions.

**Signature:**

get_balance(self) -> float

**Returns:**
*   A float representing the current cash balance.

##### `deposit`

**Description:**
Deposits a specified amount of funds into the account. The amount is added to the cash balance and also increases the total capital contributed by the user, which impacts profit/loss calculations. A transaction record is created.

**Signature:**

deposit(self, amount: float) -> bool

**Parameters:**
*   `amount`: A float representing the amount to deposit. Must be a positive value.

**Returns:**
*   `True` if the deposit was successful.
*   `False` if the amount provided is non-positive, indicating an invalid deposit attempt.

##### `withdraw`

**Description:**
Withdraws a specified amount of funds from the account. The amount is subtracted from the cash balance and decreases the total capital contributed. The system prevents withdrawals that would result in a negative cash balance. A transaction record is created.

**Signature:**

withdraw(self, amount: float) -> bool

**Parameters:**
*   `amount`: A float representing the amount to withdraw. Must be a positive value.

**Returns:**
*   `True` if the withdrawal was successful.
*   `False` if the amount is non-positive or if there are insufficient funds in the account to cover the withdrawal.

##### `buy_shares`

**Description:**
Purchases a specified quantity of shares for a given stock symbol. The method first checks if the account has sufficient funds to cover the total cost of the shares. If affordable, the cash balance is reduced, the holdings are updated, and a transaction is recorded.

**Signature:**

buy_shares(self, symbol: str, quantity: int) -> bool

**Parameters:**
*   `symbol`: A string representing the stock symbol (e.g., "AAPL").
*   `quantity`: An integer representing the number of shares to buy. Must be a positive value.

**Returns:**
*   `True` if the purchase was successful.
*   `False` if the quantity is non-positive, if the share price cannot be retrieved (e.g., symbol is invalid/unknown), or if there are insufficient funds in the account.

##### `sell_shares`

**Description:**
Sells a specified quantity of shares for a given stock symbol. The method first verifies that the account holds at least the specified quantity of shares. If so, the cash balance is increased by the sale revenue, holdings are updated, and a transaction is recorded.

**Signature:**

sell_shares(self, symbol: str, quantity: int) -> bool

**Parameters:**
*   `symbol`: A string representing the stock symbol (e.g., "AAPL").
*   `quantity`: An integer representing the number of shares to sell. Must be a positive value.

**Returns:**
*   `True` if the sale was successful.
*   `False` if the quantity is non-positive, if the share price cannot be retrieved, or if the user does not own enough shares of the specified symbol.

##### `get_holdings`

**Description:**
Provides a snapshot of the current stock portfolio, detailing the quantity of shares held for each stock symbol.

**Signature:**

get_holdings(self) -> dict[str, int]

**Returns:**
*   A dictionary where keys are stock symbols (str) and values are the quantities (int) of shares held. A copy of the internal holdings dictionary is returned to prevent external modifications to the account's state.

##### `get_portfolio_value`

**Description:**
Calculates the total current value of the entire portfolio. This value is a sum of the current cash balance and the current market value of all owned stock holdings, where market values are determined by calling the `get_share_price` function for each held symbol.

**Signature:**

get_portfolio_value(self) -> float

**Returns:**
*   A float representing the total monetary value of the portfolio at the current market prices.

##### `get_profit_loss`

**Description:**
Calculates the overall profit or loss of the account. This is determined by comparing the current total portfolio value (cash + market value of holdings) against the total net capital that the user has contributed to the account over time (`_total_capital_contributed`).

**Signature:**

get_profit_loss(self) -> dict[str, float]

**Returns:**
*   A dictionary containing three key-value pairs:
    *   `total_capital_contributed`: A float representing the net amount of funds put into the account by the user (initial deposits + subsequent deposits - withdrawals).
    *   `current_portfolio_value`: A float representing the current total value of the account (cash balance plus the market value of all holdings).
    *   `profit_loss`: A float representing the difference between `current_portfolio_value` and `total_capital_contributed`. A positive value indicates profit, a negative value indicates loss.

##### `get_transactions`

**Description:**
Retrieves a complete chronological list of all financial transactions performed on the account since its inception.

**Signature:**

get_transactions(self) -> list[dict]

**Returns:**
*   A list of dictionaries, where each dictionary represents a single transaction. Each transaction dictionary includes details such as `timestamp`, `type` (e.g., "deposit", "buy"), `amount`, `symbol` (if applicable), `quantity` (if applicable), `price` (if applicable), and the `current_balance` after the transaction. A copy of the internal transactions list is returned.