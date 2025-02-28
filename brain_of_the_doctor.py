from dotenv import load_dotenv
import os
import base64
from groq import Groq

# Load environment variables
load_dotenv()

# Check if API key is available
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY is missing. Check your .env file!")
    exit()


query = "Is there something wrong with my face?"
model = "llama-3.2-90b-vision-preview"

def encode_image(image_path):   
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: Image file '{rD:\AI_DOCTOR_VOICE_BOT\acne.jpg}' not found.")
        exit()

def analyze_image_with_query(query, model, encoded_image):
    try:
        client = Groq(api_key=GROQ_API_KEY)  
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
                ],
            }
        ]
        chat_completion = client.chat.completions.create(messages=messages, model=model)

        return chat_completion.choices[0].message.content
    
    except Exception as e:
        print("Error:", e)
        return None

# Run the script
if __name__ == "__main__":
    image_path = "acne.jpg"  # Change this to your actual image file path
    encoded_image = encode_image(image_path)
    response = analyze_image_with_query(query, model, encoded_image)

    if response:
        print("Response from model:", response)
    else:
        print("Failed to get a response from the model.")
