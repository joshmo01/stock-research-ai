import streamlit as st
from pathlib import Path

from ..config.settings import settings
from .components import fundamental, technical, sentiment

def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=settings.PAGE_TITLE,
        page_icon=settings.PAGE_ICON,
        layout="wide",
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #0e1117;
            border-radius: 4px;
            color: #fafafa;
            padding: 10px 24px;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    setup_page()
    
    st.title(settings.PAGE_TITLE)
    
    # User input
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker:",
            value="AAPL",
        ).upper()
    
    with col2:
        if st.button("Analyze", type="primary", use_container_width=True):
            if not ticker:
                st.error("Please enter a stock ticker")
                return
            
            # Create tabs for different analyses
            tab1, tab2, tab3 = st.tabs([
                "Fundamental Analysis 📊",
                "Technical Analysis 📈",
                "Sentiment Analysis 📰"
            ])
            
            # Run analyses in parallel (future enhancement)
            with tab1:
                fundamental.render_analysis(ticker)
            
            with tab2:
                technical.render_analysis(ticker)
            
            with tab3:
                sentiment.render_analysis(ticker)

if __name__ == "__main__":
    main()