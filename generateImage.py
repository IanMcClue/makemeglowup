import streamlit as st
from openai import OpenAI
import base64
import os

# Initialize OpenAI client and set the API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)
MODEL = "gpt-4o"

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Streamlit app
def main():
    st.title("Image Description Generator")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Convert the file to an image path
        image_path = "temp_image.jpg"  # Temporary file path
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Encode the image to base64
        base64_image = encode_image(image_path)

        # Display the image
        st.image(image_path, caption='Uploaded Image', use_column_width=True)

        # Generate description using OpenAI GPT-4
        if st.button("Generate Description"):
            # Use the client to make a request with the specified model
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Describe the following image."},
                    {"role": "user", "content": f"Here is the image: {base64_image}"}
                ]
            )
            st.write("Description:")
            st.write(completion.choices[0].message["content"].strip())

if __name__ == "__main__":
    main()