import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO
import base64

# Load OpenAI API key from .streamlit/credentials.toml
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = openai_api_key

# Initialize OpenAI client
client = openai.Client()

st.title("Image Variation Generator")
st.write("Upload an image to generate its variations using OpenAI's DALL-E.")

# Image upload
uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

# Convert uploaded image to PNG format and resize it
def convert_to_png(image, max_size=2048):
    img = Image.open(image)
    img = img.convert("RGBA")
    # Resize image
    img.thumbnail((max_size, max_size))
    with BytesIO() as f:
        img.save(f, format="PNG")
        return f.getvalue()

# Function to call OpenAI API for image variations
def generate_variations(image_data, n=1, size="1024x1024", response_format="url"):
    try:
        response = client.images.create_variation(
            model="dall-e-2",
            image=image_data,
            n=n,
            size=size,
            response_format=response_format
        )
        return response.data or []
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return []

if uploaded_image is not None:
    st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

    with st.spinner("Generating variations..."):
        image_data = convert_to_png(uploaded_image)
        variations = generate_variations(image_data)

    st.write("Generated Variations:")
    for i, variation in enumerate(variations):
        variation_url = variation['url']
        response = requests.get(variation_url)
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=f'Variation {i+1}', use_column_width=True)

        # Provide download link
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_data = buffered.getvalue()
        b64 = base64.b64encode(img_data).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="variation_{i+1}.png">Download Variation {i+1}</a>'
        st.markdown(href, unsafe_allow_html=True)
