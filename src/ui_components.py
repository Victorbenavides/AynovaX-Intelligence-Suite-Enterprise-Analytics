import streamlit as st

def apply_custom_style():
    """
    Injects custom CSS to transform the Streamlit app into a Professional Dashboard.
    """
    st.markdown("""
        <style>
        /* Main Background & Font */
        .stApp {
            background-color: #0e1117;
            font-family: 'Inter', sans-serif;
        }
        
        /* Metric Cards Styling */
        div[data-testid="stMetric"] {
            background-color: #262730;
            border: 1px solid #464b5c;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
            transition: transform 0.2s;
        }
        div[data-testid="stMetric"]:hover {
            transform: scale(1.02);
            border-color: #00f900;
        }
        
        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #1c1f26;
            border-radius: 5px 5px 0 0;
            border: 1px solid #464b5c;
            color: white;
        }
        .stTabs [aria-selected="true"] {
            background-color: #00f900 !important;
            color: black !important;
            font-weight: bold;
        }

        /* Sidebar Polish */
        section[data-testid="stSidebar"] {
            background-color: #1c1f26;
        }
        
        /* Hide default Streamlit Elements for cleaner look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        </style>
    """, unsafe_allow_html=True)