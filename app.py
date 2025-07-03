
import streamlit as st
import pandas as pd
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="RTR Results & Parkrun Tool", layout="centered")
st.title("RunTogether Radcliffe – Race Results & Parkrun Post Generator")

tab1, tab2 = st.tabs(["📋 Manual Race Results", "🏃‍♂️ Parkrun Club Results"])

# -------------------- TAB 1: Manual Entry --------------------
with tab1:
    st.subheader("📋 Enter Race Result Details")

    with st.form("race_form"):
        race_name = st.text_input("Race Name")
        race_date = st.date_input("Race Date", value=datetime.today())
        runner_names = st.text_area("Runner Name(s) (one per line)")
        distance = st.text_input("Distance (e.g. 10k, Half Marathon)")
        results = st.text_area("Times or Notes (one per runner)")
        submit = st.form_submit_button("Generate Post")

    if submit:
        names = [name.strip() for name in runner_names.strip().split("\n") if name.strip()]
        notes = [r.strip() for r in results.strip().split("\n")]

        entries = []
        for i, name in enumerate(names):
            if i < len(notes):
                entries.append(f"{name} ({notes[i]})")
            else:
                entries.append(name)

        joined_names = ", ".join(entries)
        date_str = race_date.strftime("%d %B %Y")

        fb_post = f"""🎉 Race Results – {race_name} ({date_str})

Congratulations to {joined_names} for representing RunTogether Radcliffe at the {race_name} on {date_str}!

🏁 Distance: {distance}

Great running everyone! 💪"""

        wa_post = f"""RTR Results – {race_name} 🏃‍♂️

{joined_names}
📅 {date_str}
📏 {distance}

Well done team! 🎉"""

        st.markdown("---")
        st.subheader("📱 Facebook / Instagram Post")
        st.text_area("Facebook/Instagram", value=fb_post, height=200)

        st.subheader("💬 WhatsApp Message")
        st.text_area("WhatsApp", value=wa_post, height=150)


# -------------------- TAB 2: Parkrun Pull --------------------
with tab2:
    st.subheader("🏃‍♂️ Auto-Fetch Parkrun Results")

    CLUB_URL = "https://www.parkrun.org.uk/groups/49581/"

    def fetch_parkrun_results(club_url):
        response = requests.get(club_url)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if not table:
            return []

        rows = table.find_all("tr")[1:]  # skip header
        data = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                name = cols[0].text.strip()
                event = cols[1].text.strip()
                time = cols[2].text.strip()
                position = cols[3].text.strip()
                age_grade = cols[4].text.strip()
                data.append({
                    "name": name,
                    "event": event,
                    "time": time,
                    "position": position,
                    "age_grade": age_grade
                })
        return data

    if st.button("🔄 Fetch Latest Parkrun Results"):
        results = fetch_parkrun_results(CLUB_URL)

        if results:
            messages = []
            for r in results:
                messages.append(f"{r['name']} – {r['event']} – {r['time']} ({r['position']} place)")

            parkrun_post = f"""🎉 Weekend Parkrun Results

This weekend, RTR runners were out at parkrun:

{chr(10).join(messages)}

👏 Great work everyone!"""
        else:
            parkrun_post = "No results could be fetched or no results available."

        st.text_area("Generated Parkrun Post:", value=parkrun_post, height=300)
