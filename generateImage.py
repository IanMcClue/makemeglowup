import streamlit as st
from openai import OpenAI

# Initialize OpenAI client and set the API key
OpenAI.api_key = st.secrets["OPENAI_API_KEY"]  # Replace "OPENAI_API_KEY" with the actual key in your secrets.toml file
client = OpenAI()

# Initialize Streamlit app
st.title("Poetic Programming Explanations")

user_input = st.text_input("Enter a programming concept to be explained poetically")

if st.button("Generate Poem"):
    if user_input:
        # Create a chat completion
        completion = client.chat.completions.create(
            model="text-davinci-003",
            messages=[
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": f"Compose a poem that explains the concept of {user_input} in programming."}
            ]
        )

        # Display the generated poem
        st.write(completion.choices[0].message.content)
    else:
        st.write("Please enter a programming concept")
