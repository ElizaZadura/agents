# accounts.py

## This module provides a simple account management system for a trading simulation platform, including functionality for managing cash, buying/selling shares, tracking holdings, and reporting portfolio value and profit/loss

### Module Level Function

#### get_share_price(symbol: str) -> float

Description:
A simulated function to retrieve the current market price of a given share symbol. For demonstration purposes, it returns fixed prices for specific symbols and raises an error for unknown symbols.

Parameters:

* symbol (str): The stock ticker symbol (e.g., "AAPL", "TSLA", "GOOGL").

Returns:

* float: The current price of the share.

Raises:

* ValueError: If the symbol is not recognized in the test data.

Example Test Implementation:

```python
def get_share_price(symbol: str) -> float:
    # This is a test implementation. In a real system, this would call an external API.
    prices = {
        "AAPL": 170.00,
        "TSLA": 250.00,
        "GOOGL": 135.00,
        "MSFT": 320.00, # Added for more variety
        "AMZN": 140.00, # Added for more variety
    }
    price = prices.get(symbol.upper())
    if price is None:
        raise ValueError(f"Unknown share symbol: {symbol}")
    return price
```

### Class

#### Account

Description:
Manages a user's trading account, including cash balance, share holdings, transaction history, and portfolio performance metrics.

Attributes:

* account_id (str): A unique identifier for the account.
* _balance (float): The current cash balance in the account.
* _initial_capital (float): The net sum of all deposits minus withdrawals, used for P&L calculation.
* _holdings (Dict[str, int]): A dictionary storing the quantity of shares held for each symbol (e.g., {"AAPL": 10, "TSLA": 5}).
* _transactions (List[Dict[str, Any]]): A list of dictionaries, where each dictionary represents a transaction (deposit, withdrawal, buy, sell).

Methods:

#### __init__(self, account_id: str)

Description:
Initializes a new trading account with a given ID. Sets the initial balance, capital, holdings, and transactions to empty states.

Parameters:

* account_id (str): The unique identifier for this account.

#### deposit(self, amount: float) -> None

Description:
Deposits funds into the account. The amount is added to both the current balance and the initial capital tracking. A transaction record is created.

Parameters:

* amount (float): The amount of money to deposit. Must be positive.

Raises:

* ValueError: If the deposit amount is not positive.

#### withdraw(self, amount: float) -> None

Description:
Withdraws funds from the account. The amount is subtracted from the current balance and the initial capital tracking. A transaction record is created. Prevents withdrawal if it would result in a negative balance.

Parameters:

* amount (float): The amount of money to withdraw. Must be positive.

Raises:

* ValueError: If the withdrawal amount is not positive or if there are insufficient funds.

#### buy_shares(self, symbol: str, quantity: int) -> None

Description:
Executes a simulated share purchase. Calculates the total cost using the current share price and debits the account balance. Updates share holdings. Prevents purchase if there are insufficient funds. A transaction record is created.

Parameters:

* symbol (str): The stock ticker symbol of the shares to buy.
* quantity (int): The number of shares to buy. Must be positive.

Raises:

* ValueError: If the quantity is not positive, if the symbol is unknown (from get_share_price), or if there are insufficient funds in the account.

#### sell_shares(self, symbol: str, quantity: int) -> None

Description:
Executes a simulated share sale. Calculates the total proceeds using the current share price and credits the account balance. Updates share holdings. Prevents sale if the user does not own enough shares. A transaction record is created.

Parameters:

* symbol (str): The stock ticker symbol of the shares to sell.
* quantity (int): The number of shares to sell. Must be positive.

Raises:

* ValueError: If the quantity is not positive, if the symbol is unknown (from get_share_price), or if there are insufficient shares in holdings.

#### get_balance(self) -> float

Description:
Returns the current cash balance in the account.

Returns:

* float: The current cash balance.

#### get_holdings(self) -> Dict[str, int]

Description:
Returns a dictionary representing the current share holdings of the account.

Returns:

* Dict[str, int]: A dictionary where keys are share symbols (str) and values are quantities (int).

#### get_portfolio_value(self) -> float

