import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="Stock Analysis Dashboard")
st.title("🚀 실시간 통합 주식 분석 및 뉴스 대시보드")

# Cache function to reduce API calls
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker_input, period="1y"):
    """Fetch stock data with caching"""
    try:
        ticker = yf.Ticker(ticker_input)
        df = ticker.history(period=period, interval="1d")
        if df.empty:
            return None, None
        return df, ticker
    except Exception as e:
        return None, None

def calculate_indicators(df):
    """Calculate technical indicators"""
    try:
        df['SMA_50'] = ta.sma(df['Close'], length=50)
        df['SMA_200'] = ta.sma(df['Close'], length=200)
        df['RSI'] = ta.rsi(df['Close'], length=14)
        bb = ta.bbands(df['Close'], length=20)
        df = pd.concat([df, bb], axis=1)
        return df
    except Exception as e:
        st.error(f"Error calculating indicators: {str(e)}")
        return None

def display_metrics(df):
    """Display key metrics"""
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        current_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        price_change = current_price - prev_price
        price_change_pct = (price_change / prev_price) * 100
        
        col1.metric(
            "현재가",
            f"${current_price:.2f}",
            f"{price_change:.2f} ({price_change_pct:.2f}%)"
        )
        
        col2.metric(
            "RSI (14일)",
            f"{df['RSI'].iloc[-1]:.2f}",
            delta=None
        )
        
        col3.metric(
            "50일 이동평균",
            f"${df['SMA_50'].iloc[-1]:.2f}",
            delta=None
        )
        
        col4.metric(
            "변동성(BB 상단)",
            f"${df.iloc[-1]['BBU_20_2.0']:.2f}",
            delta=None
        )
    except Exception as e:
        st.error(f"Error displaying metrics: {str(e)}")

def display_chart(df, ticker_input):
    """Display interactive chart"""
    try:
        st.subheader(f"📈 {ticker_input} 가격 및 이동평균")
        chart_data = df[['Close', 'SMA_50', 'SMA_200']].copy()
        st.line_chart(chart_data)
    except Exception as e:
        st.error(f"Error displaying chart: {str(e)}")

def display_data_table(df):
    """Display recent data table"""
    try:
        st.subheader("📋 최근 10일 데이터 지표")
        display_df = df[['Close', 'SMA_50', 'SMA_200', 'RSI']].tail(10).copy()
        display_df = display_df.round(2)
        st.dataframe(display_df, use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying table: {str(e)}")

def display_news(ticker):
    """Display related news"""
    try:
        st.subheader("📰 관련 실시간 뉴스")
        news = ticker.news
        
        if not news:
            st.info("뉴스를 찾을 수 없습니다.")
            return
        
        for item in news[:5]:  # Display latest 5 news
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**[{item.get('publisher', 'Unknown')}]** {item.get('title', 'No title')}")
                st.caption(f"📅 {item.get('providerPublishTime', 'Unknown time')}")
            with col2:
                if item.get('link'):
                    st.markdown(f"[🔗 링크]({item['link']})")
    except Exception as e:
        st.warning(f"뉴스를 불러올 수 없습니다: {str(e)}")

# Main application
st.sidebar.header("⚙️ 설정")

ticker_input = st.sidebar.text_input(
    "종목 코드를 입력하세요",
    value="AAPL",
    help="예: AAPL, 005930.KS, SPY"
).upper()

period = st.sidebar.selectbox(
    "분석 기간 선택",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

if st.sidebar.button("분석 실행", use_container_width=True):
    if not ticker_input:
        st.error("종목 코드를 입력해주세요.")
    else:
        with st.spinner(f"📊 {ticker_input} 데이터를 불러오는 중..."):
            df, ticker = fetch_stock_data(ticker_input, period=period)
            
            if df is None or ticker is None:
                st.error(f"❌ '{ticker_input}'에 대한 데이터를 찾을 수 없습니다. 종목 코드를 확인해주세요.")
            else:
                # Calculate indicators
                df = calculate_indicators(df)
                
                if df is None:
                    st.error("지표 계산 중 오류가 발생했습니다.")
                else:
                    # Display results
                    st.success(f"✅ {ticker_input} 분석 완료!")
                    
                    st.subheader(f"{ticker_input} 상세 분석")
                    
                    # Display metrics
                    display_metrics(df)
                    
                    st.divider()
                    
                    # Display chart
                    display_chart(df, ticker_input)
                    
                    st.divider()
                    
                    # Display data table
                    display_data_table(df)
                    
                    st.divider()
                    
                    # Display news
                    display_news(ticker)

# Footer
st.divider()
st.caption("📌 면책조항: 이 대시보드는 교육 목적으로만 사용되며, 투자 조언이 아닙니다.")
st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
