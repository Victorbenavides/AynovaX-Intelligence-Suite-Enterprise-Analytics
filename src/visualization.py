import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class DashboardCharts:
    """
    Generates interactive Plotly charts for the Streamlit dashboard.
    Includes error handling to prevent app crashes.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _create_empty_figure(self, message: str) -> go.Figure:
        """Helper to return an empty figure with an error message."""
        fig = go.Figure()
        fig.add_annotation(text=message, xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(xaxis={'visible': False}, yaxis={'visible': False})
        return fig

    def plot_segment_distribution(self) -> go.Figure:
        """Bar chart: Customer Count per Segment."""
        try:
            if self.df is None or self.df.empty:
                return self._create_empty_figure("No Data Available")
                
            if 'Customer_Segment' not in self.df.columns:
                return self._create_empty_figure("Column 'Customer_Segment' missing")

            segment_counts = self.df['Customer_Segment'].value_counts().reset_index()
            segment_counts.columns = ['Segment', 'Count']

            fig = px.bar(
                segment_counts, 
                x='Segment', 
                y='Count', 
                title='Customer Distribution by Segment',
                color='Segment',
                text='Count'
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False, height=500)
            return fig
            
        except Exception as e:
            return self._create_empty_figure(f"Chart Error: {str(e)}")

    def plot_rfm_scatter(self) -> go.Figure:
        """Scatter plot: Recency vs Frequency."""
        try:
            if self.df is None or self.df.empty:
                return self._create_empty_figure("No Data Available")

            fig = px.scatter(
                self.df,
                x='Recency',
                y='Frequency',
                color='Customer_Segment',
                size='Monetary',
                hover_data=['Customer_Segment', 'Monetary'],
                log_y=True,
                title='Recency vs Frequency (Size = Monetary Value)',
                labels={'Recency': 'Days Since Last Purchase', 'Frequency': 'Total Transactions'}
            )
            fig.update_layout(height=600)
            return fig
            
        except Exception as e:
            return self._create_empty_figure(f"Chart Error: {str(e)}")

    def plot_revenue_by_segment(self) -> go.Figure:
        """Pie chart: Revenue Share."""
        try:
            # Check for required columns
            if self.df is None or self.df.empty:
                return self._create_empty_figure("No Data Available")

            if 'Customer_Segment' not in self.df.columns or 'Monetary' not in self.df.columns:
                 return self._create_empty_figure("Missing Columns for Revenue Chart")

            segment_rev = self.df.groupby('Customer_Segment')['Monetary'].sum().reset_index()
            
            fig = px.pie(
                segment_rev, 
                values='Monetary', 
                names='Customer_Segment', 
                title='Share of Total Revenue by Segment',
                hole=0.4
            )
            fig.update_traces(textinfo='percent+label')
            return fig
            
        except Exception as e:
            # Fallback in case of unexpected errors (e.g., all zeros)
            return self._create_empty_figure(f"Could not render Revenue Chart: {str(e)}")

    def plot_3d_clusters(self, df_ai: pd.DataFrame) -> go.Figure:
        """3D Scatter Plot for AI Clusters."""
        try:
            if df_ai is None or df_ai.empty:
                return self._create_empty_figure("No AI Data Available")

            fig = px.scatter_3d(
                df_ai,
                x='Recency',
                y='Frequency',
                z='Monetary',
                color='Cluster_Label',
                opacity=0.7,
                size_max=20,
                hover_data=['Recency', 'Frequency', 'Monetary'],
                title='3D AI-Driven Customer Clusters',
                labels={'Cluster_Label': 'Customer Group'}
            )
            fig.update_layout(
                margin=dict(l=0, r=0, b=0, t=30),
                scene=dict(
                    xaxis_title='Recency',
                    yaxis_title='Frequency',
                    zaxis_title='Monetary'
                ),
                height=700
            )
            return fig
            
        except Exception as e:
            return self._create_empty_figure(f"3D Chart Error: {str(e)}")