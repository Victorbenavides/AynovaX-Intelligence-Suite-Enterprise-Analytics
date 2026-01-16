import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from utils.constants import COL_MAPPING

class TimeSeriesForecaster:
    """
    Handles Time Series Analysis and Forecasting.
    Uses Holt-Winters Exponential Smoothing for robust retail sales prediction.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def prepare_time_series(self) -> pd.DataFrame:
        """
        Aggregates daily sales data for time series modeling.
        """
        ts_data = self.df.copy()
        ts_data['Date'] = ts_data[COL_MAPPING['invoice_date']].dt.date
        daily_sales = ts_data.groupby('Date')['TotalAmount'].sum().reset_index()
        daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])
        daily_sales.set_index('Date', inplace=True)
        
        # Resample to ensure daily continuity (fill missing days with 0)
        daily_sales = daily_sales.resample('D').sum()
        return daily_sales

    def forecast_sales(self, days_ahead=30):
        """
        Predicts future sales using Exponential Smoothing.
        Returns historical data + forecast dataframe.
        """
        daily_sales = self.prepare_time_series()
        
        # Train Model (Holt-Winters with Trend and Seasonality)
        # Assuming weekly seasonality (period=7)
        model = ExponentialSmoothing(
            daily_sales['TotalAmount'], 
            trend='add', 
            seasonal='add', 
            seasonal_periods=7
        ).fit()

        # Predict
        forecast = model.forecast(days_ahead)
        forecast_df = pd.DataFrame({'Date': forecast.index, 'Predicted_Sales': forecast.values})
        forecast_df.set_index('Date', inplace=True)

        return daily_sales, forecast_df

    def plot_forecast(self, history, forecast) -> go.Figure:
        """
        Visualizes actual sales vs predicted sales.
        """
        fig = go.Figure()

        # Historical Data
        fig.add_trace(go.Scatter(
            x=history.index, 
            y=history['TotalAmount'],
            mode='lines',
            name='Historical Sales',
            line=dict(color='#3498db', width=2)
        ))

        # Forecast Data
        fig.add_trace(go.Scatter(
            x=forecast.index, 
            y=forecast['Predicted_Sales'],
            mode='lines+markers',
            name='AI Forecast (Next 30 Days)',
            line=dict(color='#e74c3c', width=2, dash='dot')
        ))

        fig.update_layout(
            title="Sales Trends & AI Prediction",
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            hovermode="x unified",
            height=500
        )
        return fig