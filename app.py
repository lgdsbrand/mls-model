import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="MLS Both Teams To Score (BTTS) Model",
    layout="wide"
)

# --------------------------
# TITLE
# --------------------------
st.title("⚽ MLS Both Teams To Score (BTTS) Model")
st.write(f"Date: {datetime.now().strftime('%A, %B %d, %Y')}")
st.markdown("Source: [FootyStats BTTS](https://footystats.org/usa/mls/btts)")

# --------------------------
# LOAD DATA FUNCTION
# --------------------------
def load_btts_table():
    url = "https://footystats.org/usa/mls/btts"
    try:
        html_content = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
        tables = pd.read_html(html_content)
        df = tables[0]

        # Clean and rename columns
        df.columns = ["#", "Team", "MP", "BTTS", "BTTS %"]
        df = df.drop("#", axis=1)
        df["BTTS %"] = df["BTTS %"].astype(str)

        return df
    except Exception as e:
        st.error(f"Failed to load BTTS table: {e}")
        return pd.DataFrame(columns=["Team", "MP", "BTTS", "BTTS %"])

# --------------------------
# LOAD DATA
# --------------------------
btts_df = load_btts_table()

if btts_df.empty:
    st.error("❌ Failed to load BTTS table: No data found.")
else:
    # Display full table first
    st.dataframe(btts_df, use_container_width=True)

    # --------------------------
    # CARD STYLE LAYOUT (Simplified)
    # --------------------------
    st.subheader("Matchup Cards (Simple View)")

    # Simulate matchups by pairing teams in order (later will pull MLS fixtures)
    for i in range(0, len(btts_df)-1, 2):
        team1 = btts_df.iloc[i]
        team2 = btts_df.iloc[i+1]

        st.markdown(f"""
        **Game Time:** TBD  
        **{team1['Team']} vs {team2['Team']}**  

        | Team | MP | BTTS | BTTS% | Model Pred | Odds | Edge |
        |------|----|------|-------|-----------|------|------|
        | {team1['Team']} | {team1['MP']} | {team1['BTTS']} | {team1['BTTS %']} | {(int(team1['BTTS %'].replace('%',''))+int(team2['BTTS %'].replace('%','')))//2}% | TBD | TBD |
        | {team2['Team']} | {team2['MP']} | {team2['BTTS']} | {team2['BTTS %']} | {(int(team1['BTTS %'].replace('%',''))+int(team2['BTTS %'].replace('%','')))//2}% | TBD | TBD |
        """)
        st.write("---")

# --------------------------
# BACK TO HOME BUTTON
# --------------------------
st.markdown("[⬅ Back to Home](https://lineupwire.com)")
