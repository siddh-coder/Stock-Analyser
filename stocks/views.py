import yfinance as yf
import plotly.graph_objects as go
from django.shortcuts import render

def stock_chart(request):
    symbol = request.GET.get("symbol", "AAPL")  # Default: Apple
    period = request.GET.get("period", "1mo")  # Default: 1 Month
    graph_type = request.GET.get("graph_type", "line")  # Default: Line chart
    currency = request.GET.get("currency", "USD")  # Default: USD

    stock_data = yf.Ticker(symbol).history(period=period)

    if stock_data.empty:
        return render(request, "stocks/stock_chart.html", {"error": "Invalid stock symbol or no data available."})

    # Fetch USD to INR conversion rate
    conversion_rate = 1  # Default to USD
    if currency == "INR":
        forex_data = yf.Ticker("USDINR=X").history(period="1d")
        if not forex_data.empty:
            conversion_rate = forex_data["Close"].iloc[-1]

    # Convert prices to selected currency
    stock_data["Open"] *= conversion_rate
    stock_data["High"] *= conversion_rate
    stock_data["Low"] *= conversion_rate
    stock_data["Close"] *= conversion_rate

    fig = go.Figure()

    if graph_type == "line":
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data["Close"], mode="lines", name=f"Closing Price ({currency})"))
    elif graph_type == "bar":
        fig.add_trace(go.Bar(x=stock_data.index, y=stock_data["Close"], name=f"Closing Price ({currency})"))
    elif graph_type == "candlestick":
        fig.add_trace(go.Candlestick(
            x=stock_data.index,
            open=stock_data["Open"],
            high=stock_data["High"],
            low=stock_data["Low"],
            close=stock_data["Close"],
            name="Candlestick Chart"
        ))

    fig.update_layout(title=f"{symbol} Stock Price in {currency}", xaxis_title="Date", yaxis_title=f"Price ({currency})", hovermode="x")

    graph_html = fig.to_html(full_html=False)

    return render(request, "stocks/stock_chart.html", {"graph_html": graph_html})

