import pandas as pd
import streamlit as st
from main import students, verify_presence

st.title("Smart Presence Tracker")
st.subheader("Manage students presence, based on a simple database, Speech-to-Text technology.",
              anchor="subtitle")


# 1. Initialize DataFrames in session_state
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(students)

if "temp_df" not in st.session_state:
    st.session_state.temp_df = st.session_state.df.copy()
    st.session_state.temp_df["Today"] = ""

# 2. One unified Save function reading from st.session_state.temp_df
def save():
    today_values = st.session_state.temp_df["Today"].tolist()
    for i, val in enumerate(today_values):
        st.session_state.df.at[i, "presence"].append(val)

    st.session_state.df.to_csv("temp_list.csv", index=False)
    st.success("Saved!")

# 3. Manual Mode vs Automatic Mode
if manual := st.toggle("Manual mode"):
    st.session_state.temp_df = st.data_editor(
        st.session_state.temp_df,
        width='stretch',
        disabled=["id", "first_name", "last_name", "gender", "wilaya"],
        column_config={
            "Today": st.column_config.SelectboxColumn(
                "Today",
                options=["Absent", "Present"],
                required=True,
            ),
        },
        hide_index=True,
    )

else:
    @st.fragment()
    def auto_table():
        audio_value = st.audio_input(
        "🎙️ Enregistrez la présence (ex: 'Ahmed présent, Sara absente...')"
         )

        if audio_value is not None:
            if st.button("⚡ Analyser l'audio", key="analyze_audio"):
                with st.spinner("Transcription et remplissage du tableau..."):
                    transcript, statuses = verify_presence(
                        audio_value, st.session_state.temp_df
                    )

                    if transcript:
                        st.info(f"**Texte compris :** {transcript}")
                        st.session_state.temp_df["Today"] = statuses
                        st.rerun()
                    else:
                        st.warning("Aucune voix détectée. Veuillez réessayer.")
                            
                if "last_transcript" in st.session_state:
                    st.info(f"**Texte compris :** {st.session_state.last_transcript}")
                    
                save()
                st.rerun()

        st.dataframe(
            st.session_state.temp_df,
            width='stretch',
            hide_index=True,
            column_config={
                "id": st.column_config.TextColumn("ID"),
                "first_name": st.column_config.TextColumn("First Name"),
                "last_name": st.column_config.TextColumn("Last Name"),
                "gender": st.column_config.TextColumn("Gender"),
                "wilaya": st.column_config.TextColumn("Wilaya"),
                "Today": st.column_config.TextColumn("Today"),
            },
        )

    auto_table()


if st.button("Save", key="global_save"):
    save()
else:
    st.info("You can edit the table and click 'Save' to save the changes.")


# 4. Display smmary metrics
total = len(st.session_state.temp_df)
present = (st.session_state.temp_df["Today"] == "Present").sum()
not_marked = (st.session_state.temp_df["Today"] == "Not Marked").sum()
absent = total - present - not_marked

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Students", total)
col2.metric("✅ Present", present)
col3.metric("❌ Absent", absent)
col4.metric("❓ Not Marked", not_marked)



