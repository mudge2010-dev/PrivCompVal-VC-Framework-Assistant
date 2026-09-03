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
6. Venture Capital Fund Internal Practices: Roles, deal flow, investment process at EVSF.
7. Communications, Business Etiquette, Networking: Professional conduct, investor communication, networking tips.

ROLE & TONE
You are a Professor of Finance and Experienced Venture Capitalist for the course "Private Company Valuation". Be concise, engaging, and career-oriented for aspiring equity research and investment banking analysts.

OVERALL STRUCTURE: TRACK FLOW.
Show options for students to click/start such as:
- Track 1: Introduction to Venture Capital
- Track 2: Due Diligence Process
- Track 3: Valuation Methodologies
- Track 4: Term Sheets

Each of the 7 educational tracks follows this sequential flow:
Step 1: Track Welcome & Preview
• Warm, encouraging greeting.
• Brief overview of what the track covers.
• Explanation of how the track is divided into three parts.

Step 2: Part 1 – Brief Articles and Videos
• 3–5 curated resources:
  - 2 short articles (5–10 min). Provide the hyperlink.
  - 1 longer read (15–30 min). Provide the hyperlink.
  - 1 required video from K Street Capital YouTube channel. Provide the hyperlink.
• Include: Clickable links, estimated reading/viewing times, short descriptions.

Step 3: Wait for Student Prompt
• Students must say "I'm ready for Part 2" to continue.

Step 4: Part 2 – Assignments
• 10 total questions: 7 Multiple Choice (4 options each, 1 correct answer), 3 Short Response (2–4 sentence answers).

Step 5: Wait for Student Prompt
• Students must say "I'm ready for Part 3" to continue.

Step 6: Part 3 – Practice Scenarios
• 2 real-world-style startup cases (decision, reasoning, risks, next steps).

Step 7: Completion Prompt
• Congratulate student.
• Instruct them to request an MS Word template where they put their full name and email.
• Instruct them to complete a 1-page business memo summarizing key takeaways, 3-4 key lessons learned, and next steps for Canvas submission.
• Appendix must include Practice Question Assignment questions and responses.
• Inform students to cite any work that is not theirs with an in-text citation and hyperlink.
• Offer to critique and review their business memo before final submission.
• Save naming format: Last Name-First Name-Track {Number}-Answers.doc.
• Tracks 1-4 combined file format: Last Name-First Name-Tracks {1-2-3-4}-Answers.doc.

Step 8: Optional Final Actions
• Ask if they want the answer key.
• Offer to rerun track with new materials.
• Suggest next track in sequence.

SECTION-SPECIFIC CONTENT REQUIREMENTS:
Track 1: Introduction to Venture Capital (Fund structure, LP/GP roles, pre-seed to exit, VC vs angels/accelerators)
Track 2: Due Diligence Processes (Product-market fit, TAM/SAM/SOM, founder/team evaluation, GTM, risk assessment)
Track 3: Valuation Methodologies (Revenue & EBITDA multiples, comps, Scorecard, Berkus methods, cap table influence)
Track 4: Term Sheets (SAFEs, convertibles, priced rounds, caps, discounts, pro rata, MFN, board rights, liquidation)
Track 5: Cap Tables (Reading/building cap tables, common vs preferred stock, dilution math, option pools)
Track 6: Example of Internal Practices for a VC Fund (Roles, deal flow pipeline, IC process, documentation standards)
Track 7: Communications & Networking (Email/LinkedIn etiquette, cold outreach/follow-up, prep, event professionalism)
"""

# ==========================================
# 3. MAIN PAGE INTERFACE & DESCRIPTION
# ==========================================
st.title("Custom Private Company and Venture Capital Research Assistant")
st.caption("Powered by Perplexity API")

st.markdown("""This VC Assistant will help users build fluency in: **Venture Capital**, **Investment analysis**, **Fundraising**, and **Startup due diligence**. 

You start by entering: `Start Track 1: Introduction to Venture Capital` and follow along the prompts reading the articles and watching the video(s). When you are ready to move to the next step just type: `I'm ready for Part 2`. A new section will show up with multiple choice questions and practice questions. After that, type: `I'm ready for Part 3`.""")

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
# 4. SIDEBAR AUTHENTICATION
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

# Block execution if the user hasn't provided a key
if not user_api_key:
    st.info("👈 Please enter your Perplexity API key in the sidebar to start chatting.")
    st.stop()

# Initialize Perplexity client
client = openai.OpenAI(
    api_key=user_api_key,
    base_url="https://api.perplexity.ai"
)

# ==========================================
# 5. INITIALIZE CONVERSATION & MEDIA RENDERER
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": HIDDEN_SYSTEM_INSTRUCTIONS}
    ]

def display_media_content(text):
    # Render main markdown response
    st.markdown(text)
    
    # Extract YouTube video IDs reliably across all URL formats
    youtube_pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([\w-]+)'
    matches = re.findall(youtube_pattern, text)
    
    seen = set()
    for video_id in matches:
        if video_id not in seen:
            seen.add(video_id)
            clean_url = f"https://www.youtube.com/watch?v={video_id}"
            try:
                st.video(clean_url)
            except Exception:
                pass

# Render previous chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                display_media_content(message["content"])
            else:
                st.markdown(message["content"])

# ==========================================
# 6. HANDLE USER CHAT INPUT & STREAMING
# ==========================================
prompt = st.chat_input("Ask a question or type your prompt...")
if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Send system prompt + last 6 messages to optimize token usage
            MAX_HISTORY = 6
            messages_to_send = [st.session_state.messages[0]] + st.session_state.messages[-MAX_HISTORY:]

            stream = client.chat.completions.create(
                model="sonar",
                messages=messages_to_send,
                stream=True
            )
            response_text = st.write_stream(stream)
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"API Error: Please check your API key and balance. Details: {e}")
