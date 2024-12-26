"""Fundamental analysis component."""
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def format_large_number(number: float) -> str:
    """Format large numbers into billions/millions."""
    if number >= 1e9:
        return f"${number/1e9:.2f}B"
    elif number >= 1e6:
        return f"${number/1e6:.2f}M"
    else:
        return f"${number:,.2f}"

def render_analysis(ticker: str) -> None:
    """Render fundamental analysis for a stock."""
    try:
        # Get stock data
        stock = yf.Ticker(ticker)
        info = stock.info

        # Custom styling
        st.markdown("""
            <style>
                .metric-row {
                    background-color: #ffffff;
                    padding: 1rem;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    margin-bottom: 1rem;
                }
                .section-title {
                    color: #1e3a8a;
                    padding: 0.5rem 0;
                    margin: 1rem 0;
                    border-bottom: 2px solid #1e3a8a;
                }
                .subsection {
                    background-color: #f8f9fa;
                    padding: 1rem;
                    border-radius: 8px;
                    margin: 0.5rem 0;
                }
            </style>
        """, unsafe_allow_html=True)

        # Company Overview
        st.markdown("<h2 class='section-title'>💼 Company Overview</h2>", unsafe_allow_html=True)
        st.markdown('<div class="metric-row">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Market Cap",
                format_large_number(info.get('marketCap', 0)),
                help="Total market value of shares"
            )
        
        with col2:
            st.metric(
                "P/E Ratio",
                f"{info.get('trailingPE', 0):.2f}",
                help="Price to Earnings Ratio"
            )
        
        with col3:
            st.metric(
                "Dividend Yield",
                f"{info.get('dividendYield', 0) * 100:.2f}%",
                help="Annual dividend yield"
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Key Metrics Section
        st.markdown("<h2 class='section-title'>📊 Key Financial Metrics</h2>", unsafe_allow_html=True)
        met_col1, met_col2 = st.columns(2)
        
        with met_col1:
            st.markdown('<div class="subsection">', unsafe_allow_html=True)
            st.subheader("Profitability Metrics")
            metrics = {
                'Gross Margin': f"{info.get('grossMargins', 0) * 100:.2f}%",
                'Operating Margin': f"{info.get('operatingMargins', 0) * 100:.2f}%",
                'Net Margin': f"{info.get('profitMargins', 0) * 100:.2f}%",
                'ROE': f"{info.get('returnOnEquity', 0) * 100:.2f}%",
                'ROA': f"{info.get('returnOnAssets', 0) * 100:.2f}%"
            }
            for metric, value in metrics.items():
                st.metric(metric, value)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with met_col2:
            st.markdown('<div class="subsection">', unsafe_allow_html=True)
            st.subheader("Valuation Metrics")
            metrics = {
                'P/E Ratio': f"{info.get('trailingPE', 0):.2f}",
                'P/B Ratio': f"{info.get('priceToBook', 0):.2f}",
                'P/S Ratio': f"{info.get('priceToSalesTrailing12Months', 0):.2f}",
                'EV/EBITDA': f"{info.get('enterpriseToEbitda', 0):.2f}",
                'PEG Ratio': f"{info.get('pegRatio', 0):.2f}"
            }
            for metric, value in metrics.items():
                st.metric(metric, value)
            st.markdown('</div>', unsafe_allow_html=True)

        # Growth Section
        st.markdown("<h2 class='section-title'>📈 Growth Analysis</h2>", unsafe_allow_html=True)
        st.markdown('<div class="metric-row">', unsafe_allow_html=True)
        growth_col1, growth_col2 = st.columns(2)
        
        with growth_col1:
            revenue_growth = info.get('revenueGrowth', 0) * 100
            st.metric(
                "Revenue Growth (YoY)",
                f"{revenue_growth:.2f}%",
                help="Year-over-year revenue growth"
            )
        
        with growth_col2:
            earnings_growth = info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0
            st.metric(
                "Earnings Growth (YoY)",
                f"{earnings_growth:.2f}%",
                help="Year-over-year earnings growth"
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Financial Health Section
        st.markdown("<h2 class='section-title'>🏦 Financial Health</h2>", unsafe_allow_html=True)
        st.markdown('<div class="metric-row">', unsafe_allow_html=True)
        health_col1, health_col2, health_col3 = st.columns(3)
        
        with health_col1:
            st.metric(
                "Quick Ratio",
                f"{info.get('quickRatio', 0):.2f}",
                help="Measure of company's short-term liquidity"
            )
        
        with health_col2:
            st.metric(
                "Debt/Equity",
                f"{info.get('debtToEquity', 0):.2f}%",
                help="Measure of financial leverage"
            )
        
        with health_col3:
            st.metric(
                "Current Ratio",
                f"{info.get('currentRatio', 0):.2f}",
                help="Measure of company's liquidity"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error analyzing fundamentals for {ticker}: {str(e)}")
        st.info("Please try again or choose a different stock.")