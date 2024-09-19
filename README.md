# MarketMind

MarketMind is a single-page web application designed to provide interactive stock market insights and predictions using Long Short-Term Memory (LSTM) models and real-time data visualizations. The app leverages Python's Dash framework to create dynamic web interfaces, enabling users to explore stock information, visualize trends, and forecast stock prices.

## Features

- **Interactive Stock Visualizations**: Displays real-time stock prices and indicators, such as moving averages and closing prices, based on user inputs.
- **LSTM-based Stock Prediction**: Predicts stock prices using an LSTM machine learning model, achieving 92.84% prediction accuracy.
- **Dynamic Date Selection**: Users can select a date range to view stock history, supported by interactive graphs and indicators.
- **Company Information**: Fetches and displays company details and logos based on the selected stock ticker.

## Tech Stack

- **Front-end**: Dash, Plotly, TailwindCSS for styling
- **Back-end**: Flask for server-side management
- **Machine Learning**: LSTM model built with Keras and TensorFlow for time-series prediction
- **Data Source**: Yahoo Finance (via `yfinance` library) for real-time stock data

## Installation

To run MarketMind locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/marketmind.git
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the app**:
   Open your browser and go to `http://127.0.0.1:8050/`.

## File Structure

```
/marketmind
|-- /assets
|   |-- styles.css               # Custom CSS for styling
|-- /models
|   |-- model.h5                 # Pre-trained LSTM model
|-- app.py                       # Main application file
|-- requirements.txt             # Python dependencies
```

## Usage

1. **Enter Stock Code**: Input a stock ticker symbol (e.g., AAPL, MSFT).
2. **View Stock Information**: The app fetches the company details and displays stock plots.
3. **Select Date Range**: Choose start and end dates to view stock data within a specific time period.
4. **Predict Stock Prices**: Click on the "Forecast" button to get the predicted stock price for the next day.

## Example

```bash
Stock Code: AAPL
Start Date: 2022-01-01
End Date: 2023-01-01
```

Output: Real-time stock prices along with predicted stock price for the next trading day.

## Screenshots

_Add screenshots of the app interface here._

## License

This project is licensed under the MIT License.

---

Happy predicting!
