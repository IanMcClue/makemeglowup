import streamlit as st
import base64
import openai
from PIL import Image

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

def get_response(base64_image):
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    openai.api_key = openai_api_key  # Correct way to set the API key

    MODEL = "gpt-4o"

    # Constructing the messages with the base64 image data
    messages = [
        {"role": "system", "content": "You are a helpful assistant that determines the user's emotion and the color they give off based on the uploaded image."},
        {"role": "user", "content": f"Here's an image (base64-encoded): {base64_image}. What is the user's emotion and the color they give off?"}
    ]

    try:
        response = openai.api_requestor.APIRequestor().request(
            "post",
            f"/v1/completions",
            json={
                "model": MODEL,
                "prompt": messages,
                "temperature": 0.0,
            },
            headers={
                "Authorization": f"Bearer {openai_api_key}",
            },
        )
        return response.json()["choices"][0]["text"]
    except Exception as e:
        return f"Error: {str(e)}"

st.title('Emotion and Color Image Processing')

openai_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = openai_api_key  # Correct way to set the API key

image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if image_file:
    image = Image.open(image_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    base64_image = encode_image(image_file)
    response = get_response(base64_image)
    st.markdown(response, unsafe_allow_html=True)
