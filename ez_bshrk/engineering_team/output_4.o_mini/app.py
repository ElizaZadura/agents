import gradio as gr
from accounts import Account, get_share_price

# Initialize the account
account = None

def create_account(username):
    global account
    if not username:
        return "Please enter a username"
    account = Account(username)
    return f"Account created for {username}"

def deposit_funds(amount):
    if account is None:
        return "Please create an account first"
    try:
        amount = float(amount)
        account.deposit(amount)
        return f"Successfully deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def withdraw_funds(amount):
    if account is None:
        return "Please create an account first"
    try:
        amount = float(amount)
        account.withdraw(amount)
        return f"Successfully withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    if account is None:
        return "Please create an account first"
    try:
        quantity = int(quantity)
        if symbol not in ["AAPL", "TSLA", "GOOGL"]:
            return f"Invalid symbol. Available symbols: AAPL, TSLA, GOOGL"
        
        price = get_share_price(symbol)
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol} at ${price:.2f} each. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    if account is None:
        return "Please create an account first"
    try:
        quantity = int(quantity)
        if symbol not in ["AAPL", "TSLA", "GOOGL"]:
            return f"Invalid symbol. Available symbols: AAPL, TSLA, GOOGL"
        
        price = get_share_price(symbol)
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol} at ${price:.2f} each. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def get_portfolio_value():
    if account is None:
        return "Please create an account first"
    total_value = account.get_portfolio_value()
    return f"Total portfolio value: ${total_value:.2f}"

def get_profit_loss():
    if account is None:
        return "Please create an account first"
    profit_loss = account.get_profit_loss()
    if profit_loss >= 0:
        return f"Profit: ${profit_loss:.2f}"
    else:
        return f"Loss: ${abs(profit_loss):.2f}"

def get_holdings():
    if account is None:
        return "Please create an account first"
    holdings = account.get_holdings()
    if not holdings:
        return "You don't have any holdings"
    
    result = "Current Holdings:\n"
    for symbol, quantity in holdings.items():
        price = get_share_price(symbol)
        value = price * quantity
        result += f"{symbol}: {quantity} shares at ${price:.2f} each = ${value:.2f}\n"
    
    return result

def get_transactions():
    if account is None:
        return "Please create an account first"
    transactions = account.get_transactions()
    if not transactions:
        return "No transactions recorded"
    
    result = "Transaction History:\n"
    for idx, (action, symbol, quantity, price, amount) in enumerate(transactions, 1):
        result += f"{idx}. {action.capitalize()} {quantity} shares of {symbol} at ${price:.2f} each"
        result += f" - {'Cost' if action == 'buy' else 'Earnings'}: ${amount:.2f}\n"
    
    return result

def get_account_info():
    if account is None:
        return "Please create an account first"
    
    balance = account.balance
    holdings_info = get_holdings()
    portfolio_value = account.get_portfolio_value()
    profit_loss = account.get_profit_loss()
    
    result = f"Username: {account.username}\n"
    result += f"Cash Balance: ${balance:.2f}\n\n"
    result += f"{holdings_info}\n"
    result += f"Total Portfolio Value: ${portfolio_value:.2f}\n"
    if profit_loss >= 0:
        result += f"Overall Profit: ${profit_loss:.2f}"
    else:
        result += f"Overall Loss: ${abs(profit_loss):.2f}"
    
    return result

with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        with gr.Box():
            gr.Markdown("### Create Account")
            username_input = gr.Textbox(label="Username")
            create_btn = gr.Button("Create Account")
            create_output = gr.Textbox(label="Result")
            create_btn.click(create_account, inputs=username_input, outputs=create_output)
        
        with gr.Box():
            gr.Markdown("### Deposit & Withdraw Funds")
            with gr.Row():
                deposit_input = gr.Number(label="Amount to Deposit")
                withdraw_input = gr.Number(label="Amount to Withdraw")
            
            with gr.Row():
                deposit_btn = gr.Button("Deposit")
                withdraw_btn = gr.Button("Withdraw")
            
            fund_output = gr.Textbox(label="Result")
            deposit_btn.click(deposit_funds, inputs=deposit_input, outputs=fund_output)
            withdraw_btn.click(withdraw_funds, inputs=withdraw_input, outputs=fund_output)
    
    with gr.Tab("Trading"):
        with gr.Box():
            gr.Markdown("### Buy & Sell Shares")
            with gr.Row():
                symbol_input = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Symbol")
                quantity_input = gr.Number(label="Quantity", precision=0)
            
            with gr.Row():
                buy_btn = gr.Button("Buy Shares")
                sell_btn = gr.Button("Sell Shares")
            
            trade_output = gr.Textbox(label="Result")
            buy_btn.click(buy_shares, inputs=[symbol_input, quantity_input], outputs=trade_output)
            sell_btn.click(sell_shares, inputs=[symbol_input, quantity_input], outputs=trade_output)
        
        with gr.Box():
            gr.Markdown("### Market Information")
            symbol_price_input = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Symbol")
            price_btn = gr.Button("Get Price")
            price_output = gr.Textbox(label="Current Price")
            
            def get_price(symbol):
                if not symbol:
                    return "Please select a symbol"
                price = get_share_price(symbol)
                return f"Current price of {symbol}: ${price:.2f}"
            
            price_btn.click(get_price, inputs=symbol_price_input, outputs=price_output)
    
    with gr.Tab("Portfolio Information"):
        with gr.Box():
            gr.Markdown("### Account Summary")
            info_btn = gr.Button("Get Account Information")
            info_output = gr.Textbox(label="Account Information", lines=10)
            info_btn.click(get_account_info, inputs=[], outputs=info_output)
        
        with gr.Box():
            gr.Markdown("### Transaction History")
            trans_btn = gr.Button("View Transactions")
            trans_output = gr.Textbox(label="Transactions", lines=10)
            trans_btn.click(get_transactions, inputs=[], outputs=trans_output)

if __name__ == "__main__":
    demo.launch()