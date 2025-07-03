
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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


# -------------------- TAB 2: Parkrun Results via BeautifulSoup --------------------
with tab2:
    st.subheader("🏃‍♂️ Fetch Parkrun Club Results from Website")

    selected_date = st.date_input("Select parkrun week (typically Saturday):", value=datetime.today())
    fetch = st.button("🔄 Fetch Parkrun Results")

    if fetch:
        url = "https://www.parkrun.org.uk/groups/49581/"
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.content, "html.parser")

            table = soup.find("table")
            rows = table.find_all("tr")[1:] if table else []

            results = []
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 5:
                    name = cols[0].get_text(strip=True)
                    event = cols[1].get_text(strip=True)
                    time = cols[2].get_text(strip=True)
                    position = cols[3].get_text(strip=True)
                    age_grade = cols[4].get_text(strip=True)
                    results.append(f"{name} – {event} – {time} ({position} place)")

            if results:
                post = f"🎉 Parkrun Results – {selected_date.strftime('%d %B %Y')}

" + "\n".join(results) + "\n\n👏 Great effort RTR team!"
            else:
                post = "No results found on the page."

            st.text_area("Generated Parkrun Post:", value=post, height=300)

        except Exception as e:
            st.error(f"Failed to fetch or parse results: {e}")
