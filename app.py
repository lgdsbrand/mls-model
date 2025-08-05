import streamlit as st
import pandas as pd

st.set_page_config(page_title="⚽ Soccer Model", layout="wide")

SHEET_ID = "16OxnlyJjmeUc28bpOU2Q733hWDuBXfatYy5f6_o7W3Y"
TABS = {
    "BTTS Model": "bttsmodel",
    "Over 1.5 Model": "o1.5model",
    "Over 2.5 Model": "o2.5model"
}

st.title("⚽ Soccer Both Teams To Score & Overs Model")
st.write("Source: Google Sheets (auto-updated)")

model_choice = st.selectbox("Choose Model", list(TABS.keys()))
selected_tab = TABS[model_choice]

# Build correct CSV URL dynamically
sheet_url = f"https://docs.google.com/spreadsheets/d/{16OxnlyJjmeUc28bpOU2Q733hWDuBXfatYy5f6_o7W3Y}/gviz/tq?tqx=out:csv&sheet=bttsmodel"

try:
    df = pd.read_csv(sheet_url)
except Exception as e:
    st.error(f"Failed to load table: {e}")
    st.stop()

if df.empty:
    st.error("No data found in the selected Google Sheet tab.")
    st.stop()

st.subheader(f"{model_choice} - Upcoming Matches")

for _, row in df.iterrows():
    with st.container():
        st.markdown("---")
        st.markdown(f"**⏰ {row['Time']}**")
        st.markdown(f"""
        **{row['Home Team']}**  
        **{row['Away Team']}**
        """)

        st.table(pd.DataFrame({
            "MP": [row["MP"]],
            "%": [row["%"]],
            "% Prediction": [row["% Prediction"]],
            "Book Odds": [row.get("Book Odds", "")],
            "Edge +/-": [row.get("Edge +/-", "")]
        }))
