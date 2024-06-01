import streamlit as st
from openai import OpenAI
import base64
import os

# Initialize OpenAI client and set the API key from Streamlit secrets
MODEL = "gpt-4o"
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai = OpenAI(api_key=openai_api_key)

# Function to encode image as base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Display a file uploader in Streamlit
uploaded_file = st.file_uploader("Choose an image...", type="png")
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    # Save the uploaded file to a temporary location
    temp_image_path = "temp_image.png"
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    base64_image = encode_image(temp_image_path)
    
    # Make a request to the OpenAI API
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that responds in Markdown. Help me with my math homework!"},
            {"role": "user", "content": [
                {"type": "text", "text": "What's the area of the triangle?"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]}
        ],
        temperature=0.0,
    )
    
    # Display the response from OpenAI
    st.markdown(response.choices[0].message.content)
    
    # Remove the temporary image file
    os.remove(temp_image_path)
