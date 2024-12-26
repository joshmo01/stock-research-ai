"""Technical analysis component."""
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate technical indicators for the given dataframe."""
    # Calculate moving averages
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['SMA200'] = df['Close'].rolling(window=200).mean()
    
    # Calculate RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Calculate MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Calculate Bollinger Bands
    df['BB_middle'] = df['Close'].rolling(window=20).mean()
    df['BB_upper'] = df['BB_middle'] + 2*df['Close'].rolling(window=20).std()
    df['BB_lower'] = df['BB_middle'] - 2*df['Close'].rolling(window=20).std()
    
    return df

def plot_technical_chart(df: pd.DataFrame) -> go.Figure:
    """Create technical analysis chart."""
    # Create figure with secondary y-axis
    fig = make_subplots(rows=3, cols=1, 
                       shared_xaxes=True,
                       vertical_spacing=0.05,
                       row_heights=[0.6, 0.2, 0.2])
    
    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Price'
    ), row=1, col=1)
    
    # Add moving averages
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['SMA20'],
        name='SMA20',
        line=dict(color='blue', width=1)
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['SMA50'],
        name='SMA50',
        line=dict(color='orange', width=1)
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['SMA200'],
        name='SMA200',
        line=dict(color='red', width=1)
    ), row=1, col=1)
    
    # Add Bollinger Bands
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['BB_upper'],
        name='BB Upper',
        line=dict(color='gray', width=1, dash='dash')
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['BB_lower'],
        name='BB Lower',
        line=dict(color='gray', width=1, dash='dash'),
        fill='tonexty'
    ), row=1, col=1)
    
    # Add RSI
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['RSI'],
        name='RSI',
        line=dict(color='purple', width=1)
    ), row=2, col=1)
    
    # Add RSI levels
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    # Add MACD
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MACD'],
        name='MACD',
        line=dict(color='blue', width=1)
    ), row=3, col=1)
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Signal_Line'],
        name='Signal Line',
        line=dict(color='orange', width=1)
    ), row=3, col=1)
    
    # Update layout
    fig.update_layout(
        title='Technical Analysis Chart',
        yaxis_title='Price',
        yaxis2_title='RSI',
        yaxis3_title='MACD',
        xaxis_rangeslider_visible=False,
        height=800
    )
    
    return fig

def get_technical_signals(df: pd.DataFrame) -> dict:
    """Generate technical analysis signals."""
    current_price = df['Close'].iloc[-1]
    signals = {
        "Trend Signals": {
            "Price vs SMA20": "Bullish" if current_price > df['SMA20'].iloc[-1] else "Bearish",
            "Price vs SMA50": "Bullish" if current_price > df['SMA50'].iloc[-1] else "Bearish",
            "Price vs SMA200": "Bullish" if current_price > df['SMA200'].iloc[-1] else "Bearish",
        },
        "Momentum Signals": {
            "RSI": "Overbought" if df['RSI'].iloc[-1] > 70 else "Oversold" if df['RSI'].iloc[-1] < 30 else "Neutral",
            "MACD": "Bullish" if df['MACD'].iloc[-1] > df['Signal_Line'].iloc[-1] else "Bearish",
        },
        "Volatility Signals": {
            "Bollinger Bands": "Upper Band" if current_price > df['BB_upper'].iloc[-1] else 
                             "Lower Band" if current_price < df['BB_lower'].iloc[-1] else "Middle Band",
        }
    }
    return signals

def render_analysis(ticker: str) -> None:
    """Render technical analysis for a stock."""
    st.header(f"Technical Analysis for {ticker}")
    
    try:
        # Get historical data
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        
        if len(hist) == 0:
            st.warning(f"No historical data found for {ticker}")
            return
        
        # Calculate technical indicators
        df = calculate_technical_indicators(hist)
        
        # Plot technical chart
        fig = plot_technical_chart(df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display technical signals
        signals = get_technical_signals(df)
        
        st.subheader("Technical Signals")
        for category, category_signals in signals.items():
            st.write(f"**{category}:**")
            cols = st.columns(len(category_signals))
            for col, (signal_name, value) in zip(cols, category_signals.items()):
                col.metric(signal_name, value)
        
        # Display key levels
        st.subheader("Key Price Levels")
        current_price = df['Close'].iloc[-1]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Support (BB Lower)", f"${df['BB_lower'].iloc[-1]:.2f}")
        
        with col2:
            st.metric("Current Price", f"${current_price:.2f}")
        
        with col3:
            st.metric("Resistance (BB Upper)", f"${df['BB_upper'].iloc[-1]:.2f}")
        
    except Exception as e:
        st.error(f"Error analyzing technicals for {ticker}: {str(e)}")
        st.info("Please try again or choose a different stock.")