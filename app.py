import streamlit as st
from streamlit_mic_recorder import mic_recorder
from utils import load_story_data
from utils.audio_utils import transcribe_audio
from utils.scoring import compute_pronunciation_score, compute_timing_score
import pandas as pd

st.set_page_config(page_title="Freadom AI Speech Evaluator", layout="centered")

story = load_story_data()

if "page_index" not in st.session_state:
    st.session_state.page_index = 0
if "results" not in st.session_state:
    st.session_state.results = {}
if "recorded" not in st.session_state:
    st.session_state.recorded = {}
if "go_next" not in st.session_state:
    st.session_state.go_next = False

if st.session_state.go_next:
    st.session_state.page_index += 1
    st.session_state.go_next = False
    st.rerun()  

idx = st.session_state.page_index
if idx >= len(story):
    st.markdown("---")
    st.header("Your Reading Summary")
    df = pd.DataFrame(st.session_state.results.values())
    df = df.sort_values("Page").reset_index(drop=True)
    st.dataframe(df)
    avg_pron = df["Pronunciation (%)"].mean()
    avg_time = df["Timing (%)"].mean()
    st.metric("Average Pronunciation", f"{avg_pron:.2f}%")
    st.metric("Average Timing", f"{avg_time:.2f}%")
    st.stop()


page = story[idx]
st.image(page["image"], use_container_width=True, width=100)
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    prev_disabled = idx == 0
    if st.button("Prev", disabled=prev_disabled):
        st.session_state.page_index -= 1

with col2:
    if not st.session_state.recorded.get(idx, False):
        left_spacer, center_col, right_spacer = st.columns([1, 2, 1])
        with center_col:
            audio = mic_recorder(start_prompt="Record", stop_prompt="Stop", key=f"rec_{idx}")


        if audio:
            transcript, duration = transcribe_audio(audio["bytes"])
            pron_score = compute_pronunciation_score(transcript, page["expected_transcript"])
            time_score = compute_timing_score(duration, page["expected_duration"])
            st.session_state.results[idx] = {
                "Page": page["page"],
                "Script": page["expected_transcript"],
                "Said": transcript,
                "Pronunciation (%)": pron_score,
                "Timing (%)": time_score
            }
            st.session_state.recorded[idx] = True
            st.session_state.go_next = True  

with col3:
    next_disabled = not st.session_state.recorded.get(idx, False)
    if st.button("Next", disabled=next_disabled):
        st.session_state.page_index += 1
