import streamlit as st
import pandas as pd
import requests

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="⚽ Soccer Model", layout="wide")

# Your Google Sheet ID
SHEET_ID = "16OxnlyJjmeUc28bpOU2Q733hWDuBXfatYy5f6_o7W3Y"

# Tabs that exist in your Google Sheet
TABS = {
    "BTTS Model": "bttsmodel",
    "Over 1.5 Model": "o1.5model",
    "Over 2.5 Model": "o2.5model"
}

# -----------------------------
# HEADER
# -----------------------------
st.title("⚽ Soccer Both Teams To Score & Overs Model")
st.write("Source: Google Sheets (auto-updated via ImportHTML)")

# Dropdown for model selection
model_choice = st.selectbox("Choose Model", list(TABS.keys()))

# Build URL for the chosen tab
selected_tab = TABS[model_choice]
sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={selected_tab}"

# Load data
try:
    df = pd.read_csv(sheet_url)
except Exception as e:
    st.error(f"Failed to load table: {e}")
    st.stop()

if df.empty:
    st.error("No data found in the selected Google Sheet tab.")
    st.stop()

# -----------------------------
# CARD VIEW
# -----------------------------
st.subheader(f"{model_choice} - Upcoming Matches")

for _, row in df.iterrows():
    # Build each game card
    with st.container():
        st.markdown("---")  # divider
        st.markdown(f"**⏰ {row['Time']}**")
        
        # Teams stacked
        st.markdown(f"""
        **{row['Home Team']}**  
        **{row['Away Team']}**
        """)
        
        # Table of stats
        card_data = pd.DataFrame({
            "MP": [row["MP"]],
            "Stat": [row.get("BTTS", row.get("O1.5", row.get("O2.5", "")))],
            "%": [row["%"]],
            "% Prediction": [row["% Prediction"]],
            "Book Odds": [row["Book Odds"]],
            "Edge +/-": [row["Edge +/-"]]
        })
        st.table(card_data)

st.markdown("---")
st.markdown("[⬅ Back to Homepage](https://lineupwire.com)")
