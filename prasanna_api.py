import streamlit as st
import requests

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="Prasanna Google AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------
# Google AI Studio API Key
# --------------------------------
GOOGLE_API_KEY = "AQ.Ab8RN6Jd8bxGt78FaU_OS2207l_xklM7sZwB3C2aF5RRlDUIeA"

# Current Gemini model
MODEL = "gemini-3.8-flash"

API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent?key={GOOGLE_API_KEY}"
)

# --------------------------------
# Custom CSS
# --------------------------------
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 25px;
}

.stButton button {
    width: 100%;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# Title
# --------------------------------
st.markdown(
    '<div class="main-title">🤖 Prasanna Google AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Powered by Google Gemini</div>',
    unsafe_allow_html=True
)

# --------------------------------
# Initialize Chat History
# --------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------
# Display Chat History
# --------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------
# Clear Chat
# --------------------------------
if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()

# --------------------------------
# User Input
# --------------------------------
user_message = st.chat_input("Type your message here...")

if user_message:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # --------------------------------
    # Prepare Conversation History
    # --------------------------------
    contents = []

    for message in st.session_state.messages:

        if message["role"] == "user":
            role = "user"
        else:
            role = "model"

        contents.append(
            {
                "role": role,
                "parts": [
                    {
                        "text": message["content"]
                    }
                ]
            }
        )

    # --------------------------------
    # Send Request to Gemini
    # --------------------------------
    with st.chat_message("assistant"):

        with st.spinner("Gemini is thinking..."):

            try:

                data = {
                    "contents": contents
                }

                response = requests.post(
                    API_URL,
                    json=data,
                    headers={
                        "Content-Type": "application/json"
                    },
                    timeout=60
                )

                # --------------------------------
                # Successful Response
                # --------------------------------
                if response.status_code == 200:

                    result = response.json()

                    assistant_message = (
                        result["candidates"][0]
                        ["content"]["parts"][0]["text"]
                    )

                    st.markdown(assistant_message)

                    # Save assistant response
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": assistant_message
                        }
                    )

                # --------------------------------
                # API Error
                # --------------------------------
                else:

                    try:
                        error_data = response.json()

                        error_message = error_data.get(
                            "error",
                            {}
                        ).get(
                            "message",
                            "Unknown API error"
                        )

                    except Exception:
                        error_message = response.text

                    st.error(
                        f"Google Gemini API Error "
                        f"{response.status_code}: "
                        f"{error_message}"
                    )

            except requests.exceptions.Timeout:

                st.error(
                    "Request timed out. "
                    "Please try again."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Internet connection error. "
                    "Please check your internet connection."
                )

            except Exception as e:

                st.error(
                    f"Unexpected error: {str(e)}"
                )