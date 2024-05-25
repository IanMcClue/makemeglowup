import streamlit as st
import base64
import openai
from PIL import Image

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

def get_response(base64_image):
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    MODEL = "gpt-4.0"

    # Constructing the messages with the base64 image data
    messages = [
        {"role": "system", "content": "You are a helpful assistant that determines the user's emotion and the color they give off based on the uploaded image."},
        {"role": "user", "content": f"Here's an image (base64-encoded): {base64_image}. What is the user's emotion and the color they give off?"}
    ]

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0.0
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"

st.title('Emotion and Color Image Processing')

image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
