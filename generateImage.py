import streamlit as st
import openai
import numpy as np
import requests
from PIL import Image
import base64
import io

# Load OpenAI API key from secrets.toml
openai_api_key = st.secrets["OPENAI_API_KEY"]
MODEL = "gpt-4o"
client = openai.Client(api_key=openai_api_key)

def analyze_image(image):
    # Convert the image to bytes
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()

    # Encode the image as base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{image_base64}"

    # Create a completion using the GPT-4o model
    messages = [
        {"role": "system", "content": "You are a helpful assistant that describes the mood and color of a person in the image."},
        {"role": "user", "content": [
            {"type": "text", "text": "Describe the mood and color of the person in the image."},
            {"type": "image_url", "image_url": image_url}
        ]}
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.0,
    )

    # Extract the mood and color from the completion
    mood = response.choices[0].message.content.split("\n")[0].split(": ")[1]
    color_choice = response.choices[0].message.content.split("\n")[1].split(": ")[1]

    return mood, color_choice

def generate_image(emotion, color_choice):
    # Create an image using the DALL-E 2 model
    response = client.images.create(
        prompt=f"{emotion} {color_choice} aura",
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )

    # Decode the image from base64 and return it
    image_base64 = response.data[0].b64_json
    image = base64.b64decode(image_base64)

    return image

st.title("Make Me Glow Up")

# Upload an image of a person
image_file = st.file_uploader("Upload an image of a person", type=["jpg", "jpeg", "png"])

if image_file:
    # Load the image using PIL
    image = Image.open(image_file)

    # Resize the image to be square and less than 4MB
    size = 1024  # Fixed size that is less than 4MB
    image = image.resize((size, size))
    image = image.convert("RGB")

    # Display the original image
    st.subheader("Original Image")
    st.image(image, use_column_width=True)

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
    st.image(aura_image, use_column_width=True)

    # Save the aura image
    aura_image.save("aura_image.png")
