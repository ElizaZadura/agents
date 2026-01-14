import unittest
from unittest.mock import patch

import accounts

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = accounts.Account('testuser')
    
    def test_initialization(self):
        self.assertEqual(self.account.username, 'testuser')
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])
    
    def test_deposit_positive(self):
        self.account.deposit(100.0)
        self.assertEqual(self.account.balance, 100.0)
    
    def test_deposit_zero_raises(self):
        with self.assertRaises(ValueError) as context:
            self.account.deposit(0)
        self.assertEqual(str(context.exception), 'Deposit amount must be positive')
    
    def test_deposit_negative_raises(self):
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-50.0)
        self.assertEqual(str(context.exception), 'Deposit amount must be positive')
    
    def test_withdraw_sufficient(self):
        self.account.deposit(200.0)
        self.account.withdraw(50.0)
        self.assertEqual(self.account.balance, 150.0)
    
    def test_withdraw_zero(self):
        self.account.deposit(100.0)
        self.account.withdraw(0)
        self.assertEqual(self.account.balance, 100.0)
    
    def test_withdraw_negative_raises(self):
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-10.0)
        self.assertEqual(str(context.exception), 'Withdrawal amount must be non-negative')
    
    def test_withdraw_insufficient_raises(self):
        self.account.deposit(30.0)
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(50.0)
        self.assertEqual(str(context.exception), 'Insufficient funds for withdrawal')
    
    @patch('accounts.get_share_price')
    def test_buy_shares_sufficient_funds(self, mock_get_price):
        mock_get_price.return_value = 150.0
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.balance, 1000.0 - (150.0 * 2))
        self.assertEqual(self.account.holdings, {'AAPL': 2})
        self.assertEqual(len(self.account.transactions), 1)
        last_transaction = self.account.transactions[-1]
        self.assertEqual(last_transaction[0], 'buy')
        self.assertEqual(last_transaction[1], 'AAPL')
        self.assertEqual(last_transaction[2], 2)
        self.assertEqual(last_transaction[3], 150.0)
        self.assertEqual(last_transaction[4], 300.0)
    
    @patch('accounts.get_share_price')
    def test_buy_shares_insufficient_funds_raises(self, mock_get_price):
        mock_get_price.return_value = 500.0
        self.account.deposit(100.0)
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('TSLA', 1)
        self.assertEqual(str(context.exception), 'Insufficient funds to buy shares')
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(self.account.holdings, {})
    
    @patch('accounts.get_share_price')
    def test_buy_shares_zero_quantity_raises(self, mock_get_price):
        mock_get_price.return_value = 150.0
        self.account.deposit(1000.0)
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', 0)
        self.assertEqual(str(context.exception), 'Quantity must be positive')
    
    @patch('accounts.get_share_price')
    def test_buy_shares_negative_quantity_raises(self, mock_get_price):
        mock_get_price.return_value = 150.0
        self.account.deposit(1000.0)
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', -5)
        self.assertEqual(str(context.exception), 'Quantity must be positive')
    
    @patch('accounts.get_share_price')
    def test_sell_shares_sufficient(self, mock_get_price):
        mock_get_price.return_value = 160.0
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 5)
        initial_balance = self.account.balance
        self.account.sell_shares('AAPL', 3)
        self.assertEqual(self.account.balance, initial_balance + 480.0)
        self.assertEqual(self.account.holdings, {'AAPL': 2})
        last_transaction = self.account.transactions[-1]
        self.assertEqual(last_transaction[0], 'sell')
        self.assertEqual(last_transaction[1], 'AAPL')
        self.assertEqual(last_transaction[2], 3)
        self.assertEqual(last_transaction[3], 160.0)
        self.assertEqual(last_transaction[4], 480.0)
    
    @patch('accounts.get_share_price')
    def test_sell_shares_zero_quantity_raises(self, mock_get_price):
        mock_get_price.return_value = 150.0
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 5)
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', 0)
        self.assertEqual(str(context.exception), 'Quantity must be positive')
    
    @patch('accounts.get_share_price')
    def test_sell_shares_negative_quantity_raises(self, mock_get_price):
        mock_get_price.return_value = 150.0
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 5)
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', -2)
        self.assertEqual(str(context.exception), 'Quantity must be positive')
    
    @patch('accounts.get_share_price')
    def test_sell_shares_not_owned_raises(self, mock_get_price):
        mock_get_price.return_value = 150.0
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', 1)
        self.assertEqual(str(context.exception), 'Not enough shares owned to sell')
    
    @patch('accounts.get_share_price')
    def test_sell_shares_insufficient_quantity_raises(self, mock_get_price):
        mock_get_price.return_value = 150.0
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 2)
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', 5)
        self.assertEqual(str(context.exception), 'Not enough shares owned to sell')
    
    @patch('accounts.get_share_price')
    def test_get_portfolio_value(self, mock_get_price):
        mock_get_price.return_value = 150.0
        self.account.deposit(500.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.get_portfolio_value(), 500.0)
    
    @patch('accounts.get_share_price')
    def test_get_profit_loss(self, mock_get_price):
        mock_get_price.side_effect = [150.0, 160.0]
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 5)
        self.account.sell_shares('AAPL', 3)
        self.assertEqual(self.account.get_profit_loss(), 300.0)
    
    def test_get_holdings(self):
        self.assertEqual(self.account.get_holdings(), {})
        with patch('accounts.get_share_price', return_value=150.0):
            self.account.deposit(1000.0)
            self.account.buy_shares('AAPL', 3)
            self.assertEqual(self.account.get_holdings(), {'AAPL': 3})
    
    def test_get_transactions(self):
        self.assertEqual(self.account.get_transactions(), [])
        with patch('accounts.get_share_price', return_value=150.0):
            self.account.deposit(200.0)
            self.account.buy_shares('AAPL', 1)
            transactions = self.account.get_transactions()
            self.assertEqual(len(transactions), 1)
            self.assertEqual(transactions[0][0], 'buy')

if __name__ == '__main__':
    unittest.main()