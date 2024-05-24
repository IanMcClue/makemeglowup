import streamlit as st
import openai
import requests
from PIL import Image
import os

# Set your OpenAI API key
openai.api_key = st.secrets["openai_api_key"]

# Create a file uploader
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read the image file
    image = Image.open(uploaded_file)

    # Resize the image to be square and less than 4MB
    size = min(image.size)
    while os.path.getsize(uploaded_file.name) > 4 * 1024 * 1024:
        size -= 100
        image = image.resize((size, size))
    image = image.resize((size, size))

    # Convert the image to PNG if necessary
    if uploaded_file.type not in ["png"]:
        image = image.convert("RGB")
        image_file = "temp_image.png"
        image.save(image_file, "PNG")
        with open(image_file, "rb") as img_file:
            img_data = img_file.read()
    else:
        with open(uploaded_file, "rb") as img_file:
            img_data = img_file.read()

    # Display the original image
    st.image(image, caption='Original Image', use_column_width=True)

    # Use the OpenAI API to create image variations
    variation_response = openai.Image.create_variation(
        image=img_data,
        n=2,
        size="1024x1024",
        response_format="url",
    )

    # Display the variation images
    for i, url in enumerate(variation_response["data"]):
        st.image(url, caption=f'Variation {i+1}', use_column_width=True)
