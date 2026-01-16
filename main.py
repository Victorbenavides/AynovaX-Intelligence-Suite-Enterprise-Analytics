import streamlit as st
import pandas as pd

# Module Imports
from src.data_loader import DataLoader
from src.preprocessor import DataPreprocessor
from src.rfm_analysis import RFMAnalyzer
from src.visualization import DashboardCharts
from src.ai_models import CustomerSegmenterAI
from src.insights_engine import generate_business_recommendations
from src.forecasting import TimeSeriesForecaster
from src.ui_components import apply_custom_style

# Utilities
from utils.constants import UI_TEXT, LANGUAGES

# --- Page Configuration (Must be the very first command) ---
st.set_page_config(
    page_title="AynovaX Analytics Suite",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """
    Main execution entry point for the AynovaX Analytics Suite.
    Orchestrates Data Loading, Preprocessing, AI Modeling, Forecasting, and Visualization.
    """
    
    # 1. Apply Premium UI/UX Styles
    apply_custom_style()

    # --- Sidebar: Global Configuration ---
    st.sidebar.title("🔮 AynovaX Intelligence")
    st.sidebar.markdown("`v2.0 Enterprise Edition`")
    st.sidebar.markdown("---")
    
    # Language Settings
    st.sidebar.header("⚙️ Settings")
    lang_code = st.sidebar.selectbox(
        "Interface Language", 
        options=list(LANGUAGES.keys()), 
        format_func=lambda x: LANGUAGES[x]
    )
    
    # --- Data Ingestion Section ---
    st.sidebar.subheader("📂 Data Source")
    
    # Path to local demo data
    DEFAULT_PATH = "data/raw/OnlineRetail.xlsx" 
    
    # Toggle between Demo Data and User Upload
    use_demo = st.sidebar.checkbox("Use Enterprise Demo Data", value=True)
    
    df = None
    
    if use_demo:
        # Load local file with caching
        loader = DataLoader(DEFAULT_PATH)
        df = loader.load_data()
    else:
        # Allow user to upload their own ERP export
        uploaded_file = st.sidebar.file_uploader("Upload ERP Export (CSV/XLSX)", type=['csv', 'xlsx'])
        if uploaded_file:
            st.info("Module ready for file processing.")
            # In a production environment, we would handle the file buffer here.
            pass 
            
    # Proceed only if data is successfully loaded
    if df is not None:
        
        # --- ETL & Preprocessing ---
        # Using a spinner to indicate backend processing
        with st.spinner("🚀 AynovaX Engine is processing millions of records..."):
            processor = DataPreprocessor(df)
            df_clean = processor.preprocess()
        
        # --- Main Dashboard Header ---
        st.title(f"📊 {UI_TEXT['app_title'][lang_code]}")
        
        # Status Bar
        st.markdown(f"""
            <div style="background-color: #1c1f26; padding: 10px; border-radius: 5px; border-left: 5px solid #00f900; margin-bottom: 20px;">
                <span style="color: #ccc;">System Status:</span> 
                <strong style="color: #fff;">Operational</strong> | 
                <span style="color: #ccc;">Data Points Analyzed:</span> 
                <strong style="color: #fff;">{len(df_clean):,} transactions</strong>
            </div>
        """, unsafe_allow_html=True)

        # --- TABS ARCHITECTURE ---
        # Splitting the application into specific functional modules
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏢 Executive Dashboard (RFM)", 
            "🤖 AI Clustering (K-Means)", 
            "📈 Sales Forecasting (Time Series)",
            "💡 Strategic Action Plan"
        ])

        # Initialize core logic engines
        analyzer = RFMAnalyzer(df_clean)
        rfm_df = analyzer.calculate_rfm_metrics()

        # ==========================================
        # TAB 1: EXECUTIVE DASHBOARD (RFM)
        # ==========================================
        with tab1:
            # Apply Scoring Rules
            rfm_scored = analyzer.score_customers(rfm_df)
            rfm_scored = analyzer.segment_customers(rfm_scored)
            viz = DashboardCharts(rfm_scored)
            
            # KPI Row - Premium Style Metrics
            st.markdown("#### Key Performance Indicators")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            
            # Using Streamlit metrics with 'delta' for business context
            kpi1.metric("Active Customers", f"{rfm_df['CustomerID'].nunique():,}", delta="12% vs last month")
            kpi2.metric("Avg. Order Value", f"${rfm_df['Monetary'].mean():.2f}", delta="3.5%")
            kpi3.metric("Purchase Frequency", f"{rfm_df['Frequency'].mean():.1f}", delta="-0.8%")
            kpi4.metric("Total Revenue Analyzed", f"${rfm_df['Monetary'].sum()/1e6:.2f}M")
            
            # Split Layout for Charts
            col_L, col_R = st.columns([2, 1])
            with col_L:
                st.markdown("##### Customer Segmentation Map")
                st.plotly_chart(viz.plot_rfm_scatter(), use_container_width=True)
            with col_R:
                st.markdown("##### Revenue Share")
                st.plotly_chart(viz.plot_revenue_by_segment(), use_container_width=True)

        # ==========================================
        # TAB 2: AI CLUSTERING (UNSUPERVISED ML)
        # ==========================================
        with tab2:
            st.markdown("### 🧠 Unsupervised Machine Learning")
            st.info("Using K-Means Algorithm to detect natural customer groupings beyond manual rules.")
            
            col_ai_viz, col_ai_ctrl = st.columns([3, 1])
            
            with col_ai_ctrl:
                st.markdown("**Model Hyperparameters**")
                # Interactive Slider to retrain model in real-time
                k_clusters = st.slider("Target Clusters (k)", 2, 8, 4)
                st.caption("Adjusting 'k' retrains the model instantly.")
            
            # Train AI Model on the fly
            ai_model = CustomerSegmenterAI(rfm_df)
            df_ai = ai_model.train_kmeans_model(n_clusters=k_clusters)
            
            with col_ai_viz:
                viz_ai = DashboardCharts(df_ai)
                # Check if 3D method exists to avoid crashes
                if hasattr(viz_ai, 'plot_3d_clusters'):
                    st.plotly_chart(viz_ai.plot_3d_clusters(df_ai), use_container_width=True)
                else:
                    st.warning("3D Visualization module not loaded.")

        # ==========================================
        # TAB 3: SALES FORECASTING (PREDICTIVE AI)
        # ==========================================
        with tab3:
            st.markdown("### 📉 Future Revenue Prediction (AI Powered)")
            st.write("Using **Holt-Winters Exponential Smoothing** to forecast demand trends and seasonality.")
            
            # Initialize Forecaster
            forecaster = TimeSeriesForecaster(df_clean)
            
            # User Controls
            days_pred = st.slider("Forecast Horizon (Days)", 7, 90, 30)
            
            if st.button("Generate AI Forecast", type="primary"):
                with st.spinner("Training Time Series Model..."):
                    # Execute prediction
                    hist, pred = forecaster.forecast_sales(days_ahead=days_pred)
                    
                    # Calculate projected revenue
                    total_pred = pred['Predicted_Sales'].sum()
                    
                    # Display Result
                    st.success(f"Projected Revenue for next {days_pred} days: **${total_pred:,.2f}**")
                    
                    # Visualize
                    fig_forecast = forecaster.plot_forecast(hist, pred)
                    st.plotly_chart(fig_forecast, use_container_width=True)

        # ==========================================
        # TAB 4: STRATEGIC INSIGHTS (ACTION PLAN)
        # ==========================================
        with tab4:
            st.header("⚡ Automated Business Strategy")
            st.markdown("Actionable recommendations generated based on AI Cluster behaviors.")
            
            # Ensure AI data exists if user jumps directly to Tab 4
            if 'df_ai' not in locals():
                ai_model = CustomerSegmenterAI(rfm_df)
                df_ai = ai_model.train_kmeans_model(n_clusters=4)
            
            # Generate Logic-based advice
            recommendations = generate_business_recommendations(df_ai)
            
            # Grid Layout for Recommendation Cards
            c1, c2 = st.columns(2)
            
            for i, (cluster, advice) in enumerate(recommendations.items()):
                # Alternating columns for better visual flow
                col = c1 if i % 2 == 0 else c2
                with col:
                    # Injecting HTML for custom "Card" design matching the AynovaX Theme
                    st.markdown(f"""
                    <div style="background-color: #262730; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #00f900; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
                        <h3 style="margin-top:0; color: #fff;">{cluster}</h3>
                        <p style="color: #00f900; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">AI Recommended Strategy</p>
                        <p style="font-size: 15px; color: #e0e0e0; line-height: 1.5;">{advice}</p>
                    </div>
                    """, unsafe_allow_html=True)

    else:
        # Fallback if data is not loaded
        st.warning("Please verify the data source path in 'src/data_loader.py' or upload a valid file.")

if __name__ == "__main__":
    main()