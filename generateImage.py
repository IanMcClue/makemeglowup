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
    size = 1024  # Fixed size that is less than 4MB
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
    for i, variation in enumerate(variation_response.data):
        url = variation.url
        st.image(url, caption=f'Variation {i+1}', use_column_width=True)

    # Save the variation images to disk
    image_dir = "variation_images"  # The directory where the images will be saved
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    variation_urls = [datum.url for datum in variation_response.data]  # Extract URLs
    variation_images = [requests.get(url).content for url in variation_urls]  # Download images
    variation_image_names = [f"variation_image_{i}.png" for i in range(len(variation_images))]  # Create names
    variation_image_filepaths = [os.path.join(image_dir, name) for name in variation_image_names]  # Create filepaths
    for image, filepath in zip(variation_images, variation_image_filepaths):  # Loop through the variations
        with open(filepath, "wb") as image_file:  # Open the file
            image_file.write(image)  # Write the image to the file

    # Print the variation image filepaths
    for filepath in variation_image_filepaths:
        st.write(filepath)
