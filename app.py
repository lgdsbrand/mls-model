import pandas as pd
import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="⚽ MLS BTTS Model", layout="centered")

# Google Sheet Info
SHEET_ID = "16OxnlyJjmeUc28bpOU2Q733hWDuBXfatYy5f6_o7W3Y"
BASE_URL = "https://docs.google.com/spreadsheets/d/{16OxnlyJjmeUc28bpOU2Q733hWDuBXfatYy5f6_o7W3Y}/gviz/tq?tqx=out:csv&sheet=bttsmodel"

# Dropdown Markets and Corresponding Sheet Tabs
MARKETS = {
    "BTTS": "bttsmodel",
    "Over 1.5": "o1.5model",
    "Over 2.5": "o2.5model"
}

# -----------------------------
# HEADER
# -----------------------------
st.title("⚽ MLS Model (BTTS / O1.5 / O2.5)")

# Dropdown to select market
market_choice = st.selectbox("Select Market", list(MARKETS.keys()))
sheet_name = MARKETS[market_choice]
csv_url = BASE_URL.format(SHEET_ID, sheet_name)

# -----------------------------
# LOAD DATA FROM GOOGLE SHEETS
# -----------------------------
try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

if df.empty:
    st.warning("No games found for this market.")
    st.stop()

# Clean up column names to match Google Sheet
df.columns = [col.strip() for col in df.columns]

# -----------------------------
# DISPLAY STACKED CARDS
# -----------------------------
for _, row in df.iterrows():
    with st.container():
        # Card Header: Game Time
        st.markdown(f"### ⏰ {row['Time']}")
        st.markdown("---")

        # Home Team Row
        st.markdown(
            f"**{row['Home Team']}** | "
            f"MP: {row['MP']} | "
            f"{market_choice}: {row.get(market_choice, '')} | "
            f"Hit Rate: {row['%']} | "
            f"Model: {row['% Prediction']} | "
            f"Odds: {row['Book Odds']} | "
            f"Edge: {row['Edge +/-']}"
        )

        # Away Team Row
        st.markdown(
            f"**{row['Away Team']}** | "
            f"MP: {row['MP']} | "
            f"{market_choice}: {row.get(market_choice, '')} | "
            f"Hit Rate: {row['%']} | "
            f"Model: {row['% Prediction']} | "
            f"Odds: {row['Book Odds']} | "
            f"Edge: {row['Edge +/-']}"
        )

        # Divider Between Games
        st.markdown("---")
