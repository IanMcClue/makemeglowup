import streamlit as st
import openai
import base64

# Set the API key and model name
openai.api_key = st.secrets["openai_api_key"]
MODEL = "gpt-4o"

def analyze_image(image):
    client = openai.Client()

    # Encode the image as base64
    image_base64 = base64.b64encode(image).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{image_base64}"

    # Create a completion using the GPT-4o model
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that describes the mood and color of a person in the image."},
            {"role": "user", "content": [
                {"type": "text", "text": "Describe the mood and color of the person in the image."},
                {"type": "image_url", "image_url": {"url": image_url}}},
            ]},
        ],
        temperature=0.0,
    )

    # Extract the mood and color from the completion
    mood = completion.choices[0].message.content.split("\n")[0].split(": ")[1]
    color_choice = completion.choices[0].message.content.split("\n")[1].split(": ")[1]

    return mood, color_choice

def generate_image(emotion, color_choice):
    client = openai.Client()

    # Create an image using the DALL-E 3 model
    response = client.images.generate(
        prompt=f"{emotion} {color_choice} aura",
        model="dalle3",
        response_format="b64_json",
        image_url=[{"type": "image_url", "image_url": image_url}] # <-- fixed
    )

    # Decode the image from base64 and return it
    image_base64 = response.choices[0].data.b64_json
    image = base64.b64decode(image_base64)

    return image

st.title("Make Me Glow Up")

# Upload an image of a person
image_file = st.file_uploader("Upload an image of a person", type=["jpg", "
