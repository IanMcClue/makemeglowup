import streamlit as st
import openai
import requests
from PIL import Image
import io
import os

# Load OpenAI API key from secrets.toml
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Create a client for the OpenAI API
client = openai.Client(api_key=openai_api_key)

# Create a file uploader
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

# Create a number input for the number of variations
num_variations = st.number_input("Number of variations", min_value=1, max_value=10, value=2)

# Create a selectbox for the size of the variations
size_options = ["256x256", "512x512", "1024x1024"]
variation_size = st.selectbox("Size of variations", size_options)

if uploaded_file is not None:
    # Read the image file
    image = Image.open(uploaded_file)

    # Resize the image to be square and less than 4MB
    size = min(image.size)
    while len(uploaded_file) > 4 * 1024 * 1024:
        size -= 100
        image = image.resize((size, size))
    image = image.convert("RGB")

    # Convert the image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    # Display the original image
    st.image(image, caption='Original Image', use_column_width=True)

    # Use the OpenAI API to create image variations
    variation_response = client.images.create_variation(
        image=image_bytes,
        n=num_variations,
        size=variation_size,
        response_format="url",
    )

    # Display the variation images
    for i, url in enumerate(variation_response["data"]):
        st.image(url, caption=f'Variation {i+1}', use_column_width=True)