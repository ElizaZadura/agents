import datetime
from typing import Dict, List, Any

def get_share_price(symbol: str) -> float:
    # This is a test implementation. In a real system, this would call an external API.
    prices = {
        "AAPL": 170.00,
        "TSLA": 250.00,
        "GOOGL": 135.00,
        "MSFT": 320.00,
        "AMZN": 140.00,
    }
    price = prices.get(symbol.upper())
    if price is None:
        raise ValueError(f"Unknown share symbol: {symbol}")
    return price

class Account:
    """Manages a user's trading account, including cash balance, share holdings, 
    transaction history, and portfolio performance metrics."""
    
    def __init__(self, account_id: str):
        """
        Initializes a new trading account with a given ID.
        
        Parameters:
            account_id (str): The unique identifier for this account.
        """
        self.account_id = account_id
        self._balance = 0.0
        self._initial_capital = 0.0  # Net sum of all deposits minus withdrawals
        self._holdings = {}
        self._transactions = []
    
    def deposit(self, amount: float) -> None:
        """
        Deposits funds into the account.
        
        Parameters:
            amount (float): The amount of money to deposit. Must be positive.
            
        Raises:
            ValueError: If the deposit amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self._balance += amount
        self._initial_capital += amount  # Increase initial capital by deposit amount
        
        # Record the transaction
        self._record_transaction({
            'type': 'deposit',
            'timestamp': self._get_timestamp(),
            'amount': amount,
            'total_value': amount,
            'new_balance': self._balance
        })
    
    def withdraw(self, amount: float) -> None:
        """
        Withdraws funds from the account.
        
        Parameters:
            amount (float): The amount of money to withdraw. Must be positive.
            
        Raises:
            ValueError: If the withdrawal amount is not positive or if there are insufficient funds.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds for withdrawal")
        
        self._balance -= amount
        self._initial_capital -= amount  # Decrease initial capital by withdrawal amount
        
        # Record the transaction
        self._record_transaction({
            'type': 'withdraw',
            'timestamp': self._get_timestamp(),
            'amount': amount,
            'total_value': -amount,  # Negative as money leaving account
            'new_balance': self._balance
        })
    
    def buy_shares(self, symbol: str, quantity: int) -> None:
        """
        Executes a simulated share purchase.
        
        Parameters:
            symbol (str): The stock ticker symbol of the shares to buy.
            quantity (int): The number of shares to buy. Must be positive.
            
        Raises:
            ValueError: If the quantity is not positive, if the symbol is unknown,
                       or if there are insufficient funds in the account.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Get the current share price and calculate total cost
        price_per_share = get_share_price(symbol)
        total_cost = price_per_share * quantity
        
        # Check if there are sufficient funds
        if total_cost > self._balance:
            raise ValueError(f"Insufficient funds. Required: ${total_cost:.2f}, Available: ${self._balance:.2f}")
        
        # Update balance
        self._balance -= total_cost
        
        # Update holdings
        if symbol in self._holdings:
            self._holdings[symbol] += quantity
        else:
            self._holdings[symbol] = quantity
        
        # Record the transaction
        self._record_transaction({
            'type': 'buy',
            'timestamp': self._get_timestamp(),
            'symbol': symbol,
            'quantity': quantity,
            'price_per_share': price_per_share,
            'total_value': -total_cost,  # Negative as money leaving account
            'new_balance': self._balance
        })
    
    def sell_shares(self, symbol: str, quantity: int) -> None:
        """
        Executes a simulated share sale.
        
        Parameters:
            symbol (str): The stock ticker symbol of the shares to sell.
            quantity (int): The number of shares to sell. Must be positive.
            
        Raises:
            ValueError: If the quantity is not positive, if the symbol is unknown,
                       or if there are insufficient shares in holdings.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Check if the user has enough shares to sell
        current_quantity = self._holdings.get(symbol, 0)
        if quantity > current_quantity:
            raise ValueError(f"Insufficient shares. Owned: {current_quantity}, Trying to sell: {quantity}")
        
        # Get the current share price and calculate total proceeds
        price_per_share = get_share_price(symbol)
        total_proceeds = price_per_share * quantity
        
        # Update balance
        self._balance += total_proceeds
        
        # Update holdings
        self._holdings[symbol] -= quantity
        if self._holdings[symbol] == 0:
            del self._holdings[symbol]  # Remove the entry if no shares left
        
        # Record the transaction
        self._record_transaction({
            'type': 'sell',
            'timestamp': self._get_timestamp(),
            'symbol': symbol,
            'quantity': quantity,
            'price_per_share': price_per_share,
            'total_value': total_proceeds,
            'new_balance': self._balance
        })
    
    def get_balance(self) -> float:
        """
        Returns the current cash balance in the account.
        
        Returns:
            float: The current cash balance.
        """
        return self._balance
    
    def get_holdings(self) -> Dict[str, int]:
        """
        Returns a dictionary representing the current share holdings of the account.
        
        Returns:
            Dict[str, int]: A dictionary where keys are share symbols (str) and values are quantities (int).
        """
        return self._holdings.copy()  # Return a copy to prevent external modification
    
    def get_portfolio_value(self) -> float:
        """
        Calculates and returns the total value of the user's portfolio.
        
        Returns:
            float: The total current value of the portfolio.
        """
        # Start with cash balance
        total_value = self._balance
        
        # Add the value of all holdings
        for symbol, quantity in self._holdings.items():
            price = get_share_price(symbol)
            total_value += price * quantity
        
        return total_value
    
    def get_profit_loss(self) -> float:
        """
        Calculates the profit or loss from the initial capital deposited into the account.
        
        Returns:
            float: The calculated profit or loss. Positive for profit, negative for loss.
        """
        return self.get_portfolio_value() - self._initial_capital
    
    def get_transactions(self) -> List[Dict[str, Any]]:
        """
        Returns a chronological list of all transactions made in the account.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each detailing a transaction.
        """
        return self._transactions.copy()  # Return a copy to prevent external modification
    
    def _record_transaction(self, transaction: Dict[str, Any]) -> None:
        """
        Records a transaction in the account's transaction history.
        
        Parameters:
            transaction (Dict[str, Any]): A dictionary containing transaction details.
        """
        self._transactions.append(transaction)
    
    def _get_timestamp(self) -> str:
        """
        Returns a UTC timestamp string for the current time.
        
        Returns:
            str: A UTC timestamp string.
        """
        return datetime.datetime.now(datetime.timezone.utc).isoformat()