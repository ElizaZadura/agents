import unittest
from unittest.mock import patch
import accounts

class TestGetSharePrice(unittest.TestCase):
    def test_valid_symbol(self):
        self.assertEqual(accounts.get_share_price('AAPL'), 150.0)
        self.assertEqual(accounts.get_share_price('TSLA'), 700.0)
        self.assertEqual(accounts.get_share_price('GOOGL'), 2800.0)
    
    def test_invalid_symbol(self):
        self.assertEqual(accounts.get_share_price('INVALID'), 0.0)

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = accounts.Account('test123', 1000.0)
    
    def test_initialization(self):
        # Test with positive initial deposit
        acc = accounts.Account('acc1', 500.0)
        self.assertEqual(acc.get_account_id(), 'acc1')
        self.assertEqual(acc.get_balance(), 500.0)
        self.assertEqual(acc.get_holdings(), {})
        self.assertEqual(len(acc.get_transactions()), 1)  # deposit transaction
        
        # Test with zero initial deposit
        acc2 = accounts.Account('acc2')
        self.assertEqual(acc2.get_balance(), 0.0)
        self.assertEqual(len(acc2.get_transactions()), 0)
        
        # Test with negative initial deposit raises ValueError
        with self.assertRaises(ValueError):
            accounts.Account('acc3', -100.0)
    
    def test_deposit(self):
        # Successful deposit
        self.assertTrue(self.account.deposit(200.0))
        self.assertEqual(self.account.get_balance(), 1200.0)
        
        # Deposit zero or negative amount returns False
        self.assertFalse(self.account.deposit(0.0))
        self.assertFalse(self.account.deposit(-50.0))
        self.assertEqual(self.account.get_balance(), 1200.0)  # unchanged
        
        # Verify transaction recorded
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)  # initial deposit + new deposit
        self.assertEqual(transactions[-1]['type'], 'deposit')
        self.assertEqual(transactions[-1]['amount'], 200.0)
    
    def test_withdraw(self):
        # Successful withdrawal
        self.assertTrue(self.account.withdraw(300.0))
        self.assertEqual(self.account.get_balance(), 700.0)
        
        # Withdraw zero or negative returns False
        self.assertFalse(self.account.withdraw(0.0))
        self.assertFalse(self.account.withdraw(-100.0))
        self.assertEqual(self.account.get_balance(), 700.0)
        
        # Withdraw more than balance returns False
        self.assertFalse(self.account.withdraw(800.0))
        self.assertEqual(self.account.get_balance(), 700.0)
        
        # Verify transaction recorded
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)  # initial deposit + withdrawal
        self.assertEqual(transactions[-1]['type'], 'withdraw')
        self.assertEqual(transactions[-1]['amount'], 300.0)
    
    @patch('accounts.get_share_price')
    def test_buy_shares(self, mock_get_share_price):
        mock_get_share_price.return_value = 150.0  # AAPL price
        
        # Successful buy
        self.assertTrue(self.account.buy_shares('AAPL', 2))
        self.assertEqual(self.account.get_balance(), 1000.0 - 300.0)  # 700.0
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})
        
        # Buy zero or negative quantity returns False
        self.assertFalse(self.account.buy_shares('AAPL', 0))
        self.assertFalse(self.account.buy_shares('AAPL', -1))
        self.assertEqual(self.account.get_balance(), 700.0)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})
        
        # Buy with insufficient balance returns False
        self.assertFalse(self.account.buy_shares('AAPL', 10))  # cost 1500 > 700
        self.assertEqual(self.account.get_balance(), 700.0)
        
        # Buy with invalid symbol (price 0.0) returns False
        mock_get_share_price.return_value = 0.0
        self.assertFalse(self.account.buy_shares('INVALID', 1))
        
        # Verify transaction recorded
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)  # initial deposit + buy
        self.assertEqual(transactions[-1]['type'], 'buy')
        self.assertEqual(transactions[-1]['symbol'], 'AAPL')
        self.assertEqual(transactions[-1]['quantity'], 2)
        self.assertEqual(transactions[-1]['price'], 150.0)
    
    @patch('accounts.get_share_price')
    def test_sell_shares(self, mock_get_share_price):
        mock_get_share_price.return_value = 150.0
        # First buy some shares
        self.account.buy_shares('AAPL', 4)
        balance_after_buy = self.account.get_balance()
        
        # Successful sell
        self.assertTrue(self.account.sell_shares('AAPL', 2))
        self.assertEqual(self.account.get_balance(), balance_after_buy + 300.0)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})
        
        # Sell zero or negative quantity returns False
        self.assertFalse(self.account.sell_shares('AAPL', 0))
        self.assertFalse(self.account.sell_shares('AAPL', -1))
        
        # Sell more than holdings returns False
        self.assertFalse(self.account.sell_shares('AAPL', 5))
        
        # Sell symbol not in holdings returns False
        self.assertFalse(self.account.sell_shares('TSLA', 1))
        
        # Sell all remaining shares, holdings should be empty
        self.assertTrue(self.account.sell_shares('AAPL', 2))
        self.assertEqual(self.account.get_holdings(), {})
        
        # Verify transaction recorded
        transactions = self.account.get_transactions()
        # initial deposit, buy, sell, sell
        self.assertEqual(len(transactions), 4)
        self.assertEqual(transactions[-1]['type'], 'sell')
        self.assertEqual(transactions[-1]['symbol'], 'AAPL')
        self.assertEqual(transactions[-1]['quantity'], 2)
    
    def test_get_portfolio_value(self):
        # Initially only cash
        self.assertEqual(self.account.get_portfolio_value(), 1000.0)
        
        # With holdings
        with patch('accounts.get_share_price') as mock_get:
            mock_get.return_value = 150.0
            self.account.buy_shares('AAPL', 2)
            # balance = 1000 - 300 = 700, holdings value = 300, total = 1000
            self.assertEqual(self.account.get_portfolio_value(), 1000.0)
            
            # Change mock price
            mock_get.return_value = 200.0
            # holdings value = 400, total = 700 + 400 = 1100
            self.assertEqual(self.account.get_portfolio_value(), 1100.0)
    
    def test_get_profit_loss(self):
        # Initially no profit/loss
        pl = self.account.get_profit_loss()
        self.assertEqual(pl['total_capital_contributed'], 1000.0)
        self.assertEqual(pl['current_portfolio_value'], 1000.0)
        self.assertEqual(pl['profit_loss'], 0.0)
        
        # After deposit
        self.account.deposit(500.0)
        pl = self.account.get_profit_loss()
        self.assertEqual(pl['total_capital_contributed'], 1500.0)
        self.assertEqual(pl['current_portfolio_value'], 1500.0)
        self.assertEqual(pl['profit_loss'], 0.0)
        
        # After withdrawal
        self.account.withdraw(200.0)
        pl = self.account.get_profit_loss()
        self.assertEqual(pl['total_capital_contributed'], 1300.0)
        self.assertEqual(pl['current_portfolio_value'], 1300.0)
        self.assertEqual(pl['profit_loss'], 0.0)
        
        # With holdings and price change
        with patch('accounts.get_share_price') as mock_get:
            mock_get.return_value = 150.0
            self.account.buy_shares('AAPL', 2)  # cost 300
            # total capital contributed remains 1300
            # portfolio value = balance 1000 + holdings 300 = 1300
            pl = self.account.get_profit_loss()
            self.assertEqual(pl['profit_loss'], 0.0)
            
            # Price increases
            mock_get.return_value = 200.0
            # portfolio value = 1000 + 400 = 1400
            pl = self.account.get_profit_loss()
            self.assertEqual(pl['profit_loss'], 100.0)
    
    def test_get_transactions(self):
        # Initial transaction from deposit
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['type'], 'deposit')
        self.assertEqual(transactions[0]['amount'], 1000.0)
        
        # Transactions are copied, not the original list
        transactions.append('extra')
        self.assertEqual(len(self.account.get_transactions()), 1)
    
    def test_get_holdings(self):
        # Initially empty
        self.assertEqual(self.account.get_holdings(), {})
        
        # After buying shares
        with patch('accounts.get_share_price') as mock_get:
            mock_get.return_value = 150.0
            self.account.buy_shares('AAPL', 3)
            holdings = self.account.get_holdings()
            self.assertEqual(holdings, {'AAPL': 3})
            
            # Holdings are copied
            holdings['AAPL'] = 5
            self.assertEqual(self.account.get_holdings(), {'AAPL': 3})

if __name__ == '__main__':
    unittest.main()