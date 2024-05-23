import streamlit as st
from openai import OpenAI, OpenAIError
from PIL import Image
import io
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Title of the Streamlit app
st.title("Image Editing App")

# File uploader for image and mask
uploaded_image = st.file_uploader("Upload an image", type="png")
uploaded_mask = st.file_uploader("Upload a mask", type="png")

# Display uploaded images
if uploaded_image is not None and uploaded_mask is not None:
    st.image(uploaded_image, caption="Uploaded Image", width=300)
    st.image(uploaded_mask, caption="Uploaded Mask", width=300)
    prompt_input = st.text_input("Enter prompt:", value="", max_chars=100)

    # Button to trigger image editing
    if st.button("Edit Image"):
        with st.spinner("Editing image..."):
            try:
                # Initialize OpenAI client with API key
                client = OpenAI(api_key=openai_api_key)

                # Read the uploaded image and mask data as bytes
                image_data = uploaded_image.read()
                mask_data = uploaded_mask.read()

                # Call OpenAI API to edit the image
                response = client.images.edit(
                    image=image_data,
                    mask=mask_data,
                    prompt=prompt_input,
                    n=1,
                    size="1024x1024",
                    response_format="url",
                )

                # Access the generated image URL
                edited_image_url = response['data'][0]['url']

                # Display the edited image
                st.image(edited_image_url, caption="Edited Image", width=300)

            except OpenAIError as e:
                st.error(f"An error occurred: {str(e)}")
else:
    st.write("Please upload both an image and a mask.")
