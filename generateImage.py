import streamlit as st
from openai import OpenAI
import base64
import os

# Initialize OpenAI client and set the API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = openai_api_key

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

        # Generate description using OpenAI GPT-4o
        if st.button("Generate Description"):
            # Assuming 'client' is defined and follows the pattern from your documentation
            response = openai.Completion.create(
                model="text-davinci-003",  # Update this with the correct GPT-4 model when available
                prompt=f"Describe the following image: {base64_image}",
                max_tokens=200,
                temperature=0.5,
            )
            st.write("Description:")
            st.write(response.choices[0].text.strip())

if __name__ == "__main__":
    main()