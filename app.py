
import streamlit as st
import pandas as pd
import random
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


# -------------------- TAB 2: Parkrun Pull --------------------
with tab2:
    st.subheader("🏃‍♂️ Auto-Fetch Parkrun Results")
    st.info("This tab will eventually auto-pull parkrun results using club ID 49581. Currently a placeholder.")

    st.write("Click below to simulate fetching parkrun data.")

    if st.button("🔄 Fetch Latest Parkrun Results"):
        # Placeholder sample
        fake_parkrun_data = [
            {"name": "Alice", "time": "25:38", "note": "PB!"},
            {"name": "Bob", "time": "28:02", "note": ""},
            {"name": "Charlie", "time": "Volunteer", "note": ""}
        ]

        messages = []
        for r in fake_parkrun_data:
            if "Volunteer" in r["time"]:
                messages.append(f"{r['name']} volunteered 🙌")
            else:
                msg = f"{r['name']} ({r['time']})"
                if r["note"]:
                    msg += f" – {r['note']}"
                messages.append(msg)

        parkrun_post = f"""🎉 Weekend Parkrun Results

This weekend, several RTR members took part in parkrun:

{chr(10).join(messages)}

👏 Great effort everyone – whether you ran or volunteered!"""

        st.text_area("Generated Parkrun Post:", value=parkrun_post, height=220)
