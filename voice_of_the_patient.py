# Load environment variables
from dotenv import load_dotenv
import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Step 1: Setup Audio Recorder
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Records audio from the microphone and saves it as an MP3 file.

    Args:
        file_path (str): Path to save the recorded audio file.
        timeout (int): Max time to wait for speech (seconds).
        phrase_time_limit (int): Max time for the phrase (seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert to MP3 format
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred while recording audio: {e}")

# Set the audio file path
audio_filepath = "patient_voice_test_for_patient.mp3"

# 🔹 Call the recording function (Uncommented)
record_audio(file_path=audio_filepath)

# Step 2: Speech-to-Text (STT) Transcription
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Validate API key
if not GROQ_API_KEY:
    logging.error("GROQ_API_KEY is not set. Please check your environment variables.")
    exit(1)

stt_model = "whisper-large-v3"

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    """
    Transcribes an audio file using the Groq API.

    Args:
        stt_model (str): Model name for STT.
        audio_filepath (str): Path to the audio file.
        GROQ_API_KEY (str): API key for authentication.

    Returns:
        str: Transcribed text.
    """
    try:
        if not os.path.exists(audio_filepath):
            logging.error(f"Audio file {audio_filepath} not found!")
            return ""

        client = Groq(api_key=GROQ_API_KEY)

        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )

        logging.info(f"Transcription Output: {transcription.text}")
        return transcription.text

    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")
        return ""

# 🔹 Call the transcription function
transcription_text = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)

# Print final transcription
if transcription_text:
    print("\nFinal Transcription:", transcription_text)
else:
    print("\nTranscription failed.")
