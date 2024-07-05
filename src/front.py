import streamlit as st
import os
import sys
from datetime import datetime
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import bot as cb
import subprocess

# version compatibility issue : had to edit Wav2Lip audio.py file --- check _build_mel_basis() function! 

st.set_page_config(
    page_title="Video Chatbot",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("//enter//path//to//your//css//file")

def ensure_temp_dir():
    temp_dir = os.path.join(os.getcwd(), 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir

def save_audio_file(audio_bytes, file_extension):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"
    with open(file_name, "wb") as f:
        f.write(audio_bytes)
    return file_name

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data, language='en-US')
        except sr.UnknownValueError:
            return "I'm sorry, I couldn't catch that. Could you please repeat your question?"
        except sr.RequestError:
            return "I'm sorry, there was an error with the speech recognition service. Please try again."
        
def text_to_speech(text):
    temp_dir = ensure_temp_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = os.path.join(temp_dir, f"output_{timestamp}.mp3")
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)
    return filename

import logging
import traceback

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_lip_sync_video(response, image_file_path):
    audio_file_path = text_to_speech(response)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    wav2lip_path = r"//enter//path//to//your//wav2lip//folder"
    temp_dir = ensure_temp_dir()

    output_video_path = os.path.join(temp_dir, f"output_video_{timestamp}.mp4")

    cmd = [
        sys.executable,
        os.path.join(wav2lip_path, "inference.py"),
        "--checkpoint_path", os.path.join(wav2lip_path, "checkpoints", "wav2lip_gan.pth"),
        "--face", image_file_path,
        "--audio", audio_file_path,
        "--outfile", output_video_path,
    ]

    try:
        logging.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logging.info(f"Command output: {result.stdout}")
        return output_video_path
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while generating the video: {e.stderr}")
        st.error(f"An error occurred while generating the video: {e.stderr}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        logging.error(traceback.format_exc())
        st.error(f"An unexpected error occurred: {str(e)}")
        return None


def play_lip_sync_video(output_video_path):
    if output_video_path:
        st.header("Generating response to your query...")
        st.video(output_video_path)
        st.header("Video playback ended!")

def main():
    my_expander = st.expander("Ask me a question!", expanded=False)
    with my_expander:
        tab1, tab2 = st.columns([1, 1])
        
        # Record Audio Tab
        with tab1:
            st.header("Record Audio")
            audio_bytes = audio_recorder(text="Click to start recording.")
            if audio_bytes:
                st.cache_data.clear()
                audio_file_path = save_audio_file(audio_bytes, "mp3")
                transcript_text = transcribe_audio(audio_file_path)
                os.remove(audio_file_path)
                if transcript_text != "I'm sorry, I couldn't catch that. Could you please repeat your question?":
                    st.header("Transcript")
                    st.write(transcript_text)
                    conversation_context = ""
                    question = transcript_text
                    response = cb.get_response_from_bot(question)
                    conversation_context += f"Question: {question}\nAnswer: {response}\n"
                    cb.store_context(conversation_context)
                    if response:
                        st.header("Response")
                        st.write(response)
                        audio_filename = text_to_speech(response)
                        st.audio(audio_filename)
                        image_file_path = "//enter//path//to/your//bot//image"
                        output_video_path = generate_lip_sync_video(response, image_file_path)
                        play_lip_sync_video(output_video_path)

        # Chat Tab
        with tab2:
            st.header("Chat")
            query = st.text_area("Enter question here.", label_visibility="hidden")
            button = st.button("Submit")
            if button and query.strip():
                st.cache_data.clear()
                question = query.strip()
                response = cb.get_response_from_bot(question)
                if response:
                    st.header("Response")
                    st.write(response)
                    audio_filename = text_to_speech(response)
                    st.audio(audio_filename)
                    image_file_path = "//enter//path//to//your//image//bot"
                    output_video_path = generate_lip_sync_video(response, image_file_path)
                    play_lip_sync_video(output_video_path)

working_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(working_dir)

try:
    main()
except Exception as e:
    logging.error(f"An error occurred in main: {str(e)}")
    logging.error(traceback.format_exc())
    st.error(f"An error occurred (Please refresh and try): {e}")
    st.info("We ran into a problem. We're still in beta. Please refresh and try!")
