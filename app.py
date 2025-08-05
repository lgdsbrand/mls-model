import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="MLS BTTS Model", layout="wide")

st.title("⚽ MLS BTTS / Over Goals Model")
st.caption("Automatically updates from Windrawwin.com | LineupWire.com")

# Back to homepage button
st.markdown("[🏠 Back to Homepage](https://lineupwire.com)")

# Dropdown to select market
market_choice = st.selectbox("Select Market", ["BTTS", "Over 1.5", "Over 2.5"])

# -------------------------
# SCRAPING FUNCTION
# -------------------------

def scrape_btts_table():
    url = "https://www.windrawwin.com/us/soccer-stats/both-teams-to-score/usa-major-league-soccer/"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Table parsing
    table = soup.find("table")
    df = pd.read_html(str(table))[0]

    # Clean columns
    df.columns = ["Team", "Pld", "BTTS", "HitRate"]
    df["HitRate"] = df["HitRate"].str.replace("%", "").astype(float)

    return df

# Example: Mock upcoming matches with odds
def get_upcoming_matches():
    data = [
        ["New York City", "Columbus", "Sun 8:00 PM", 75, 76, 1.80],
        ["Chicago", "LAFC", "Sun 9:30 PM", 75, 72, 1.95],
        ["Inter Miami", "Kansas City", "Sun 7:00 PM", 73, 71, 1.88],
    ]
    df = pd.DataFrame(data, columns=[
        "Home Team","Away Team","Time",
        "Home HitRate","Away HitRate","BookOdds"
    ])
    df["ModelPred"] = (df["Home HitRate"]+df["Away HitRate"])/2
    df["Edge"] = (df["ModelPred"]/100) * df["BookOdds"] - 1
    return df

btts_df = scrape_btts_table()
matches_df = get_upcoming_matches()

# -------------------------
# DISPLAY MATCH CARDS
# -------------------------
st.subheader(f"Upcoming MLS Matches ({market_choice})")

for _, row in matches_df.iterrows():
    home = row["Home Team"]
    away = row["Away Team"]
    time = row["Time"]
    home_hit = row["Home HitRate"]
    away_hit = row["Away HitRate"]
    model_pred = row["ModelPred"]
    odds = row["BookOdds"]
    edge = row["Edge"]

    st.markdown(f"### {away} @ {home}  |  ⏰ {time}")

    # Last 5 match form placeholder
    st.write("Form: 🟥🟩⬜  vs  🟩🟥⬜")  # Replace with real scrape later

    cols = st.columns([2,2,2,2,2,2])
    cols[0].metric("Pld (Est)", 25)
    cols[1].metric("BTTS%", f"{(home_hit+away_hit)/2:.0f}%")
    cols[2].metric("Model Pred", f"{model_pred:.1f}%")
    cols[3].metric("Odds", f"{odds:.2f}")
    edge_color = "green" if edge > 0 else "red"
    cols[4].markdown(f"<span style='color:{edge_color}'>{edge*100:.1f}%</span>", unsafe_allow_html=True)

    st.markdown("---")
