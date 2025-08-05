import streamlit as st
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(layout="wide", page_title="MLS Soccer Models")

# Define dropdown menu
model_choice = st.selectbox(
    "Select Soccer Model",
    ["BTTS", "Over 1.5", "Over 2.5"]
)

# Map dropdown selection to Google Sheet tab
sheet_map = {
    "BTTS": "bttsmodel",
    "Over 1.5": "o1_5model",
    "Over 2.5": "o2_5model"
}

selected_sheet = sheet_map[model_choice]

# -----------------------------
# LOAD DATA FROM GOOGLE SHEETS
# -----------------------------
sheet_id = "16OxnlyJjmeUc28bpOU2Q733hWDuBXfatYy5f6_o7W3Y"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={selected_sheet}"

try:
    df = pd.read_csv(url)
except Exception as e:
    st.error(f"Failed to load Google Sheet data. Error: {e}")
    st.stop()

# Clean data
df.dropna(how='all', inplace=True)

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
        st.markdown(f"#### 🕒 {row['Time']}  —  {row['Home Team']} vs {row['Away Team']}")
        
        # Card content
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.markdown(f"**Prediction %:** {round(row['Prediction %'],1)}%")
            st.markdown(f"**Matches Played:** {row['MP']}")
        
        with col2:
            st.markdown(f"**Book Odds:** {row['Book Odds']}")
        
        with col3:
            st.markdown(f"**Edge:** {round(row['Edge'],2)}")

st.markdown("---")
st.caption("LineupWire MLS Models | Auto-updated daily via Google Sheets")
