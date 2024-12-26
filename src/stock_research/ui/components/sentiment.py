"""Sentiment analysis component with social media integration."""
import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import requests
from plotly.subplots import make_subplots

def calculate_sentiment(text: str) -> int:
    """Calculate a simple sentiment score based on keywords."""
    if not isinstance(text, str):
        return 0
        
    positive_words = ['rise', 'gain', 'up', 'surge', 'jump', 'boost', 'positive', 'strong', 'success', 'bullish']
    negative_words = ['fall', 'drop', 'down', 'decline', 'weak', 'negative', 'loss', 'risk', 'concern', 'bearish']
    
    text = text.lower()
    positive_count = sum(1 for word in positive_words if word in text)
    negative_count = sum(1 for word in negative_words if word in text)
    
    return positive_count - negative_count

def parse_news_date(date_str: str) -> datetime:
    """Parse date string to datetime object."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return datetime.now()

def get_stocktwits_sentiment(symbol: str) -> dict:
    """Fetch sentiment data from StockTwits API."""
    try:
        url = f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])
            
            sentiment_counts = {
                'bullish': 0,
                'bearish': 0,
                'neutral': 0
            }
            
            recent_messages = []
            for msg in messages:
                sentiment = msg.get('entities', {}).get('sentiment', {}).get('basic', 'neutral')
                sentiment_counts[sentiment] += 1
                
                recent_messages.append({
                    'message': msg.get('body', ''),
                    'created_at': msg.get('created_at', ''),
                    'user': msg.get('user', {}).get('username', ''),
                    'sentiment': sentiment
                })
            
            return {
                'sentiment_counts': sentiment_counts,
                'recent_messages': recent_messages[:10],
                'total_messages': len(messages)
            }
        
        return None
    except Exception as e:
        st.error(f"Error fetching StockTwits data: {str(e)}")
        return None

def render_news_sentiment(ticker: str):
    """Render news sentiment analysis."""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        
        if not news:
            st.warning(f"No recent news found for {ticker}")
            return

        processed_news = []
        for item in news:
            try:
                if 'content' in item:
                    content = item['content']
                    title = content.get('title', '')
                    summary = content.get('summary', '')
                    date = content.get('pubDate', '')
                    url = content.get('previewUrl', '')
                else:
                    title = item.get('title', '')
                    summary = item.get('summary', '')
                    date = item.get('pubDate', '')
                    url = item.get('previewUrl', '')

                sentiment_score = calculate_sentiment(title) + calculate_sentiment(summary)
                sentiment_category = (
                    'positive' if sentiment_score > 0
                    else 'negative' if sentiment_score < 0
                    else 'neutral'
                )

                news_item = {
                    'title': title,
                    'summary': summary,
                    'date': parse_news_date(date) if date else datetime.now(),
                    'url': url,
                    'sentiment_score': sentiment_score,
                    'sentiment_category': sentiment_category
                }
                processed_news.append(news_item)
            except Exception as e:
                continue

        if processed_news:
            # Sentiment Overview
            st.subheader("📊 News Sentiment Overview")
            
            total_news = len(processed_news)
            positive_news = sum(1 for item in processed_news if item['sentiment_category'] == 'positive')
            negative_news = sum(1 for item in processed_news if item['sentiment_category'] == 'negative')
            neutral_news = sum(1 for item in processed_news if item['sentiment_category'] == 'neutral')

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total News", total_news)
            with col2:
                st.metric("Positive News", positive_news, f"{(positive_news/total_news*100):.1f}%")
            with col3:
                st.metric("Negative News", negative_news, f"{(negative_news/total_news*100):.1f}%")
            with col4:
                st.metric("Neutral News", neutral_news, f"{(neutral_news/total_news*100):.1f}%")

            # Recent News
            st.subheader("📰 Recent News")
            processed_news.sort(key=lambda x: x['date'], reverse=True)
            
            for news_item in processed_news:
                st.markdown(
                    f'<div class="news-card sentiment-{news_item["sentiment_category"]}">',
                    unsafe_allow_html=True
                )
                
                st.markdown(f'<div class="news-title">{news_item["title"]}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="news-meta">Published on {news_item["date"].strftime("%Y-%m-%d %H:%M")}</div>',
                    unsafe_allow_html=True
                )
                
                if news_item['summary']:
                    with st.expander("Read Summary"):
                        st.write(news_item['summary'])
                        if news_item['url']:
                            st.markdown(f"[Read full article]({news_item['url']})")

                st.markdown('</div>', unsafe_allow_html=True)

            # Sentiment Timeline
            st.subheader("📈 News Sentiment Timeline")
            df = pd.DataFrame(processed_news)
            
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['sentiment_score'],
                    mode='lines+markers',
                    name='Sentiment',
                    text=df['title'],
                    hovertemplate="<b>%{text}</b><br>Sentiment: %{y}<extra></extra>"
                )
            )
            
            fig.update_layout(
                height=400,
                margin=dict(l=0, r=0, t=30, b=0),
                yaxis_title="Sentiment Score",
                xaxis_title="Date",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Could not process any news items.")

    except Exception as e:
        st.error(f"Error analyzing news for {ticker}: {str(e)}")

def render_social_sentiment(ticker: str):
    """Render social media sentiment analysis."""
    st.subheader("📱 Social Media Sentiment")
    
    stocktwits_data = get_stocktwits_sentiment(ticker)
    
    if stocktwits_data:
        # Social Sentiment Overview
        st.markdown('<div class="sentiment-section">', unsafe_allow_html=True)
        counts = stocktwits_data['sentiment_counts']
        total = sum(counts.values())
        
        if total > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Messages", total)
            
            with col2:
                bullish_pct = (counts['bullish'] / total * 100)
                st.metric("Bullish", counts['bullish'], f"{bullish_pct:.1f}%")
            
            with col3:
                bearish_pct = (counts['bearish'] / total * 100)
                st.metric("Bearish", counts['bearish'], f"{bearish_pct:.1f}%")
            
            with col4:
                neutral_pct = (counts['neutral'] / total * 100)
                st.metric("Neutral", counts['neutral'], f"{neutral_pct:.1f}%")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recent Messages
            st.subheader("Recent StockTwits Messages")
            for msg in stocktwits_data['recent_messages']:
                sentiment_color = {
                    'bullish': 'sentiment-positive',
                    'bearish': 'sentiment-negative',
                    'neutral': 'sentiment-neutral'
                }.get(msg['sentiment'], 'sentiment-neutral')
                
                st.markdown(
                    f'<div class="social-card {sentiment_color}">',
                    unsafe_allow_html=True
                )
                st.markdown(f"**@{msg['user']}**")
                st.write(msg['message'])
                st.caption(f"Posted on {msg['created_at']}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Sentiment Distribution Chart
            st.subheader("Social Sentiment Distribution")
            fig = go.Figure()
            
            fig.add_trace(go.Pie(
                labels=['Bullish', 'Bearish', 'Neutral'],
                values=[counts['bullish'], counts['bearish'], counts['neutral']],
                hole=.3,
                marker_colors=['#10B981', '#EF4444', '#6B7280'],
                textinfo='percent+label'
            ))
            
            fig.update_layout(
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No sentiment data available.")
    else:
        st.warning("Unable to fetch social media sentiment data at this time.")

def render_analysis(ticker: str) -> None:
    """Render sentiment analysis for a stock."""
    try:
        # Custom styling
        st.markdown("""
            <style>
            .news-card, .social-card {
                background-color: white;
                padding: 1rem;
                border-radius: 8px;
                margin: 0.5rem 0;
                border: 1px solid #e0e0e0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .news-title {
                font-size: 1.1rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            .news-meta {
                font-size: 0.9rem;
                color: #666;
                margin-bottom: 1rem;
            }
            .sentiment-positive {
                border-left: 4px solid #10B981;
            }
            .sentiment-negative {
                border-left: 4px solid #EF4444;
            }
            .sentiment-neutral {
                border-left: 4px solid #6B7280;
            }
            .sentiment-section {
                background-color: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Create tabs for different sentiment sources
        news_tab, social_tab = st.tabs(["📰 News Sentiment", "📱 Social Media Sentiment"])
        
        with news_tab:
            render_news_sentiment(ticker)
        
        with social_tab:
            render_social_sentiment(ticker)

    except Exception as e:
        st.error(f"Error analyzing sentiment: {str(e)}")
        st.info("Please try again or choose a different stock.")