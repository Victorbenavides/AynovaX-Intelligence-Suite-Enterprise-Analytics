import pandas as pd
import numpy as np
from utils.constants import COL_MAPPING

class DataPreprocessor:
    """
    Responsible for cleaning, transforming, and preparing the raw data for analysis.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def preprocess(self) -> pd.DataFrame:
        """
        Executes the full preprocessing pipeline.
        
        Steps:
        1. Remove null CustomerIDs (Crucial for RFM).
        2. Remove duplicates.
        3. Handle cancellations (Quantity < 0).
        4. Calculate TotalPrice.
        5. Type conversion.

        Returns:
            pd.DataFrame: Cleaned and enriched dataset.
        """
        if self.df is None or self.df.empty:
            return pd.DataFrame()

        # 1. Create a copy to avoid SettingWithCopyWarning
        df_clean = self.df.copy()

        # 2. Handling Missing Values
        # For RFM, we cannot use transactions without a CustomerID
        df_clean.dropna(subset=[COL_MAPPING['customer_id']], inplace=True)

        # 3. Data Types Conversion
        # Ensure CustomerID is treated as a string/category, not a number
        df_clean[COL_MAPPING['customer_id']] = df_clean[COL_MAPPING['customer_id']].astype(str)
        
        # Ensure Date is datetime
        df_clean[COL_MAPPING['invoice_date']] = pd.to_datetime(df_clean[COL_MAPPING['invoice_date']])

        # 4. Filter Cancellations and Bad Data
        # We are interested in sales, so we filter out negative quantities
        df_clean = df_clean[df_clean[COL_MAPPING['quantity']] > 0]
        df_clean = df_clean[df_clean[COL_MAPPING['price']] > 0]

        # 5. Feature Engineering
        # Calculate Total Amount per line item
        df_clean['TotalAmount'] = df_clean[COL_MAPPING['quantity']] * df_clean[COL_MAPPING['price']]

        return df_clean