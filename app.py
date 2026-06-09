import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="MarketMind AI", layout="wide")

st.title("MarketMind AI 📈")

ticker = st.text_input("Enter a stock ticker (e.g., AAPL)")

if ticker:

    # -----------------------
    # DATA
    # -----------------------
    stock = yf.Ticker(ticker)
    info = stock.info
    data = stock.history(period="6mo")

    # -----------------------
    # TABS
    # -----------------------
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Overview", "📰 News", "🧑‍🤝‍🧑 Competitors", "🧠 Insights"]
    )

    # -----------------------
    # TAB 1: OVERVIEW
    # -----------------------
    with tab1:
        st.subheader(info.get("longName", ticker))

        col1, col2, col3 = st.columns(3)

        col1.metric("Price", info.get("currentPrice"))
        col2.metric("Market Cap", info.get("marketCap"))
        col3.metric("Sector", info.get("sector"))

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

        st.plotly_chart(fig, use_container_width=True)

    # -----------------------
    # TAB 2: NEWS + SENTIMENT
    # -----------------------
    with tab2:
        st.subheader("Market News Feed")

        rss_url = f"https://news.google.com/rss/search?q={ticker}+stock"
        news_feed = feedparser.parse(rss_url)

        analyzer = SentimentIntensityAnalyzer()
        scores = []
        headlines = []

        for entry in news_feed.entries[:7]:
            title = entry.title
            headlines.append(title)

            sentiment = analyzer.polarity_scores(title)
            compound = sentiment["compound"]
            scores.append(compound)

            st.markdown(f"**{title}**")
            st.caption(entry.published)
            st.write(entry.link)

            if compound >= 0.05:
                st.write("🟢 Positive")
            elif compound <= -0.05:
                st.write("🔴 Negative")
            else:
                st.write("⚪ Neutral")

            st.markdown("---")

    # -----------------------
    # TAB 3: COMPETITORS
    # -----------------------
    with tab3:
        st.subheader("Competitors")

        competitors = {
            "AAPL": ["MSFT", "GOOGL", "AMZN"],
            "MSFT": ["AAPL", "GOOGL", "NVDA"],
            "NVDA": ["AMD", "INTC", "TSM"],
            "TSLA": ["F", "GM", "RIVN"]
        }

        if ticker.upper() in competitors:
            for comp in competitors[ticker.upper()]:
                comp_data = yf.Ticker(comp).info
                st.write(f"**{comp}** - {comp_data.get('currentPrice', 'N/A')}")
        else:
            st.write("No competitor data available.")

    # -----------------------
    # TAB 4: INSIGHTS + AI EXPLANATION
    # -----------------------
    with tab4:
        st.subheader("Market Intelligence")

        if len(scores) > 0:
            avg = sum(scores) / len(scores)

            if avg >= 0.05:
                label = "🟢 Bullish"
            elif avg <= -0.05:
                label = "🔴 Bearish"
            else:
                label = "⚪ Neutral"

            # -----------------------
            # SENTIMENT SUMMARY
            # -----------------------
            st.markdown(f"### Overall Sentiment: {label}")
            st.write(f"Sentiment Score: {avg:.3f}")

            st.progress((avg + 1) / 2)

            # -----------------------
            # AI EXPLANATION LAYER (NEW)
            # -----------------------
            st.subheader("🧠 AI Explanation")

            if len(headlines) > 0:

                summary_text = " ".join(headlines)

                # simple AI-style reasoning (no external API needed)
                explanation = ""

                if avg > 0.05:
                    explanation = (
                        f"{ticker.upper()} is showing a mildly positive outlook. "
                        "Recent news headlines suggest optimistic market sentiment, "
                        "likely driven by positive corporate developments or investor confidence."
                    )
                elif avg < -0.05:
                    explanation = (
                        f"{ticker.upper()} is showing negative pressure. "
                        "Recent headlines suggest concerns or uncertainty that may be affecting investor sentiment."
                    )
                else:
                    explanation = (
                        f"{ticker.upper()} is relatively neutral. "
                        "News sentiment is mixed with no strong directional bias."
                    )

                st.write(explanation)

                st.caption("Based on aggregated news sentiment + headline analysis")

            else:
                st.write("Not enough news data for explanation.")

        else:
            st.write("Not enough data for sentiment analysis yet.")