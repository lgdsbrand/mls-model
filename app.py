import streamlit as st
import pandas as pd
from requests_html import HTMLSession
from datetime import datetime

st.set_page_config(page_title="MLS BTTS Model", layout="wide")

st.title("⚽ MLS Both Teams To Score (BTTS) Model")
st.markdown("Source: [Windrawwin BTTS Stats](https://www.windrawwin.com/us/soccer-stats/both-teams-to-score/usa-major-league-soccer/)")

# -----------------------------
# Dropdown menu
# -----------------------------
bet_type = st.selectbox("Select Market", ["BTTS", "Over 1.5", "Over 2.5"])

session = HTMLSession()

# -----------------------------
# SCRAPER FUNCTIONS
# -----------------------------
def scrape_btts_table():
    url = "https://www.windrawwin.com/us/soccer-stats/both-teams-to-score/usa-major-league-soccer/"
    r = session.get(url)
    r.html.render(timeout=30, sleep=2)
    
    table = r.html.find("table", first=True)
    if not table:
        return pd.DataFrame()
    
    rows = []
    links = []
    for row in table.find("tr")[1:]:
        cols = row.find("td")
        if len(cols) >= 4:
            team_name = cols[0].text.strip()
            team_link = cols[0].find("a", first=True)
            link_url = "https://www.windrawwin.com" + team_link.attrs['href'] if team_link else None
            
            rows.append([
                team_name,
                cols[1].text.strip(),
                cols[2].text.strip(),
                cols[3].text.strip()
            ])
            links.append(link_url)
    
    df = pd.DataFrame(rows, columns=["Team", "Pld", "BTTS", "Hit Rate"])
    df["Link"] = links
    df["Pld"] = pd.to_numeric(df["Pld"], errors="coerce")
    df["BTTS"] = pd.to_numeric(df["BTTS"], errors="coerce")
    df["Hit Rate"] = df["Hit Rate"].str.replace("%","").astype(float)/100
    return df

def scrape_team_form(url):
    """Scrape last 5 match results (W/D/L) from team page."""
    if not url:
        return [""]*5
    try:
        r = session.get(url)
        r.html.render(timeout=30, sleep=1)
        # Windrawwin marks last 5 matches with small colored squares (L=red, W=green, D=orange/white)
        results = []
        for res in r.html.find(".form .formwl"):  # adapt selector if needed
            if "W" in res.text: results.append("W")
            elif "D" in res.text: results.append("D")
            else: results.append("L")
        return results[:5]
    except:
        return [""]*5

def color_result(res):
    colors = {"W":"green", "L":"red", "D":"white", "":"gray"}
    return f"<div style='background:{colors[res]};color:black;width:20px;text-align:center;border:1px solid black;display:inline-block'>{res}</div>"

# -----------------------------
# BUILD PAGE
# -----------------------------
df = scrape_btts_table()

if df.empty:
    st.error("Failed to load BTTS table: No tables found")
else:
    for i in range(0, len(df), 2):  # pairing teams
        if i+1 >= len(df):
            break
        
        team1, team2 = df.iloc[i], df.iloc[i+1]
        form1 = scrape_team_form(team1["Link"])
        form2 = scrape_team_form(team2["Link"])

        game_time = datetime.now().strftime("%I:%M %p")
        model_pred = round((team1["Hit Rate"] + team2["Hit Rate"]) / 2 * 100, 1)
        odds = 1.8  # placeholder
        edge = round(model_pred/100 * odds - 1, 2)

        with st.container():
            st.markdown(f"### 🕒 {game_time}")

            # Team 1 Row
            col_team, col_stats = st.columns([1.5,6])
            with col_team:
                st.write(team1["Team"])
                form_html = "".join([color_result(r) for r in form1])
                st.markdown(form_html, unsafe_allow_html=True)
            with col_stats:
                st.write(f"Pld: {team1['Pld']} | {bet_type}: {team1['BTTS']} | Hit Rate: {team1['Hit Rate']:.0%} | "
                         f"Model: {model_pred:.1f}% | Odds: {odds} | Edge: {edge}")

            # Team 2 Row
            col_team, col_stats = st.columns([1.5,6])
            with col_team:
                st.write(team2["Team"])
                form_html = "".join([color_result(r) for r in form2])
                st.markdown(form_html, unsafe_allow_html=True)
            with col_stats:
                st.write(f"Pld: {team2['Pld']} | {bet_type}: {team2['BTTS']} | Hit Rate: {team2['Hit Rate']:.0%} | "
                         f"Model: {model_pred:.1f}% | Odds: {odds} | Edge: {edge}")
            
            st.markdown("---")

st.markdown("[⬅ Back to Home](https://lineupwire.com)")
