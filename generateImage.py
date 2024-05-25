import streamlit as st
import base64
import openai
import os
from PIL import Image

# Ensure you are using the latest version of the openai package
# pip install --upgrade openai

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

def get_response(base64_image):
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    prompt = f"Here's an image (base64-encoded): {base64_image}. What is the user's emotion and the color they give off?"

    try:
        messages = [
            {"role": "system", "content": "You are an assistant that analyzes images and determines the user's emotion and the color they give off."},
            {"role": "user", "content": prompt}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Adjust the model name if necessary
            messages=messages,
            temperature=0.7,
            max_tokens=200,
            top_p=1,
        )

        choices = response.choices[0]
        text = choices.message.content
        return text
    except Exception as e:
        return f"Error: {str(e)}"

st.title('Emotion and Color Image Processing')

image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if image_file is not None:
    # Display the uploaded image
    image = Image.open(image_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Encode the image
    base64_image = encode_image(image_file)

    # Get the response
    response = get_response(base64_image)

    # Display the response
    st.write("Response from the model:")
    st.write(response)
