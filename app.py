
import streamlit as st
import pandas as pd
from datetime import datetime
from parkrun import Club

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

# -------------------- TAB 2: Parkrun Club Results --------------------
with tab2:
    st.subheader("🏃‍♂️ Fetch Latest Parkrun Results")

    try:
        club = Club(49581)  # RunTogether Radcliffe ID
        events = club.results()

        if not events:
            st.warning("No Parkrun results found for this club.")
        else:
            selected_date = st.date_input("Select a parkrun date", value=datetime.today())
            selected_str = selected_date.strftime("%Y-%m-%d")
            filtered = [e for e in events if e['Date'] == selected_str]

            if not filtered:
                st.info("No Parkrun events found for the selected date.")
            else:
                post_lines = []
                for r in filtered:
                    name = r['AthleteName']
                    time = r['Time']
                    position = r['Position']
                    note = "PB!" if r.get("PB", False) else ""
                    post_lines.append(f"{name} – {time} ({position} place){' – ' + note if note else ''}")

                parkrun_post = f"""🎉 Parkrun Results – {selected_str}

RTR runners took part in Parkrun this weekend:

{chr(10).join(post_lines)}

👏 Great running everyone!"""

                st.text_area("Generated Parkrun Post:", value=parkrun_post, height=300)

    except Exception as e:
        st.error(f"Error fetching Parkrun data: {e}")
