class Account:
    def __init__(self, username: str) -> None:
        self.username = username
        self.balance = 0.0
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError('Deposit amount must be positive')
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount < 0:
            raise ValueError('Withdrawal amount must be non-negative')
        if self.balance - amount < 0:
            raise ValueError('Insufficient funds for withdrawal')
        self.balance -= amount

    def buy_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Quantity must be positive')
        price = get_share_price(symbol)
        cost = price * quantity
        if cost > self.balance:
            raise ValueError('Insufficient funds to buy shares')
        
        self.balance -= cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append(('buy', symbol, quantity, price, cost))

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Quantity must be positive')
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError('Not enough shares owned to sell')
        
        price = get_share_price(symbol)
        earnings = price * quantity
        self.balance += earnings
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append(('sell', symbol, quantity, price, earnings))

    def get_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_loss(self) -> float:
        initial_deposit = sum(cost for _, _, _, _, cost in self.transactions if _ == 'buy')
        return self.get_portfolio_value() - initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transactions(self) -> list:
        return self.transactions


def get_share_price(symbol: str) -> float:
    prices = {
        'AAPL': 150.00,
        'TSLA': 700.00,
        'GOOGL': 2800.00
    }
    return prices.get(symbol, 0)