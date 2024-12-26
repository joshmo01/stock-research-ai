"""Main Streamlit application."""
import streamlit as st
from pathlib import Path

from stock_research.config.settings import settings
from stock_research.ui.components import fundamental, technical, sentiment

def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=settings.PAGE_TITLE,
        page_icon=settings.PAGE_ICON,
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 0 !important;
        }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            padding-left: 5rem !important;
            padding-right: 5rem !important;
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
        .analysis-section {
            margin-top: 2rem;
            padding: 2rem;
            border-radius: 10px;
            background-color: #ffffff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stMetric {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        h1 {
            padding: 1rem 0;
            color: #1e3a8a;
            text-align: center;
            font-size: 2.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    setup_page()
    
    st.title("🚀 Stock Market Research Assistant")
    
    # User input section with better styling
    st.markdown("""
        <style>
        .input-section {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input(
            "📈 Enter Stock Ticker:",
            value="AAPL",
            help="Enter the stock symbol (e.g., AAPL for Apple Inc.)"
        ).upper()
    
    with col2:
        analyze_button = st.button(
            "🔍 Analyze",
            type="primary",
            use_container_width=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_button:
        if not ticker:
            st.error("Please enter a stock ticker")
            return
        
        # Create tabs with better styling
        tab1, tab2, tab3 = st.tabs([
            "📊 Fundamental Analysis",
            "📈 Technical Analysis",
            "📰 Sentiment Analysis"
        ])
        
        with tab1:
            st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
            fundamental.render_analysis(ticker)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
            technical.render_analysis(ticker)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
            sentiment.render_analysis(ticker)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
