import pandas as pd

def generate_business_recommendations(df_ai: pd.DataFrame) -> dict:
    """
    Generates automated actionable advice based on cluster statistics.
    Returns a dictionary mapping Cluster Name -> Advice String.
    """
    recommendations = {}
    
    # Calculate averages per cluster
    summary = df_ai.groupby('Cluster_Label').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean'
    }).reset_index()
    
    for _, row in summary.iterrows():
        label = row['Cluster_Label']
        r, f, m = row['Recency'], row['Frequency'], row['Monetary']
        
        if "Whales" in label or ("Cluster" in label and m > 5000):
            advice = "👑 **VIP Treatment:** Assign a dedicated account manager. Offer early access to new products. No discounts needed."
        elif "High Value" in label or ("Cluster" in label and m > 1000):
            advice = "🚀 **Upsell Opportunity:** Recommend complementary products based on purchase history. Join loyalty program."
        elif "Developing" in label:
            advice = "🔄 **Nurture:** Send weekly newsletters with 'Best Sellers'. Offer small threshold discounts (e.g., '$5 off over $50')."
        elif "Dormant" in label or "Low" in label:
            advice = "⚠️ **Re-activation:** Send a 'We miss you' email with a time-limited aggressive discount (e.g., 20% off)."
        else:
            advice = "Analyze further."
            
        recommendations[label] = advice
        
    return recommendations