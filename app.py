import streamlit as st
import pandas as pd

st.set_page_config(page_title="LineupWire MLS Model", layout="wide")

# -------------------------------
# Header
# -------------------------------
st.title("⚽ LineupWire MLS Model")
st.write("Your smarter soccer betting starts here.")

# -------------------------------
# Today's Matches (Placeholder)
# -------------------------------
matches = pd.DataFrame({
    "Matchup": ["LAFC vs Inter Miami", "Seattle Sounders vs Atlanta United", "NYCFC vs LA Galaxy"],
    "BTTS %": [72, 65, 54],
    "Over 1.5 %": [88, 79, 70],
    "Over 2.5 %": [66, 59, 41],
    "Tip": ["BTTS ✅", "Over 1.5 ✅", "No Bet"]
})

st.subheader("Today's MLS Predictions (Demo)")
st.dataframe(matches.style.format({
    "BTTS %": "{:.0f}%",
    "Over 1.5 %": "{:.0f}%",
    "Over 2.5 %": "{:.0f}%"
}), use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("This is a demo layout. Future version will scrape Windrawwin for daily MLS stats & expert tips.")
