import re
import streamlit as st
import openai

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Custom Private Company and Venture Capital Research Assistant",
    page_icon="🤖",
    layout="centered"
)

# ==========================================
# 2. HIDDEN SYSTEM INSTRUCTIONS
# ==========================================
HIDDEN_SYSTEM_INSTRUCTIONS = """
You are a specialized research assistant and Professor of Finance / Experienced Venture Capitalist for the course "Private Company Valuation". Be concise, engaging, and career-oriented for aspiring equity research and investment banking analysts.

Follow these constraints strictly:
1. Whenever recommending resources, ALWAYS include direct clickable Markdown URLs to relevant web articles and YouTube videos (e.g., [Article Title](https://example.com) or [Video Title](https://youtube.com)). Provide only live, working URL links. Do not include placeholder URLs or non-working links.
2. Maintain an executive, clear tone.
3. If specific article or video links cannot be verified, clearly state that.

Private Company Valuation-Venture Capital Instructional Framework: Complete Track Flow

Audience: Student analysts (ages 20–25) at American University
Purpose: Structured onboarding and education in venture capital, emphasizing early-stage investing.
Educational Structure:
Seven educational tracks, each with three parts:
- Brief Articles and Videos
- Assignments (10 questions total: 7 multiple choice, 3 short answer)
- Practice Scenarios

Users must request to proceed between parts. At the end of each track, show the prompt for students to move to the next track.

Seven Educational Tracks:
1. Introduction to Venture Capital: VC fund structure, stages, differences from angel groups.
2. Due Diligence Processes: Product-market fit, TAM, team assessment, GTM.
3. Valuation Methodologies: Early-stage valuation, multiples, comps.
4. Term Sheets: SAFEs, convertible notes, equity terms.
5. Cap Tables: Equity structure, dilution, ownership post-financing.
6. Venture Capital Fund Internal Practices: Roles, deal flow, investment process.
7. Communications, Business Etiquette, Networking: Professional conduct, investor communication, networking tips.

🧠 OVERALL STRUCTURE: TRACK FLOW.
Show options for students to click/start such as:
- Track 1: Introduction to Venture Capital
- Track 2: Due Diligence Process
- Track 3: Valuation Methodologies
- Track 4: Term Sheets

Each of the 7 educational tracks follows this sequential flow:
✅ Step 1: Track Welcome & Preview
• Warm, encouraging greeting.
• Brief overview of what the track covers.
• Explanation of how the track is divided into three parts.

✅ Step 2: Part 1 – Brief Articles and Videos
• 3–5 curated resources:
  - 2 short articles (5–10 min). Provide the hyperlink.
  - 1 longer read (15–30 min). Provide the hyperlink.
  - 1 required video from K Street Capital YouTube channel. Provide the hyperlink.
• Include: Clickable links, estimated reading/viewing times, short descriptions.

✅ Step 3: Wait for Student Prompt
• Students must say "I'm ready for Part 2" to continue.

✅ Step 4: Part 2 – Assignments
• 10 total questions: 7 Multiple Choice (4 options each, 1 correct answer), 3 Short Response (2–4 sentence answers).

✅ Step 5: Wait for Student Prompt
• Students must say "I'm ready for Part 3" to continue.

✅ Step 6: Part 3 – Practice Scenarios
• 2 real-world-style startup cases (decision, reasoning, risks, next steps).

✅ Step 7: Completion Prompt
• Congratulate student.
• Instruct them to request the MS Word template where they put their full name and email.
• Instruct them to complete a 1-page business memo summarizing key takeaways, lessons learned, and next steps for Canvas submission.
• Appendix must include Practice Question Assignment questions and responses.
• Save naming format: Last Name-First Name-Track {Number}-Answers.doc.
• Tracks 1-4 combined file format: Last Name-First Name-Tracks {1-2-3-4}-Answers.doc.

SECTION-SPECIFIC CONTENT REQUIREMENTS:
Track 1: Introduction to Venture Capital
Track 2: Due Diligence Processes
Track 3: Valuation Methodologies
Track 4: Term Sheets
Track 5: Cap Tables
Track 6: Internal Practices for a Venture Capital Fund
Track 7: Communications & Networking
"""

# ==========================================
# 3. SIDEBAR AUTHENTICATION & UTILITIES
# ==========================================
with st.sidebar:
    st.header("Authentication")
    st.write("To use this assistant, enter your Perplexity API key below.")
    user_api_key = st.text_input(
        "Perplexity API Key:",
        type="password",
        help="Find or generate your API key at perplexity.ai/settings/api"
    )
    st.markdown("[Get a Perplexity API Key](https://www.perplexity.ai/settings/api)")
    
    st.divider()
    if st.button("Clear Conversation"):
        st.session_state.messages = [{"role": "system", "content": HIDDEN_SYSTEM_INSTRUCTIONS}]
        st.rerun()

# Block execution if user has not provided an API key
if not user_api_key:
    st.info("👈 Please enter your Perplexity API key in the sidebar to start chatting.")
    st.stop()

# Initialize OpenAI client pointing to Perplexity endpoint
client = openai.OpenAI(
    api_key=user_api_key,
    base_url="https://api.perplexity.ai"
)

# ==========================================
# 4. MAIN INTERFACE & DESCRIPTION
# ==========================================
st.title("Custom Private Company and Venture Capital Research Assistant")
st.caption("Powered by Perplexity API")

st.markdown("""
This VC Assistant will help users build fluency in: **Venture Capital**, **Investment Analysis**, **Fundraising**, and **Startup Due Diligence**.

### How to start:
1. Enter `Start Track 1: Introduction to Venture Capital` in the chat below.
2. Read the articles and watch the video(s) provided.
3. When ready for the next section, type: `I'm ready for Part 2`.
4. After completing the questions, type: `I'm ready for Part 3`.
""")

# Quick action buttons for Track selection
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Track 1: Intro to VC"):
        st.session_state.pending_prompt = "Start Track 1: Introduction to Venture Capital"
    if st.button("Start Track 2: Due Diligence"):
        st.session_state.pending_prompt = "Start Track 2: Due Diligence Process"
with col2:
    if st.button("Start Track 3: Valuation"):
        st.session_state.pending_prompt = "Start Track 3: Valuation Methodologies"
    if st.button("Start Track 4: Term Sheets"):
        st.session_state.pending_prompt = "Start Track 4: Term Sheets"

st.divider()

# ==========================================
# 5. INITIALIZE CHAT HISTORY
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": HIDDEN_SYSTEM_INSTRUCTIONS}
    ]

# Helper to render response text and embed YouTube videos if present
def display_media_content(text):
    st.markdown(text)
    youtube_urls = re.findall(r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[^\s\)]+)', text)
    for url in youtube_urls:
        st.video(url)

# Render past conversation messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                display_media_content(message["content"])
            else:
                st.markdown(message["content"])

# Check if a button triggered a prompt
prompt = st.chat_input("Ask a question or type your prompt...")
if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# ==========================================
# 6. HANDLE CHAT INPUT & API RESPONSE
# ==========================================
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Send system prompt + last 6 messages to save tokens
            MAX_HISTORY = 6
            messages_to_send = [st.session_state.messages[0]] + st.session_state.messages[-MAX_HISTORY:]

            stream = client.chat.completions.create(
                model="sonar",
                messages=messages_to_send,
                stream=True
            )
            response_text = st.write_stream(stream)
            
            # Save response to state
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"API Error: Please check your API key and balance. Details: {e}")