Description:
Calculates and returns the total value of the user's portfolio, which includes the current cash balance and the current market value of all share holdings.

Returns:

* float: The total current value of the portfolio.

#### get_profit_loss(self) -> float

Description:
Calculates the profit or loss from the initial net capital deposited into the account. This is calculated as the current portfolio value minus the net initial capital (total deposits - total withdrawals).

Returns:

* float: The calculated profit or loss. Positive for profit, negative for loss.

#### get_transactions(self) -> List[Dict[str, Any]]

Description:
Returns a chronological list of all transactions made in the account.

Returns:

* List[Dict[str, Any]]: A list of dictionaries, each detailing a transaction. Transaction dictionaries include:
  * 'type' (str): "deposit", "withdraw", "buy", "sell"
  * 'timestamp' (str): UTC timestamp of the transaction.
  * 'amount' (float): For deposit/withdraw, the amount.
  * 'symbol' (str, optional): For buy/sell, the stock symbol.
  * 'quantity' (int, optional): For buy/sell, the number of shares.
  * 'price_per_share' (float, optional): For buy/sell, the price at which shares were traded.
  * 'total_value' (float): The total monetary value of the transaction.
  * 'new_balance' (float): The account balance immediately after the transaction.

### Example Usage (for testing purposes)

```python
# Import the Account class and get_share_price function
from accounts import Account, get_share_price

# Create an account
my_account = Account("user123")
print(f"Initial Balance: ${my_account.get_balance():.2f}")
print(f"Initial Holdings: {my_account.get_holdings()}")
print(f"Initial Portfolio Value: ${my_account.get_portfolio_value():.2f}")
print(f"Initial P&L: ${my_account.get_profit_loss():.2f}\n")

# Deposit funds
try:
    my_account.deposit(10000.00)
    print(f"Deposited $10,000. New Balance: ${my_account.get_balance():.2f}")
except ValueError as e:
    print(f"Deposit error: {e}")

# Buy shares
try:
    print(f"AAPL price: ${get_share_price('AAPL'):.2f}")
    my_account.buy_shares("AAPL", 10)
    print(f"Bought 10 AAPL. New Balance: ${my_account.get_balance():.2f}")
    print(f"Holdings: {my_account.get_holdings()}")
except ValueError as e:
    print(f"Buy error: {e}")

try:
    print(f"TSLA price: ${get_share_price('TSLA'):.2f}")
    my_account.buy_shares("TSLA", 5)
    print(f"Bought 5 TSLA. New Balance: ${my_account.get_balance():.2f}")
    print(f"Holdings: {my_account.get_holdings()}")
except ValueError as e:
    print(f"Buy error: {e}")

# Attempt to buy more than affordable
try:
    my_account.buy_shares("GOOGL", 1000)
except ValueError as e:
    print(f"Attempted to buy 1000 GOOGL shares, got error: {e}")

# Withdraw funds
try:
    my_account.withdraw(500.00)
    print(f"Withdrew $500. New Balance: ${my_account.get_balance():.2f}")
except ValueError as e:
    print(f"Withdraw error: {e}")

# Sell shares
try:
    print(f"Selling 2 AAPL shares...")
    my_account.sell_shares("AAPL", 2)
    print(f"Sold 2 AAPL. New Balance: ${my_account.get_balance():.2f}")
    print(f"Holdings: {my_account.get_holdings()}")
except ValueError as e:
    print(f"Sell error: {e}")

# Attempt to sell more than owned
try:
    print(f"Attempting to sell 100 TSLA shares...")
    my_account.sell_shares("TSLA", 100)
except ValueError as e:
    print(f"Got error: {e}")

# Report current status
print("\n--- Current Account Status ---")
print(f"Current Balance: ${my_account.get_balance():.2f}")
print(f"Current Holdings: {my_account.get_holdings()}")
print(f"Current Portfolio Value: ${my_account.get_portfolio_value():.2f}")
print(f"Profit/Loss: ${my_account.get_profit_loss():.2f}")

# List all transactions
print("\n--- Transaction History ---")
for transaction in my_account.get_transactions():
    print(transaction)
```
