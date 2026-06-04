import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("MarketMind AI 📈")

ticker = st.text_input("Enter a stock ticker (e.g., AAPL)")

if ticker:
    stock = yf.Ticker(ticker)

    info = stock.info

    st.subheader(info.get("longName", ticker))

    st.write("Current Price:", info.get("currentPrice"))
    st.write("Market Cap:", info.get("marketCap"))
    st.write("Sector:", info.get("sector"))

    data = stock.history(period="6mo")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Price"
        )
    )

    fig.update_layout(
        title=f"{ticker.upper()} Stock Price (6 Months)",
        xaxis_title="Date",
        yaxis_title="Price ($)"
    )

    st.plotly_chart(fig)