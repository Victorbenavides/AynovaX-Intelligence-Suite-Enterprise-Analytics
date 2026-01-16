import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import streamlit as st

class CustomerSegmenterAI:
    """
    Implements Unsupervised Machine Learning (K-Means) to discover hidden customer segments.
    """

    def __init__(self, rfm_df: pd.DataFrame):
        self.rfm_df = rfm_df

    def train_kmeans_model(self, n_clusters=4) -> pd.DataFrame:
        """
        Trains a K-Means model on RFM data.
        
        Why StandardScaler?
        K-Means is distance-based. 'Monetary' (thousands of $) dwarfs 'Frequency' (units).
        We must scale them to give equal weight to all features.
        """
        # Select features
        features = ['Recency', 'Frequency', 'Monetary']
        X = self.rfm_df[features]

        # 1. Log Transformation (to handle skewness - common in financial data)
        # Using numpy log1p (log(1+x)) to avoid issues with zeros
        import numpy as np
        X_log = np.log1p(X)

        # 2. Scaling
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_log)

        # 3. K-Means Implementation
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        # 4. Assign Clusters back to original DF
        df_ai = self.rfm_df.copy()
        df_ai['Cluster_AI'] = clusters
        
        # Determine which cluster is "Best" based on Monetary mean to label them logically
        # (Cluster 0 isn't always the worst, purely mathematical)
        cluster_avg = df_ai.groupby('Cluster_AI')['Monetary'].mean().sort_values()
        
        # Rename clusters: 0 -> "Bronze", 1 -> "Silver", etc based on value
        cluster_map = {old_label: new_label for new_label, old_label in enumerate(cluster_avg.index)}
        
        # Map to friendly names
        cluster_names = {
            0: 'Low Value / Dormant',
            1: 'Developing',
            2: 'High Value',
            3: 'Top Whales' 
        }
        
        # If user selected different N, we stick to integers or generating dynamic names
        if n_clusters == 4:
             df_ai['Cluster_Label'] = df_ai['Cluster_AI'].map(cluster_map).map(cluster_names)
        else:
             df_ai['Cluster_Label'] = "Cluster " + df_ai['Cluster_AI'].astype(str)

        return df_ai