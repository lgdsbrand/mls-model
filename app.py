import pandas as pd
import streamlit as st

st.set_page_config(page_title="MLS BTTS / Totals Model", layout="wide")
st.title("⚽ MLS BTTS / Totals Model")

# --- Google Sheet CSV link ---
sheet_url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(sheet_url)
except Exception as e:
    st.error(f"Failed to load MLS data: {e}")
    st.stop()

# Ensure numeric columns are clean
for col in ["Home BTTS %", "Away BTTS %"]:
    df[col] = df[col].astype(str).str.rstrip('%').astype(float)

# Compute prediction and edge
df["BTTS Prediction %"] = (df["Home BTTS %"] + df["Away BTTS %"]) / 2

# Calculate edge if Book Odds exist (implied probability vs prediction)
# Convert American odds to implied probability
def odds_to_prob(odds):
    try:
        odds = float(odds)
    except:
        return None
    if odds > 0:  # Positive odds
        return 100 / (odds + 100) * 100
    else:         # Negative odds
        return abs(odds) / (abs(odds) + 100) * 100

if "Book Odds" in df.columns:
    df["Book Prob %"] = df["Book Odds"].apply(odds_to_prob)
    df["Edge %"] = df["BTTS Prediction %"] - df["Book Prob %"]
else:
    df["Book Prob %"] = None
    df["Edge %"] = None

# --- Dropdown to filter ---
st.subheader("Filter Market")
market = st.selectbox("Choose Market", ["BTTS", "O1.5", "O2.5"], index=0)

# Filter df if needed
if market != "BTTS" and market in df.columns:
    df_filtered = df[df[market] == 1]
else:
    df_filtered = df.copy()

# --- Display Game Cards ---
for idx, row in df_filtered.iterrows():
    with st.container():
        st.markdown("---")
        st.markdown(f"### 🕒 {row['Time (EST)']} — {row['Away Team']} @ {row['Home Team']}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**🏠 {row['Home Team']}**")
            st.markdown(f"BTTS: {row['Home BTTS %']:.0f}%")
            st.markdown(f"Last 5: {row['Last 5 Home']}")
        with col2:
            st.markdown(f"**✈️ {row['Away Team']}**")
            st.markdown(f"BTTS: {row['Away BTTS %']:.0f}%")
            st.markdown(f"Last 5: {row['Last 5 Away']}")

        # Prediction and odds
        st.markdown(f"**Prediction:** {row['BTTS Prediction %']:.1f}%")
        if pd.notna(row['Book Odds']):
            st.markdown(f"**Book Odds:** {row['Book Odds']}")
        if pd.notna(row['Edge %']):
            st.markdown(f"**Edge:** {row['Edge %']:.1f}%")

# Back to Homepage
st.markdown("[⬅ Back to Homepage](https://lineupwire.com)")
