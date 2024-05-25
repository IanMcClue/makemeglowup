import streamlit as st
import base64
import openai
from PIL import Image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_response(base64_image):
    # Load OpenAI API key from secrets.toml
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    MODEL = "gpt-4o"
    client = openai.Client(api_key=openai_api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that determines the user's emotion and the color they give off based on the uploaded image."},
            {"role": "user", "content": [
                {"type": "text", "text": "Here's an image. What's the user's emotion and the color they give off?"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ]
    )

    return response.choices[0].message.content

st.title('Emotion and Color Image Processing')

image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if image_file:
    image = Image.open(image_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    base64_image = encode_image(image_file.name)
    response = get_response(base64_image)
    st.markdown(response, unsafe_allow_html=True)
