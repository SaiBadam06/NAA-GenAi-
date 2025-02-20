import streamlit as st
import speech_recognition as sr
import pyaudio
import wave
import os

# Function to record audio
def record_audio(filename, duration=5):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    st.write("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    st.write("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to convert audio to text
def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Streamlit UI
st.title("Audio to Text Converter")

# Record audio
if st.button("Record Audio"):
    filename = "recorded_audio.wav"
    record_audio(filename)
    st.audio(filename)

    # Automatically convert the recorded audio to text
    text = audio_to_text(filename)
    st.write("Converted Text:")
    st.write(text)

# Upload audio file
uploaded_file = st.file_uploader("Or upload an audio file", type=["wav"])
if uploaded_file is not None:
    filename = "uploaded_audio.wav"
    with open(filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.audio(filename)

    # Automatically convert the uploaded audio to text
    text = audio_to_text(filename)
    st.write("Converted Text:")
    st.write(text)
