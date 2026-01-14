import unittest
from unittest.mock import patch
import datetime
import sys
sys.path.insert(0, '.')
from accounts import get_share_price, Account

class TestGetSharePrice(unittest.TestCase):
    def test_valid_symbol(self):
        self.assertEqual(get_share_price('AAPL'), 170.00)
        self.assertEqual(get_share_price('tsla'), 250.00)  # lowercase
        self.assertEqual(get_share_price('GOOGL'), 135.00)
    
    def test_invalid_symbol(self):
        with self.assertRaises(ValueError) as context:
            get_share_price('INVALID')
        self.assertEqual(str(context.exception), 'Unknown share symbol: INVALID')

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('test123')
    
    def test_initial_state(self):
        self.assertEqual(self.account.account_id, 'test123')
        self.assertEqual(self.account.get_balance(), 0.0)
        self.assertEqual(self.account.get_holdings(), {})
        self.assertEqual(self.account.get_transactions(), [])
        self.assertEqual(self.account.get_portfolio_value(), 0.0)
        self.assertEqual(self.account.get_profit_loss(), 0.0)
    
    def test_deposit_positive(self):
        self.account.deposit(100.0)
        self.assertEqual(self.account.get_balance(), 100.0)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['type'], 'deposit')
        self.assertEqual(transactions[0]['amount'], 100.0)
        self.assertEqual(transactions[0]['new_balance'], 100.0)
    
    def test_deposit_zero(self):
        with self.assertRaises(ValueError) as context:
            self.account.deposit(0)
        self.assertEqual(str(context.exception), 'Deposit amount must be positive')
    
    def test_deposit_negative(self):
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-50.0)
        self.assertEqual(str(context.exception), 'Deposit amount must be positive')
    
    def test_withdraw_sufficient(self):
        self.account.deposit(200.0)
        self.account.withdraw(50.0)
        self.assertEqual(self.account.get_balance(), 150.0)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[1]['type'], 'withdraw')
        self.assertEqual(transactions[1]['amount'], 50.0)
        self.assertEqual(transactions[1]['new_balance'], 150.0)
    
    def test_withdraw_insufficient(self):
        self.account.deposit(30.0)
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(50.0)
        self.assertEqual(str(context.exception), 'Insufficient funds for withdrawal')
    
    def test_withdraw_zero(self):
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(0)
        self.assertEqual(str(context.exception), 'Withdrawal amount must be positive')
    
    def test_withdraw_negative(self):
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-10.0)
        self.assertEqual(str(context.exception), 'Withdrawal amount must be positive')
    
    @patch('accounts.get_share_price', return_value=170.0)
    def test_buy_shares_sufficient_funds(self, mock_get_price):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.get_balance(), 1000.0 - 170.0*2)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[1]['type'], 'buy')
        self.assertEqual(transactions[1]['symbol'], 'AAPL')
        self.assertEqual(transactions[1]['quantity'], 2)
        self.assertEqual(transactions[1]['price_per_share'], 170.0)
        self.assertEqual(transactions[1]['total_value'], -340.0)
    
    @patch('accounts.get_share_price', return_value=170.0)
    def test_buy_shares_insufficient_funds(self, mock_get_price):
        self.account.deposit(100.0)
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', 1)
        self.assertIn('Insufficient funds', str(context.exception))
    
    @patch('accounts.get_share_price', side_effect=ValueError('Unknown share symbol: INVALID'))
    def test_buy_shares_invalid_symbol(self, mock_get_price):
        self.account.deposit(1000.0)
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('INVALID', 1)
        self.assertEqual(str(context.exception), 'Unknown share symbol: INVALID')
    
    @patch('accounts.get_share_price', return_value=170.0)
    def test_buy_shares_zero_quantity(self, mock_get_price):
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', 0)
        self.assertEqual(str(context.exception), 'Quantity must be positive')
    
    @patch('accounts.get_share_price', return_value=170.0)
    def test_buy_shares_negative_quantity(self, mock_get_price):
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', -5)
        self.assertEqual(str(context.exception), 'Quantity must be positive')
    
    @patch('accounts.get_share_price', return_value=250.0)
    def test_sell_shares_sufficient(self, mock_get_price):
        self.account.deposit(1000.0)
        self.account.buy_shares('TSLA', 4)
        self.account.sell_shares('TSLA', 2)
        self.assertEqual(self.account.get_balance(), 1000.0 - 250.0*4 + 250.0*2)
        self.assertEqual(self.account.get_holdings(), {'TSLA': 2})
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[2]['type'], 'sell')
        self.assertEqual(transactions[2]['symbol'], 'TSLA')
        self.assertEqual(transactions[2]['quantity'], 2)
        self.assertEqual(transactions[2]['price_per_share'], 250.0)
        self.assertEqual(transactions[2]['total_value'], 500.0)
    
    @patch('accounts.get_share_price', return_value=250.0)
    def test_sell_shares_insufficient(self, mock_get_price):
        self.account.deposit(1000.0)
        self.account.buy_shares('TSLA', 3)
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('TSLA', 5)
        self.assertIn('Insufficient shares', str(context.exception))
    
    @patch('accounts.get_share_price', return_value=250.0)
    def test_sell_shares_zero_quantity(self, mock_get_price):
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('TSLA', 0)
        self.assertEqual(str(context.exception), 'Quantity must be positive')
    
    @patch('accounts.get_share_price', return_value=250.0)
    def test_sell_shares_negative_quantity(self, mock_get_price):
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('TSLA', -1)
        self.assertEqual(str(context.exception), 'Quantity must be positive')
    
    @patch('accounts.get_share_price', return_value=250.0)
    def test_sell_all_shares(self, mock_get_price):
        self.account.deposit(1000.0)
        self.account.buy_shares('TSLA', 2)
        self.account.sell_shares('TSLA', 2)
        self.assertEqual(self.account.get_holdings(), {})
    
    @patch('accounts.get_share_price', side_effect=ValueError('Unknown share symbol: INVALID'))
    def test_sell_shares_invalid_symbol(self, mock_get_price):
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('INVALID', 1)
        self.assertEqual(str(context.exception), 'Unknown share symbol: INVALID')
    
    @patch('accounts.get_share_price')
    def test_get_portfolio_value(self, mock_get_price):
        mock_get_price.side_effect = lambda s: {'AAPL': 170.0, 'TSLA': 250.0}[s]
        self.account.deposit(500.0)
        self.account.buy_shares('AAPL', 2)
        self.account.buy_shares('TSLA', 1)
        expected = 500.0 - (170.0*2 + 250.0*1) + (170.0*2 + 250.0*1)
        self.assertEqual(self.account.get_portfolio_value(), expected)
    
    @patch('accounts.get_share_price')
    def test_get_profit_loss(self, mock_get_price):
        mock_get_price.side_effect = lambda s: {'AAPL': 170.0}[s]
        self.account.deposit(1000.0)
        self.account.withdraw(200.0)
        self.account.buy_shares('AAPL', 2)
        # initial capital = 1000 - 200 = 800
        # portfolio value = balance + holdings = (1000-200-340) + (170*2) = 460 + 340 = 800
        # profit/loss = 800 - 800 = 0
        self.assertEqual(self.account.get_profit_loss(), 0.0)
        # simulate price increase
        mock_get_price.side_effect = lambda s: {'AAPL': 200.0}[s]
        # portfolio value = 460 + (200*2) = 860
        # profit/loss = 860 - 800 = 60
        self.assertEqual(self.account.get_profit_loss(), 60.0)
    
    def test_transaction_history_order(self):
        self.account.deposit(100.0)
        self.account.withdraw(30.0)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['type'], 'deposit')
        self.assertEqual(transactions[1]['type'], 'withdraw')
        # check timestamps are increasing
        self.assertLess(transactions[0]['timestamp'], transactions[1]['timestamp'])
    
    def test_holdings_copy(self):
        self.account.deposit(1000.0)
        with patch('accounts.get_share_price', return_value=170.0):
            self.account.buy_shares('AAPL', 2)
        holdings = self.account.get_holdings()
        holdings['AAPL'] = 999  # modify the copy
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})  # original unchanged
    
    def test_transactions_copy(self):
        self.account.deposit(100.0)
        transactions = self.account.get_transactions()
        transactions.append({'type': 'fake'})  # modify the copy
        self.assertEqual(len(self.account.get_transactions()), 1)  # original unchanged

if __name__ == '__main__':
    unittest.main()