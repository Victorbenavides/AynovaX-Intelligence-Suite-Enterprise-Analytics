import pandas as pd
import numpy as np
import datetime as dt
from utils.constants import COL_MAPPING

class RFMAnalyzer:
    """
    Performs RFM (Recency, Frequency, Monetary) analysis on customer transaction data.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_rfm_metrics(self) -> pd.DataFrame:
        """
        Aggregates data by CustomerID to calculate R, F, and M values.

        Logic:
        - Recency: Days since last purchase (Reference date = max date + 1)
        - Frequency: Count of unique invoices per customer
        - Monetary: Sum of TotalAmount spent
        """
        # Define reference date as the next day of the last available date in dataset
        last_date = self.df[COL_MAPPING['invoice_date']].max()
        reference_date = last_date + dt.timedelta(days=1)

        # Aggregation
        rfm = self.df.groupby(COL_MAPPING['customer_id']).agg({
            COL_MAPPING['invoice_date']: lambda x: (reference_date - x.max()).days,
            COL_MAPPING['invoice']: 'nunique',
            'TotalAmount': 'sum'
        }).reset_index()

        # Rename columns for clarity
        rfm.rename(columns={
            COL_MAPPING['invoice_date']: 'Recency',
            COL_MAPPING['invoice']: 'Frequency',
            'TotalAmount': 'Monetary'
        }, inplace=True)

        return rfm

    def score_customers(self, rfm_df: pd.DataFrame) -> pd.DataFrame:
        """
        Assigns scores from 1 to 5 based on quartiles.
        
        Scoring Logic:
        - Recency: Lower is better (bought recently). Label range [5, 4, 3, 2, 1]
        - Frequency: Higher is better. Label range [1, 2, 3, 4, 5]
        - Monetary: Higher is better. Label range [1, 2, 3, 4, 5]
        """
        # Create labels
        r_labels = range(5, 0, -1) # 5, 4, 3, 2, 1
        f_labels = range(1, 6)     # 1, 2, 3, 4, 5
        m_labels = range(1, 6)     # 1, 2, 3, 4, 5

        # Assign scores using qcut (Quantile-based discretization)
        rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], q=5, labels=r_labels).astype(int)
        
        # Using 'rank' method first for F and M to handle duplicate edges (many customers with 1 purchase)
        rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), q=5, labels=f_labels).astype(int)
        rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'].rank(method='first'), q=5, labels=m_labels).astype(int)

        # Concatenate scores to create RFM Segment string (e.g., "555" is best)
        rfm_df['RFM_Segment'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)
        
        # Calculate RFM Score (Sum)
        rfm_df['RFM_Score'] = rfm_df[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

        return rfm_df

    def segment_customers(self, rfm_df: pd.DataFrame) -> pd.DataFrame:
        """
        Maps RFM Scores to human-readable segments using Regex logic or Score summation.
        """
        
        def map_segment(row):
            # Logic based on R and F scores mainly
            if row['R_Score'] >= 5 and row['F_Score'] >= 5:
                return 'Champions'
            elif row['R_Score'] >= 3 and row['F_Score'] >= 4:
                return 'Loyal Customers'
            elif row['R_Score'] >= 4 and row['F_Score'] <= 2:
                return 'Potential Loyalists'
            elif row['R_Score'] <= 2 and row['F_Score'] >= 4:
                return 'At Risk'
            elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
                return 'Hibernating'
            else:
                return 'Needs Attention'

        rfm_df['Customer_Segment'] = rfm_df.apply(map_segment, axis=1)
        return rfm_df