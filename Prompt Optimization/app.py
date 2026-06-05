import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Review Analyzer",
    page_icon="📊",
    layout="centered"
)

st.title("Reviews Classify by Groq LLM")

# CHECK API KEY
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()

# CREATE CLIENT
client = Groq(api_key=api_key)

# SIDEBAR
st.sidebar.title("Settings")

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.5)
max_tokens = st.sidebar.slider("Max Tokens", 1, 2048, 512)

# SYSTEM PROMPT
system_prompt = """
You are an expert sentiment analysis assistant.

Your task is to carefully analyze the given review step-by-step using Chain of Thought reasoning.

Follow these steps internally:

1. Identify all positive sentiment phrases.
2. Identify all negative sentiment phrases.
3. Detect whether the review contains mixed or contradictory opinions.
4. Analyze the overall emotional tone.
5. Decide the final sentiment label.

Sentiment labels:
- Positive
- Negative
- Neutral

Rules:
- If the review mainly contains praise, satisfaction, or happy opinions → Positive
- If the review mainly contains complaints, disappointment, or negative opinions → Negative
- If the review contains both positive and negative opinions OR unclear sentiment → Neutral
'''

Final Sentiment:
Positive / Negative / Neutral

Reason:
Explain clearly why this label was chosen based on the review content.
"""

# INPUT
user_input = st.text_area("Enter Review")

# GENERATE BUTTON
if st.button("Generate Classification"):

    if user_input.strip() == "":
        st.warning("Please enter a review")
    
    else:
        with st.spinner("Analyzing Review..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            result = response.choices[0].message.content

        st.subheader("LLM Response")
        st.write(result)
