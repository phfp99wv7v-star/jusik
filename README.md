# 🚀 실시간 통합 주식 분석 및 뉴스 대시보드 (jusik)

A comprehensive real-time stock analysis and news dashboard built with Streamlit.

## Features

- 📊 **Real-time Stock Data** - Fetch 1-year historical data for any stock ticker
- 📈 **Technical Analysis** - Calculate key indicators:
  - Simple Moving Averages (50-day, 200-day)
  - RSI (Relative Strength Index)
  - Bollinger Bands
- 📉 **Interactive Charts** - Visualize price trends and indicators
- 📰 **Real-time News** - Display latest 5 news articles related to the stock
- 🌍 **Global Support** - Supports international tickers (e.g., AAPL, 005930.KS, SPY)

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/phfp99wv7v-star/jusik.git
cd jusik
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. Enter a stock ticker code (e.g., AAPL, 005930.KS, SPY)
2. Click "분석 실행" (Run Analysis) button
3. View technical indicators, charts, and related news

## Supported Ticker Formats

- US Stocks: AAPL, GOOGL, MSFT, etc.
- Korean Stocks: 005930.KS (Samsung), 000660.KS (SK Hynix), etc.
- ETFs: SPY, QQQ, VTI, etc.

## Project Structure

```
jusik/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore rules
```

## Technologies Used

- **Streamlit** - Web framework for building dashboards
- **yfinance** - Yahoo Finance API wrapper
- **pandas** - Data manipulation and analysis
- **pandas-ta** - Technical analysis indicators

## Deployment

### Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app" and select your repository
5. Specify `app.py` as the main file

## Future Enhancements

- [ ] Add more technical indicators (MACD, Stochastic, etc.)
- [ ] Implement portfolio tracking
- [ ] Add sentiment analysis for news
- [ ] Cache data to reduce API calls
- [ ] Add user authentication
- [ ] Implement alerts for price movements

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open a GitHub issue.
