import streamlit as st
import openai

# 1. Page Configuration
st.set_page_config(
    page_title="Custom Research Assistant", 
    page_icon="🤖", 
    layout="centered"
)

st.title("Custom Assistant")
st.caption("Powered by Perplexity API")

# 2. Hidden System Instructions
# Add your custom prompt instructions here. External users CANNOT view this text.
HIDDEN_SYSTEM_INSTRUCTIONS = """
You are a specialized expert assistant.
Follow these constraints strictly:
1. Provide accurate, clear, and well-structured answers using web-verified information.
2. Maintain a professional, executive, and objective tone.
3. If information is uncertain, state it clearly rather than guessing.
"""

# 3. Sidebar Authentication (User enters their API key)
with st.sidebar:
    st.header("Authentication")
    st.write("To use this assistant, enter your Perplexity API key below.")
    user_api_key = st.text_input(
        "Perplexity API Key:",
        type="password",
        help="Find or generate your API key at perplexity.ai/settings/api"
    )
    st.markdown("[Get a Perplexity API Key](https://www.perplexity.ai/settings/api)")

# Block execution if the user hasn't provided a key
if not user_api_key:
    st.info("👈 Please enter your Perplexity API key in the sidebar to start chatting.")
    st.stop()

# 4. Initialize Perplexity Client using the User's API Key
client = openai.OpenAI(
    api_key=user_api_key,
    base_url="https://api.perplexity.ai"
)

# 5. Initialize Conversation History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": HIDDEN_SYSTEM_INSTRUCTIONS}
    ]

# 6. Render Previous Chat Messages (Skip system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. Handle User Chat Input
if prompt := st.chat_input("Ask a question..."):
    # Append user input to session history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Render user prompt in UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream assistant response from Perplexity API
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="sonar",  # Perplexity real-time web model
                messages=st.session_state.messages,
                stream=True
            )
            response_text = st.write_stream(stream)
            
            # Save assistant response to session history
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"API Error: Please check your API key and balance. Details: {e}")
