import streamlit as st
import whisper
import requests
import tempfile
import pyttsx3

st.set_page_config(page_title="SalesBoost Semantic Analysis")

st.title("🎧 SalesBoost Semantic Analysis")

# ==========================
# 1. Question (Voice + Text)
# ==========================
question_text = "hey i need to change my event date , there is some change in last time"

st.subheader("Question:")
st.write(question_text)

# Speak question (TTS)
if st.button("🔊 Play Question"):
    engine = pyttsx3.init()
    engine.say(question_text)
    engine.runAndWait()

# ==========================
# 2. Record Learner Answer
# ==========================
st.subheader("🎤 Record Your Answer")

audio_file = st.audio_input("Speak your answer")

learner_answer = None

if audio_file is not None:
    st.success("✅ Audio recorded")

    # Save audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        temp_audio_path = tmp_file.name

    st.info("⏳ Transcribing your answer...")

    model = whisper.load_model("base")
    result = model.transcribe(temp_audio_path)

    learner_answer = result["text"]

    st.subheader("📝 Learner Answer (Transcribed)")
    st.write(learner_answer)

# ==========================
# UI FUNCTION FOR RESULTS
# ==========================
def score_card(title, score, detected=None, feedback="", improvement=""):
    st.markdown(f"### {title}")
    
    col1, col2 = st.columns([1, 3])

    with col1:
        st.metric("Score", f"{score}/100")
        st.progress(score / 100)

    with col2:
        if detected:
            if isinstance(detected, list):
                detected = ", ".join(detected)
            st.markdown(f"**Detected:** {detected}")
        st.markdown(f"**Feedback:** {feedback}")
        st.markdown(f"**Improvement:** {improvement}")

    st.divider()

# ==========================
# 3. Call Backend API
# ==========================
if learner_answer and st.button("🚀 Analyze Answer"):
    st.info("📡 Sending data to backend API...")

    api_url = "http://127.0.0.1:8000/evaluate"

    payload = {
        "learner_answer": learner_answer
    }

    try:
        response = requests.post(api_url, json=payload)
        data = response.json()

        st.subheader("📊 SalesBoost Semantic Analysis Report")

        # Tone
        score_card(
            "🎯 Tone",
            data["tone"]["score"],
            data["tone"].get("detected"),
            data["tone"]["feedback"],
            data["tone"]["improvement"]
        )

        # Articulation
        score_card(
            "🗣️ Articulation",
            data["articulation"]["score"],
            None,
            data["articulation"]["feedback"],
            data["articulation"]["improvement"]
        )

        # Emotion
        score_card(
            "❤️ Emotion",
            data["emotion"]["score"],
            data["emotion"].get("detected"),
            data["emotion"]["feedback"],
            data["emotion"]["improvement"]
        )

        # Pace
        score_card(
            "⏱️ Pace",
            data["pace"]["score"],
            None,
            data["pace"]["feedback"],
            data["pace"]["improvement"]
        )

        # Accuracy
        score_card(
            "🎯 Accuracy",
            data["accuracy"]["score"],
            None,
            data["accuracy"]["feedback"],
            data["accuracy"]["improvement"]
        )

        # Overall Section
        st.subheader("🌟 Overall Feedback")
        st.success(data["overall"]["feedback"])

        st.subheader("💡 Coaching Suggestions")
        for i, suggestion in enumerate(data["overall"]["coachingSuggestions"], 1):
            st.markdown(f"**{i}.** {suggestion}")

    except Exception as e:
        st.error(f"❌ API Error: {e}")
