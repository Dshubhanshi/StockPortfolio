import sqlite3
import requests

class PortfolioDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS portfolio
                          (symbol TEXT PRIMARY KEY, quantity INTEGER)''')
        self.conn.commit()

    def add_stock(self, symbol, quantity):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO portfolio (symbol, quantity) VALUES (?, ?)", (symbol, quantity))
        self.conn.commit()

    def remove_stock(self, symbol):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM portfolio WHERE symbol=?", (symbol,))
        self.conn.commit()

    def get_portfolio(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM portfolio")
        return cursor.fetchall()

class StockAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_stock_price(self, symbol):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}"
        response = requests.get(url)
        data = response.json()
        if 'Global Quote' in data:
            return float(data['Global Quote']['05. price'])
        else:
            return None

# Example usage
if __name__ == "__main__":
    db = PortfolioDB("portfolio.db")
    api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
    stock_api = StockAPI(api_key)
    
    # Add stocks to the portfolio
    db.add_stock("AAPL", 10)
    db.add_stock("MSFT", 5)
    
    # Remove a stock from the portfolio
    db.remove_stock("AAPL")
    
    # Print the current portfolio
    print("Current Portfolio:")
    portfolio = db.get_portfolio()
    for symbol, quantity in portfolio:
        price = stock_api.get_stock_price(symbol)
        if price is not None:
            print(f"Symbol: {symbol}, Quantity: {quantity}, Price: ${price}")
        else:
            print(f"Symbol: {symbol}, Quantity: {quantity}, Price: Unknown")
