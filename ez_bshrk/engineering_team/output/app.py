import gradio as gr
from accounts import Account, get_share_price

# Initialize account
account = None

def create_account(account_id, initial_deposit):
    global account
    try:
        initial_deposit = float(initial_deposit)
        account = Account(account_id, initial_deposit)
        return f"Account {account_id} created with initial deposit of ${initial_deposit:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def deposit(amount):
    if account is None:
        return "Please create an account first."
    try:
        amount = float(amount)
        if account.deposit(amount):
            return f"Successfully deposited ${amount:.2f}. New balance: ${account.get_balance():.2f}"
        else:
            return "Deposit failed. Amount must be positive."
    except ValueError:
        return "Please enter a valid number."

def withdraw(amount):
    if account is None:
        return "Please create an account first."
    try:
        amount = float(amount)
        if account.withdraw(amount):
            return f"Successfully withdrew ${amount:.2f}. New balance: ${account.get_balance():.2f}"
        else:
            return "Withdrawal failed. Amount must be positive and not exceed your balance."
    except ValueError:
        return "Please enter a valid number."

def buy_shares(symbol, quantity):
    if account is None:
        return "Please create an account first."
    try:
        quantity = int(quantity)
        if account.buy_shares(symbol, quantity):
            price = get_share_price(symbol)
            return f"Successfully bought {quantity} shares of {symbol} at ${price:.2f} per share. Total cost: ${price * quantity:.2f}"
        else:
            return "Purchase failed. Check if symbol exists, quantity is positive, or if you have enough funds."
    except ValueError:
        return "Please enter a valid quantity."

def sell_shares(symbol, quantity):
    if account is None:
        return "Please create an account first."
    try:
        quantity = int(quantity)
        if account.sell_shares(symbol, quantity):
            price = get_share_price(symbol)
            return f"Successfully sold {quantity} shares of {symbol} at ${price:.2f} per share. Total revenue: ${price * quantity:.2f}"
        else:
            return "Sale failed. Check if you own enough shares of this symbol or if quantity is positive."
    except ValueError:
        return "Please enter a valid quantity."

def get_holdings():
    if account is None:
        return "Please create an account first."
    holdings = account.get_holdings()
    if not holdings:
        return "No holdings in portfolio."
    
    result = "Current Holdings:\n"
    for symbol, quantity in holdings.items():
        price = get_share_price(symbol)
        value = price * quantity
        result += f"{symbol}: {quantity} shares at ${price:.2f} = ${value:.2f}\n"
    return result

def get_portfolio_value():
    if account is None:
        return "Please create an account first."
    
    portfolio_value = account.get_portfolio_value()
    holdings_value = portfolio_value - account.get_balance()
    
    result = f"Cash balance: ${account.get_balance():.2f}\n"
    result += f"Holdings value: ${holdings_value:.2f}\n"
    result += f"Total portfolio value: ${portfolio_value:.2f}"
    return result

def get_profit_loss():
    if account is None:
        return "Please create an account first."
    
    pl_data = account.get_profit_loss()
    
    result = f"Total capital contributed: ${pl_data['total_capital_contributed']:.2f}\n"
    result += f"Current portfolio value: ${pl_data['current_portfolio_value']:.2f}\n"
    
    if pl_data['profit_loss'] >= 0:
        result += f"Profit: ${pl_data['profit_loss']:.2f}"
    else:
        result += f"Loss: ${abs(pl_data['profit_loss']):.2f}"
    
    return result

def get_transactions():
    if account is None:
        return "Please create an account first."
    
    transactions = account.get_transactions()
    if not transactions:
        return "No transactions recorded."
    
    result = "Transaction History:\n"
    for idx, txn in enumerate(transactions, 1):
        result += f"{idx}. {txn['timestamp'][:19]} - {txn['type'].capitalize()}"
        
        if txn['type'] in ['deposit', 'withdraw']:
            result += f": ${txn['amount']:.2f}"
        elif txn['type'] in ['buy', 'sell']:
            result += f": {txn['quantity']} {txn['symbol']} at ${txn['price']:.2f}/share"
            result += f" (${txn['amount']:.2f} total)"
        
        result += f" - Balance: ${txn['current_balance']:.2f}\n"
    
    return result

def get_available_stocks():
    return "Available Stocks for Trading:\nAAPL: $150.00\nTSLA: $700.00\nGOOGL: $2800.00"

with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        with gr.Group():
            gr.Markdown("### Create Account")
            with gr.Row():
                account_id_input = gr.Textbox(label="Account ID")
                initial_deposit_input = gr.Textbox(label="Initial Deposit ($)")
            create_account_btn = gr.Button("Create Account")
            create_account_output = gr.Textbox(label="Result", interactive=False)
            create_account_btn.click(create_account, [account_id_input, initial_deposit_input], create_account_output)
        
        with gr.Group():
            gr.Markdown("### Deposit/Withdraw")
            with gr.Row():
                deposit_input = gr.Textbox(label="Deposit Amount ($)")
                withdraw_input = gr.Textbox(label="Withdraw Amount ($)")
            with gr.Row():
                deposit_btn = gr.Button("Deposit")
                withdraw_btn = gr.Button("Withdraw")
            money_output = gr.Textbox(label="Result", interactive=False)
            deposit_btn.click(deposit, [deposit_input], money_output)
            withdraw_btn.click(withdraw, [withdraw_input], money_output)
    
    with gr.Tab("Trading"):
        gr.Markdown("### Stock Information")
        stock_info_btn = gr.Button("Show Available Stocks")
        stock_info_output = gr.Textbox(label="Available Stocks", interactive=False)
        stock_info_btn.click(get_available_stocks, [], stock_info_output)
        
        with gr.Group():
            gr.Markdown("### Buy/Sell Shares")
            with gr.Row():
                symbol_input = gr.Textbox(label="Stock Symbol (e.g., AAPL)")
                quantity_input = gr.Textbox(label="Quantity")
            with gr.Row():
                buy_btn = gr.Button("Buy Shares")
                sell_btn = gr.Button("Sell Shares")
            trading_output = gr.Textbox(label="Result", interactive=False)
            buy_btn.click(buy_shares, [symbol_input, quantity_input], trading_output)
            sell_btn.click(sell_shares, [symbol_input, quantity_input], trading_output)
    
    with gr.Tab("Portfolio"):
        with gr.Row():
            holdings_btn = gr.Button("Show Holdings")
            portfolio_value_btn = gr.Button("Show Portfolio Value")
            profit_loss_btn = gr.Button("Show Profit/Loss")
        
        portfolio_output = gr.Textbox(label="Portfolio Information", interactive=False, lines=10)
        
        holdings_btn.click(get_holdings, [], portfolio_output)
        portfolio_value_btn.click(get_portfolio_value, [], portfolio_output)
        profit_loss_btn.click(get_profit_loss, [], portfolio_output)
    
    with gr.Tab("Transactions"):
        transactions_btn = gr.Button("Show Transaction History")
        transactions_output = gr.Textbox(label="Transactions", interactive=False, lines=15)
        transactions_btn.click(get_transactions, [], transactions_output)

if __name__ == "__main__":
    demo.launch()