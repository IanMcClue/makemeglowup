import streamlit as st
import openai
import numpy as np
import requests
from PIL import Image
import base64
import os

# Set the API key and model names
openai.api_key = st.secrets["openai_api_key"]
GPT4O_MODEL = "gpt-4o"
DALL_E_3_MODEL = "dall-e-3"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_image(image):
    client = openai.Client()

    base64_image = encode_image(image)
    image_url = f"data:image/png;base64,{base64_image}"

    response = client.chat.completions.create(
        model=GPT4O_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that describes the mood and color of a person in the image."},
            {"role": "user", "content": [
                {"type": "text", "text": "Describe the mood and color of the person in the image."},
                {"type": "image_url", "image_url": {"url": image_url}}},
            ]},
        ],
        temperature=0.0,
    )

    mood = None
    color_choice = None

    for result in response.choices[0].message.content.split("\n"):
        if "mood" in result:
            mood = result.split(": ")[-1]
        if "color" in result:
            color_choice = result.split(": ")[-1]

    return mood, color_choice

def generate_aura_image(emotion, color_choice):
    client = openai.Client()

    prompt = f"Create a high-fidelity, circular aura image that exudes a sense of energy and {emotion}. " \
             f"The aura should be a gradient, using only various shades of {color_choice} that seamlessly blend into one another. " \
             f"Start with a light, pastel shade of {color_choice} at the outermost edge, gradually transitioning to a vibrant, mid-tone shade in the middle, " \
             f"and finally, a deep, rich shade of {color_choice} at the innermost part of the circle. The transition between the shades should be smooth and refined, " \
             f"creating a polished, high-quality finish. The image should be centered on a black background to make the {color_choice} tones pop and to add depth and contrast to the overall composition."

    generation_response = client.images.generate(
        model=DALL_E_3_MODEL,
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="url",
    )

    image_url = generation_response.data[0].url
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))

    return image

st.title("Aura Generator")

uploaded_image = st.file_uploader("Upload an image of a person", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    mood, color_choice = analyze_image(uploaded_image)

    st.write(f"Mood: {mood}")
    st.write(f"Color choice: {color_choice}")

    aura_image = generate_aura_image(mood, color_choice)
    st.image(aura_image, caption="Generated Aura", use_column_width=True)
