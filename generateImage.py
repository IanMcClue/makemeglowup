import streamlit as st
import base64
import openai
from PIL import Image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_response(base64_image, emotion, color):
    # Load OpenAI API key from secrets.toml
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    MODEL = "gpt-4o"
    client = openai.Client(api_key=openai_api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that responds to images, emotions, and colors."},
            {"role": "user", "content": [
                {"type": "text", "text": f"Here's an image. The user is feeling {emotion} and their favorite color is {color}."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ]
    )

    return response.choices[0].message.content

st.title('Emotion and Color Image Processing')

image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
emotion = st.text_input("Enter your current emotion")
color = st.text_input("Enter your favorite color")

if image_file and emotion and color:
    image = Image.open(image_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    base64_image = encode_image(image_file.name)
    response = get_response(base64_image, emotion, color)
    st.markdown(response, unsafe_allow_html=True)
