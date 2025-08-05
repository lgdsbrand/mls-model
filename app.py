import streamlit as st
import pandas as pd
from requests_html import HTMLSession
from datetime import datetime

st.set_page_config(layout="wide", page_title="MLS BTTS Model")

# -------------------------------
# Scraper function
# -------------------------------
def scrape_btts_table():
    url = "https://www.windrawwin.com/us/soccer-stats/both-teams-to-score/usa-major-league-soccer/"
    session = HTMLSession()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36"
    }
    r = session.get(url, headers=headers)
    r.html.render(timeout=30, sleep=2)

    rows = []

    # 1️⃣ Try table first
    table = r.html.find("table", first=True)
    if table:
        for row in table.find("tr")[1:]:
            cols = row.find("td")
            if len(cols) >= 4:
                team_name = cols[0].text.strip()
                link = cols[0].find("a", first=True)
                link_url = "https://www.windrawwin.com" + link.attrs['href'] if link else None

                rows.append([
                    team_name,
                    cols[1].text.strip(),  # Played
                    cols[2].text.strip(),  # BTTS count
                    cols[3].text.strip(),  # Hit %
                    link_url
                ])
    else:
        # 2️⃣ Backup: div scraping
        team_blocks = r.html.find(".statstable div.row")
        for block in team_blocks:
            cols = block.find("div")
            if len(cols) >= 4:
                team_name = cols[0].text.strip()
                link = cols[0].find("a", first=True)
                link_url = "https://www.windrawwin.com" + link.attrs['href'] if link else None

                rows.append([
                    team_name,
                    cols[1].text.strip(),
                    cols[2].text.strip(),
                    cols[3].text.strip(),
                    link_url
                ])

    # Build DataFrame
    df = pd.DataFrame(rows, columns=["Team", "Pld", "BTTS", "Hit Rate", "Link"])
    if df.empty:
        return pd.DataFrame()

    # Clean types
    df["Pld"] = pd.to_numeric(df["Pld"], errors="coerce")
    df["BTTS"] = pd.to_numeric(df["BTTS"], errors="coerce")
    df["Hit Rate"] = df["Hit Rate"].str.replace("%", "").astype(float) / 100
    return df

# -------------------------------
# UI
# -------------------------------
st.title("⚽ MLS BTTS Model")
st.write(f"Updated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}")

# Back to homepage
st.markdown("[⬅️ Back to Homepage](https://lineupwire.com)")

# Dropdown for filter type
bet_type = st.selectbox("Select Bet Type", ["BTTS", "O1.5", "O2.5"])

# Scrape data
with st.spinner("Scraping Windrawwin for MLS BTTS stats..."):
    df = scrape_btts_table()

if df.empty:
    st.error("No data found. Windrawwin may have blocked scraping or changed layout.")
else:
    # Split into match cards (2 teams per card)
    teams = df["Team"].tolist()

    # Pair teams in order (1 vs 2, 3 vs 4, etc.)
    matchups = [teams[i:i+2] for i in range(0, len(teams), 2)]

    for idx, matchup in enumerate(matchups):
        if len(matchup) < 2:
            continue  # skip incomplete pair

        team1 = df.iloc[idx*2]
        team2 = df.iloc[idx*2+1]

        with st.container():
            st.markdown("---")
            st.markdown(f"### 🕒 Game {idx+1} — {matchup[0]} vs {matchup[1]}")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(team1["Team"])
                st.write(f"Matches: {team1['Pld']}")
                st.write(f"BTTS Hits: {team1['BTTS']}")
                st.write(f"Hit Rate: {team1['Hit Rate']:.0%}")
                st.write("Form (L5): 🟢🟡🔴🟢🔴")  # placeholder

            with col2:
                st.subheader(team2["Team"])
                st.write(f"Matches: {team2['Pld']}")
                st.write(f"BTTS Hits: {team2['BTTS']}")
                st.write(f"Hit Rate: {team2['Hit Rate']:.0%}")
                st.write("Form (L5): 🔴🟡🟢🟢🟡")  # placeholder

    # Raw table at bottom
    st.markdown("---")
    st.subheader("Full MLS BTTS Data")
    st.dataframe(df)
