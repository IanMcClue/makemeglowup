import streamlit as st
import base64
import openai
from PIL import Image
import io

# Function to encode image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Function to get response from OpenAI
def get_response(base64_image):
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    openai.api_key = openai_api_key  # Correct way to set the API key

    MODEL = "gpt-4"

    # Constructing the prompt with the base64 image data
    prompt = f"Here's an image (base64-encoded): {base64_image}. What is the user's emotion and the color they give off?"

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that determines the user's emotion and the color they give off based on the uploaded image."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app layout
st.title('Emotion and Color Image Processing')

image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if image_file:
    # Display the uploaded image
    image = Image.open(image_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Encode the image to base64
    base64_image = encode_image(image_file)

    # Get the response from the OpenAI API
    response = get_response(base64_image)
    
    # Display the response
    st.markdown(response, unsafe_allow_html=True)
