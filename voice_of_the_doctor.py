import os
import platform
import subprocess
import time
from gtts import gTTS
import playsound  # Install with: pip install playsound
import elevenlabs
from elevenlabs.client import ElevenLabs

# Load API Key
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

if ELEVENLABS_API_KEY is None:
    print("Error: ELEVENLABS_API_KEY is missing! Set it before running.")
else:
    print("✅ ElevenLabs API Key detected!")

# -------------------- gTTS Text-to-Speech Function --------------------
def text_to_speech_with_gtts(input_text, output_filepath):
    print("\n🔹 Generating audio using gTTS...")
    
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)
    
    print(f"✅ gTTS audio saved as: {output_filepath}")
    
    # Play audio
    play_audio(output_filepath)

# -------------------- ElevenLabs Text-to-Speech Function --------------------
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    if ELEVENLABS_API_KEY is None:
        print("❌ Error: ElevenLabs API key is missing!")
        return

    print("\n🔹 Generating audio using ElevenLabs...")
    
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    
    elevenlabs.save(audio, output_filepath)
    print(f"✅ ElevenLabs audio saved as: {output_filepath}")
    
    # Play audio
    play_audio(output_filepath)

# -------------------- Audio Playback Function --------------------
def play_audio(filepath):
    print(f"\n🔊 Playing: {filepath}")

    if not os.path.exists(filepath):
        print(f"❌ Error: File not found - {filepath}")
        return
    
    os_name = platform.system()
    try:
        if os_name == "Windows":
            playsound.playsound(filepath)
        elif os_name == "Darwin":  # macOS
            subprocess.run(['afplay', filepath])
        elif os_name == "Linux":
            subprocess.run(['aplay', filepath])  # Use 'mpg123' or 'ffplay' if needed
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"❌ Error playing audio: {e}")

# -------------------- Run Text-to-Speech --------------------
input_text = "Hi, this is AI with Shrikant! Testing voice output."

# ✅ Run gTTS
text_to_speech_with_gtts(input_text, "gtts_testing.mp3")

# ✅ Run ElevenLabs (Uncomment if you want to test)
# text_to_speech_with_elevenlabs(input_text, "elevenlabs_testing.mp3")
