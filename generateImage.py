import os
import streamlit as st
from openai import OpenAI, OpenAIError
import requests
from PIL import Image

st.title("Image Editing App")

# Load OpenAI API key from secrets.toml
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Upload image and mask
uploaded_image = st.file_uploader("Upload an image", type="png")
uploaded_mask = st.file_uploader("Upload a mask", type="png")

if uploaded_image is not None and uploaded_mask is not None:
    st.image(uploaded_image, caption="Uploaded Image", width=300)
    st.image(uploaded_mask, caption="Uploaded Mask", width=300)
    prompt_input = st.text_input("Enter prompt:", value="", max_chars=100)

    # Edit the image using OpenAI
    if st.button("Edit Image"):
        with st.spinner("Editing image..."):
            try:
                # Access the API key from Streamlit environment variables
                api_key = st.secrets["openai_api_key"]

                client = OpenAI(api_key=api_key)

                # Read the uploaded image and mask data as bytes
                image_data = uploaded_image.read()
                mask_data = uploaded_mask.read()

                response = client.images.edit(
                    image=image_data,
                    mask=mask_data,
                    prompt=prompt_input,
                    n=1,
                    size="1024x1024",
                    response_format="url",
                )

                # Access the generated image URL
                edited_image_url = response.data[0].url

                # Display the edited image
                st.image(edited_image_url, caption="Edited Image", width=300)

            except OpenAIError as e:
                st.error(f"An error occurred: {str(e)}")
            except KeyError:
                st.error("OpenAI API key is not set. Please set it in Streamlit's advanced settings.")

else:
    st.write("Please upload both an image and a mask.")
