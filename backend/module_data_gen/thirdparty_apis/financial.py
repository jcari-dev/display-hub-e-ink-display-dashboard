import yfinance as yf


def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)

        # Get today's historical data
        today_data = stock.history(period="1d")
        if today_data.empty:
            return "No data available for today."

        # Get the previous close price
        previous_close = stock.info.get("previousClose")
        if previous_close is None:
            return "Previous close data not available."

        # Get the current price
        current_price = stock.info.get("currentPrice")
        if current_price is None:
            return "Current price data not available."

        # Calculate the percentage change
        price_difference_percent = (
            (current_price - previous_close) / previous_close) * 100

        # Format the data
        stock_data = f"{ticker}\n{current_price:.2f}\n{price_difference_percent:.2f}%"
        return stock_data
    except Exception as e:
        print(e)
        return f"Error fetching stock data: {e}"
