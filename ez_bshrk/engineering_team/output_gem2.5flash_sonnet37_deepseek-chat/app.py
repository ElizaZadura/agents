import gradio as gr
import pandas as pd
from accounts import Account, get_share_price
import datetime

# Create a single account for demonstration
account = Account("demo_user")

def create_account(deposit_amount):
    try:
        amount = float(deposit_amount)
        account.deposit(amount)
        return f"Account created with initial deposit of ${amount:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def deposit_funds(amount):
    try:
        amount = float(amount)
        account.deposit(amount)
        return f"Successfully deposited ${amount:.2f}. New balance: ${account.get_balance():.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def withdraw_funds(amount):
    try:
        amount = float(amount)
        account.withdraw(amount)
        return f"Successfully withdrew ${amount:.2f}. New balance: ${account.get_balance():.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def buy_shares(symbol, quantity):
    try:
        quantity = int(quantity)
        symbol = symbol.strip().upper()
        
        # Check if symbol is valid
        try:
            price = get_share_price(symbol)
        except ValueError as e:
            return f"Error: {str(e)}"
        
        account.buy_shares(symbol, quantity)
        return f"Successfully bought {quantity} shares of {symbol} at ${price:.2f} per share. New balance: ${account.get_balance():.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def sell_shares(symbol, quantity):
    try:
        quantity = int(quantity)
        symbol = symbol.strip().upper()
        
        # Check if symbol is valid
        try:
            price = get_share_price(symbol)
        except ValueError as e:
            return f"Error: {str(e)}"
        
        account.sell_shares(symbol, quantity)
        return f"Successfully sold {quantity} shares of {symbol} at ${price:.2f} per share. New balance: ${account.get_balance():.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def get_balance_info():
    balance = account.get_balance()
    return f"Current cash balance: ${balance:.2f}"

def get_portfolio_info():
    holdings = account.get_holdings()
    
    if not holdings:
        return "You currently don't own any shares."
    
    portfolio_value = 0
    result = "Current Holdings:\n"
    
    for symbol, quantity in holdings.items():
        price = get_share_price(symbol)
        value = price * quantity
        portfolio_value += value
        result += f"- {symbol}: {quantity} shares @ ${price:.2f} = ${value:.2f}\n"
    
    total_portfolio = account.get_portfolio_value()
    profit_loss = account.get_profit_loss()
    
    result += f"\nCash Balance: ${account.get_balance():.2f}\n"
    result += f"Total Portfolio Value: ${total_portfolio:.2f}\n"
    result += f"Profit/Loss: ${profit_loss:.2f} ({'profit' if profit_loss >= 0 else 'loss'})"
    
    return result

def get_transaction_history():
    transactions = account.get_transactions()
    
    if not transactions:
        return "No transactions recorded yet."
    
    df = pd.DataFrame(transactions)
    
    # Format the dataframe for better display
    if 'timestamp' in df.columns:
        df['timestamp'] = df['timestamp'].apply(lambda x: x.split('T')[0] + ' ' + x.split('T')[1][:8])
    
    # Select and reorder columns based on availability
    cols_to_display = []
    for col in ['type', 'timestamp', 'symbol', 'quantity', 'price_per_share', 'amount', 'total_value', 'new_balance']:
        if col in df.columns:
            cols_to_display.append(col)
    
    df = df[cols_to_display]
    
    # Format numeric columns
    for col in ['amount', 'price_per_share', 'total_value', 'new_balance']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"${x:.2f}" if pd.notnull(x) else x)
    
    # Return as markdown table
    return df.to_markdown(index=False)

def check_share_price(symbol):
    try:
        symbol = symbol.strip().upper()
        price = get_share_price(symbol)
        return f"Current price of {symbol}: ${price:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def list_available_symbols():
    # This function just shows the available symbols for demonstration
    return "Available symbols for demo: AAPL, TSLA, GOOGL, MSFT, AMZN"

# Create Gradio interface
with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account"):
        with gr.Group():
            gr.Markdown("### Create Account")
            with gr.Row():
                deposit_amount_input = gr.Textbox(label="Initial Deposit ($)")
                create_btn = gr.Button("Create Account")
            create_output = gr.Textbox(label="Result")
            create_btn.click(create_account, inputs=[deposit_amount_input], outputs=[create_output])
        
        with gr.Group():
            gr.Markdown("### Deposit & Withdraw")
            with gr.Row():
                with gr.Column():
                    deposit_amount = gr.Textbox(label="Deposit Amount ($)")
                    deposit_btn = gr.Button("Deposit")
                    deposit_output = gr.Textbox(label="Result")
                with gr.Column():
                    withdraw_amount = gr.Textbox(label="Withdraw Amount ($)")
                    withdraw_btn = gr.Button("Withdraw")
                    withdraw_output = gr.Textbox(label="Result")
            
            deposit_btn.click(deposit_funds, inputs=[deposit_amount], outputs=[deposit_output])
            withdraw_btn.click(withdraw_funds, inputs=[withdraw_amount], outputs=[withdraw_output])
    
    with gr.Tab("Trading"):
        with gr.Group():
            gr.Markdown("### Stock Information")
            with gr.Row():
                symbol_input = gr.Textbox(label="Stock Symbol")
                check_price_btn = gr.Button("Check Price")
            price_output = gr.Textbox(label="Price Info")
            list_symbols_btn = gr.Button("List Available Symbols")
            symbols_output = gr.Textbox(label="Available Symbols")
            
            check_price_btn.click(check_share_price, inputs=[symbol_input], outputs=[price_output])
            list_symbols_btn.click(list_available_symbols, inputs=[], outputs=[symbols_output])
        
        with gr.Group():
            gr.Markdown("### Buy & Sell Shares")
            with gr.Row():
                with gr.Column():
                    buy_symbol = gr.Textbox(label="Symbol")
                    buy_quantity = gr.Textbox(label="Quantity")
                    buy_btn = gr.Button("Buy Shares")
                    buy_output = gr.Textbox(label="Result")
                with gr.Column():
                    sell_symbol = gr.Textbox(label="Symbol")
                    sell_quantity = gr.Textbox(label="Quantity")
                    sell_btn = gr.Button("Sell Shares")
                    sell_output = gr.Textbox(label="Result")
            
            buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=[buy_output])
            sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=[sell_output])
    
    with gr.Tab("Portfolio"):
        with gr.Group():
            gr.Markdown("### Account Overview")
            balance_btn = gr.Button("Check Balance")
            balance_output = gr.Textbox(label="Balance Info")
            
            portfolio_btn = gr.Button("View Portfolio")
            portfolio_output = gr.Textbox(label="Portfolio Info")
            
            balance_btn.click(get_balance_info, inputs=[], outputs=[balance_output])
            portfolio_btn.click(get_portfolio_info, inputs=[], outputs=[portfolio_output])
    
    with gr.Tab("Transactions"):
        with gr.Group():
            gr.Markdown("### Transaction History")
            history_btn = gr.Button("View Transaction History")
            history_output = gr.Markdown(label="Transactions")
            
            history_btn.click(get_transaction_history, inputs=[], outputs=[history_output])

# Launch the app
if __name__ == "__main__":
    demo.launch()