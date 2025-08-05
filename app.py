import streamlit as st
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(layout="wide", page_title="MLS Soccer Models")

# Google Sheet info
SHEET_ID = "16OxnlyJjmeUc28bpOU2Q733hWDuBXfatYy5f6_o7W3Y"
TAB_MAP = {
    "BTTS": "bttsmodel",
    "Over 1.5": "o1_5model",
    "Over 2.5": "o2_5model"
}

# Dropdown menu
model_choice = st.selectbox(
    "Select Soccer Model",
    list(TAB_MAP.keys())
)
selected_tab = TAB_MAP[model_choice]

# Build CSV export URL for the chosen tab
sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={selected_tab}"

# -----------------------------
# LOAD DATA
# -----------------------------
try:
    df = pd.read_csv(sheet_url)
except Exception as e:
    st.error(f"Failed to load Google Sheet data. Error: {e}")
    st.stop()

df.dropna(how="all", inplace=True)

# -----------------------------
# TITLE & NAV
# -----------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.title(f"MLS ⚽ {model_choice} Model")
with col2:
    st.markdown("[⬅️ Back to Homepage](https://lineupwiremlb.streamlit.app)")

# Show today's date
st.markdown(f"### 📅 Upcoming Matches for: **{pd.Timestamp.now().strftime('%B %d, %Y')}**")
st.markdown("---")

# -----------------------------
# STACKED CARD LAYOUT
# -----------------------------
for idx, row in df.iterrows():
    with st.container():
        st.markdown("---")  # Card separator
        
        # Match header
        st.markdown(f"#### 🕒 {row['Time']} — {row['Home Team']} vs {row['Away Team']}")
        
        # Card content
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.markdown(f"**Prediction %:** {round(row['Prediction %'], 1)}%")
            st.markdown(f"**Matches Played:** {row['MP']}")
        
        with col2:
            st.markdown(f"**Book Odds:** {row['Book Odds']}")
        
        with col3:
            st.markdown(f"**Edge:** {round(row['Edge'], 2)}")

st.markdown("---")
st.caption("LineupWire MLS Models | Auto-updated daily via Google Sheets")
