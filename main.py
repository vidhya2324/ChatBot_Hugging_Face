import os
import json
import streamlit as st
import requests
import streamlit.components.v1 as components

# Configuring API key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
HF_API_KEY = config_data["HUGGINGFACE_API_KEY"]  # Use your Hugging Face API key

# Hugging Face API URL (Replace with your desired model)
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-3B"

# Streamlit page settings
st.set_page_config(
    page_title="Hugging Face Chatbot",
    page_icon="💬",
    layout="centered"
)

# Initialize chat session in Streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Custom HTML and CSS for better UI
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            text-align: center;
        }
        .chat-container {
            max-width: 600px;
            margin: auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        }
        .title {
            font-size: 28px;
            font-weight: bold;
            color: #007BFF;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="title">🤯 ChatSphere</div>
    </div>
</body>
</html>
"""

# Display the HTML
components.html(html_code, height=100)

# Display chat history properly
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask something...")

if user_prompt:
    # Add user's message to chat and display it immediately
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.write(user_prompt)

    # Send user message to Hugging Face API
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            assistant_response = response.json()[0]["generated_text"]
        else:
            assistant_response = f"⚠️ API Error {response.status_code}: {response.text}"
    except Exception as e:
        assistant_response = f"⚠️ API Request Failed: {str(e)}"

    # Add bot response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display assistant response immediately
    with st.chat_message("assistant"):
        st.write(assistant_response)

    # Ensure UI updates immediately
    st.rerun()
