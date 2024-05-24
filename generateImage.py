import os
import streamlit as st
from openai import OpenAI, OpenAIError
import requests
from PIL import Image
import io

st.title("Image Editing App")

# Load OpenAI API key from secrets.toml
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Upload image
uploaded_image = st.file_uploader("Upload an image", type="png")

if uploaded_image is not None:
    # Resize the uploaded image to reduce its file size
    max_size = (1024, 1024)
    resized_image = Image.open(io.BytesIO(uploaded_image.read())).resize(max_size)

    st.image(resized_image, caption="Uploaded Image", width=300)

    # Create a custom mask
    width = 1024
    height = 1024
    mask = Image.new("RGBA", (width, height), (0, 0, 0, 1))  # create an opaque image mask

    # set the bottom half to be transparent
    for x in range(width):
        for y in range(height // 2, height):  # only loop over the bottom half of the mask
            # set alpha (A) to zero to turn pixel transparent
            alpha = 0
            mask.putpixel((x, y), (0, 0, 0, alpha))

    st.image(mask, caption="Custom Mask", width=300)

    prompt_input = st.text_input("Enter prompt:", value="", max_chars=100)

    # Edit the image using OpenAI
    if st.button("Edit Image"):
        with st.spinner("Editing image..."):
            try:
                # Use the previously loaded OpenAI API key
                client = OpenAI(api_key=openai_api_key)

                # Convert the resized image and custom mask to bytes and send them to the OpenAI API
                image_bytes = io.BytesIO()
                resized_image.save(image_bytes, format="PNG")
                image_bytes.seek(0)

                mask_bytes = io.BytesIO()
                mask.save(mask_bytes, format="PNG")
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
    st.write("Please upload an image.")
