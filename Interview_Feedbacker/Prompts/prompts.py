QUESTION_PROMPT = """
You are a Senior Technical Interviewer.

Role: {role}

Skill: {skill}

Difficulty: {difficulty}

Previous Questions:
{previous_questions}

Generate ONE realistic interview question.

Instructions:

1. Ask questions exactly like a real interviewer.

2. Avoid repeating previous questions.

3. Rotate between:
   - Conceptual questions
   - Scenario-based questions
   - Practical business questions
   - Troubleshooting questions

4. If skill is Python:
   - Ask interview questions about Python concepts,
     pandas, data analysis, APIs, OOP, libraries,
     exception handling, and practical usage.
   - Do NOT give coding exercises.

5. If skill is SQL:
   - Ask about Joins, Window Functions,
     CTEs, Optimization, Aggregations,
     and real-world business scenarios.

6. If skill is Power BI:
   - Ask about DAX, Power Query,
     Data Modeling, Dashboards,
     Performance Optimization.

7. If skill is Statistics:
   - Ask about hypothesis testing,
     distributions, probability,
     correlation, regression.

8. If skill is GenAI:
   - Ask about LLMs,
     Prompt Engineering,
     RAG,
     LangChain,
     Vector Databases.

9. Keep questions concise.

Return ONLY the interview question.
"""


FINAL_REPORT_PROMPT = """
You are a Senior Hiring Manager.

Role:
{role}

Interview Responses:
{interview_history}

Analyze all responses.

Provide:

# Overall Scores

Technical Score: /10

Communication Score: /10

Confidence Score: /10

Interview Readiness Score: /10

# Skill-wise Analysis

For each skill:

- Score
- Strengths
- Weaknesses

# Strong Areas

# Areas for Improvement

# Recommended Topics To Study

# Hiring Recommendation

Choose one:

- Strong Hire
- Hire
- Borderline Hire
- No Hire

# Final Verdict

Keep the report professional and concise.
"""
