import streamlit as st
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="⚽ Soccer Model", layout="wide")

# Google Sheet info
SHEET_ID = "16OxnlyJjmeUc28bpOU2Q733hWDuBXfatYy5f6_o7W3Y"
TABS = {
    "BTTS Model": "bttsmodel",
    "Over 1.5 Model": "o1.5model",
    "Over 2.5 Model": "o2.5model"
}

# -----------------------------
# HEADER
# -----------------------------
st.title("⚽ Soccer Both Teams To Score & Overs Model")
st.write("Source: Google Sheets (auto-updated via Apps Script)")

# Dropdown for model selection
model_choice = st.selectbox("Choose Model", list(TABS.keys()))
selected_tab = TABS[model_choice]

# Google Sheet CSV URL
sheet_url = f"https://docs.google.com/spreadsheets/d/{16OxnlyJjmeUc28bpOU2Q733hWDuBXfatYy5f6_o7W3Y}/gviz/tq?tqx=out:csv&sheet=bttsmodel"

# -----------------------------
# LOAD DATA
# -----------------------------
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
    with st.container():
        st.markdown("---")  # divider line

        # Game time
        st.markdown(f"**⏰ {row['Time']}**")

        # Teams stacked vertically
        st.markdown(f"""
        **{row['Home Team']}**  
        **{row['Away Team']}**
        """)

        # Stats table for card view
        card_data = pd.DataFrame({
            "Overall%": [row["Overall%"]],
            "Home%": [row["Home%"]],
            "Away%": [row["Away%"]],
            "% Prediction": [row["% Prediction"]],
            "Book Odds": [row.get("Book Odds", "")],
            "Edge +/-": [row.get("Edge +/-", "")]
        })

        st.dataframe(card_data, use_container_width=True)

st.markdown("---")
st.markdown("Return to [Home Page](https://lineupwire.com)")
