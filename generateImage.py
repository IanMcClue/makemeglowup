import os
import streamlit as st
from openai import OpenAI, OpenAIError
import requests
from PIL import Image
import io

st.title("Image Editing App")

# Load OpenAI API key from secrets.toml
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Upload image and mask
uploaded_image = st.file_uploader("Upload an image", type="png")
uploaded_mask = st.file_uploader("Upload a mask", type="png")

if uploaded_image is not None and uploaded_mask is not None:
    # Resize the uploaded images to reduce their file size
    max_size = (1024, 1024)
    resized_image = Image.open(io.BytesIO(uploaded_image.read())).resize(max_size)
    resized_mask = Image.open(io.BytesIO(uploaded_mask.read())).resize(max_size)

    st.image(resized_image, caption="Uploaded Image", width=300)
    st.image(resized_mask, caption="Uploaded Mask", width=300)
    prompt_input = st.text_input("Enter prompt:", value="", max_chars=100)

    # Edit the image using OpenAI
    if st.button("Edit Image"):
        with st.spinner("Editing image..."):
            try:
                # Use the previously loaded OpenAI API key
                client = OpenAI(api_key=openai_api_key)

                # Convert the resized images to bytes and send them to the OpenAI API
                image_bytes = io.BytesIO()
                resized_image.save(image_bytes, format="PNG")
                image_bytes.seek(0)

                mask_bytes = io.BytesIO()
                resized_mask.save(mask_bytes, format="PNG")
                mask_bytes.seek(0)

                response = client.images.edit(
                    image=image_bytes,
                    mask=mask_bytes,
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
