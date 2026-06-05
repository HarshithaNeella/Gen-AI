import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import pandas as pd


# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="ML Model Analyzer",
    page_icon="📊",
    layout="centered"
)

st.title("Best Model by Classify Groq LLM")

# CHECK API KEY
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()

# CREATE CLIENT
client = Groq(api_key=api_key)



uploaded_file=st.file_uploader("Upload CSV File", type="csv")
if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
csv_text=df.head(10).to_csv(index=False)

# SYSTEM PROMPT


system_prompt = f"""

You are an expert ML engineer.

Use Tree-of-Thought reasoning internally.

Instructions:

1. Identify top 3 promising hyperparameter configurations.
2. Treat each configuration as a separate candidate branch.
3. Group configurations by promising performance ranges.
4. Compare branches using:
   - mean_test_score
   - std_test_score
   - test_r2
   - training_time
   - rank_test_score

5. Evaluate:
   - bias-variance tradeoff
   - stability
   - generalization
   - overfitting risk

6. Eliminate weaker branches.
7. Select the BEST final configuration.

IMPORTANT RESPONSE FORMAT:

Best Hyperparameter Configuration:
<params>

Best Mean Test Score:
<score>

Why It Is Best:
- point 1
- point 2
- point 3

Rejected Alternatives:
- config X rejected because ...
- config Y rejected because ...

Final Recommendation:
<short conclusion>

IMPORTANT:
- Use ONLY configurations from CSV.
- Do NOT invent parameters.
- Keep answer concise.

Hyperparameter Results:

{csv_text}

"""

# GENERATE BUTTON
if st.button("Analyze Hyperparameters"):


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
                        "content": system_prompt
                    }
                ],
                
            )

            result = response.choices[0].message.content

        st.subheader("LLM Analysis")
        st.write(result)
