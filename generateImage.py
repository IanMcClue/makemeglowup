import streamlit as st
from openai import OpenAI
import base64
import os

# Initialize OpenAI client and set the API key from Streamlit secrets
MODEL = "gpt-4o"
openai.api_key = st.secrets["OPENAI_API_KEY"]

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
            # Set the model to "gpt-4o" when making the API call
            model = "gpt-4o"  # Replace with the actual model ID you have access to

            # Use the client to make a request with the specified model
            response = client.Completion.create
                model=MODEL,
                prompt=f"Describe the following image in a few words: {base64_image}",
                max_tokens=200,
                temperature=0.5,
            )
            st.write("Description:")
            st.write(response.choices[0].text.strip())

if __name__ == "__main__":
    main()