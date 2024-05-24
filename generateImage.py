import streamlit as st
import openai
import numpy as np
import requests
from PIL import Image
import base64
import os

# Set the API key and model name
openai.api_key = st.secrets["openai_api_key"]
MODEL = "gpt-4o"
client = openai.Client()

def analyze_image(image):
    # Encode the image as base64
    image_base64 = base64.b64encode(image).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{image_base64}"

    # Create a completion using the GPT-4o model
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that describes the mood and color of a person in the image."},
            {"role": "user", "content": [
                {"type": "text", "text": "Describe the mood and color of the person in the image."},
                {"type": "image_url", "image_url": {"url": image_url}}},
            ]},
        ],
        temperature=0.0,
    )

    # Extract the mood and color from the completion
    mood = completion.choices[0].message.content.split("\n")[0].split(": ")[1]
    color_choice = completion.choices[0].message.content.split("\n")[1].split(": ")[1]

    return mood, color_choice

def generate_image(emotion, color_choice):
    # Create an image using the DALL-E 3 model
    response = client.images.generate(
        prompt=f"{emotion} {color_choice} aura",
        model="dalle3",
        response_format="b64_json",
    )

    # Decode the image from base64 and return it
    image_base64 = response.choices[0].data.b64_json
    image = base64.b64decode(image_base64)

    return image

st.title("Make Me Glow Up")

# Upload an image of a person
image_file = st.file_uploader("Upload an image of a person", type=["jpg", "jpeg", "png"])

if image_file:
    # Load the image using PIL
    image = Image.open(image_file)

    # Display the original image
    st.subheader("Original Image")
    st.image(image)

    # Analyze the image
    mood, color_choice = analyze_image(image)

    # Display the mood and color
    st.subheader("Mood and Color")
    st.write(f"Mood: {mood}")
    st.write(f"Color: {color_choice}")

    # Generate the aura image
    aura_image = generate_image(mood, color_choice)

    # Convert the aura image to PIL format
    aura_image = Image.fromarray(np.uint8(aura_image))

    # Display the aura image
    st.subheader("Aura Image")
    st.image(aura_image)

    # Save the aura image
    aura_image.save("aura_image.png")
