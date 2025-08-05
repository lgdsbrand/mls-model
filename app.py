import pandas as pd
import streamlit as st

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="MLS BTTS Model", layout="wide")

# Google Sheet CSV links (replace YOUR_SHEET_ID)
BASE_URL = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}"
SHEET_ID = "16OxnlyJjmeUc28bpOU2Q733hWDuBXfatYy5f6_o7W3Y"

TABS = {
    "BTTS": "bttsmodel",
    "Over 1.5": "o1.5model",
    "Over 2.5": "o2.5model"
}

# -----------------------------
# SIDEBAR & HEADER
# -----------------------------
st.title("⚽ MLS Both Teams To Score (BTTS) Model")
st.markdown("Data Source: Google Sheets (auto-updating)")

# Dropdown for model selection
selected_tab = st.selectbox("Select Market", list(TABS.keys()))

# -----------------------------
# LOAD DATA
# -----------------------------
csv_url = BASE_URL.format(SHEET_ID, TABS[selected_tab])
try:
    df = pd.read_csv(csv_url)
except:
    st.error("Failed to load model data from Google Sheets. Check sharing permissions.")
    st.stop()

# -----------------------------
# DISPLAY CARDS
# -----------------------------
if df.empty:
    st.warning("No games available for this market today.")
else:
    for _, row in df.iterrows():
        with st.container():
            st.markdown(f"""
            ### {row['Time']}
            **{row['Home Team']}** vs **{row['Away Team']}**
            
            **MP:** {row['MP']} | **{selected_tab}:** {row[selected_tab]} | **Hit Rate:** {row['%']}
            
            **Model Prediction:** {row['% Prediction']}  
            **Book Odds:** {row['Book Odds']} | **Edge:** {row['Edge +/-']}
            ---
            """)
