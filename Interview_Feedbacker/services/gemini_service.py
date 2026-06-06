from dotenv import load_dotenv
import os
import logging

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from Prompts.prompts import (
    QUESTION_PROMPT,
    FINAL_REPORT_PROMPT
)

load_dotenv()

logging.basicConfig(
    filename="logs/chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
    max_tokens=1024
)


def generate_question(
    role,
    skill,
    difficulty,
    previous_questions
):

    try:

        prompt = PromptTemplate(
            template=QUESTION_PROMPT,
            input_variables=[
                "role",
                "skill",
                "difficulty",
                "previous_questions"
            ]
        )

        chain = prompt | llm

        response = chain.invoke(
            {
                "role": role,
                "skill": skill,
                "difficulty": difficulty,
                "previous_questions": ", ".join(previous_questions)
            }
        )

        logging.info(
            "Question generated successfully"
        )

        return response.content

    except Exception as e:

        logging.error(
            f"Question generation error: {str(e)}"
        )

        return "Unable to generate question."


def generate_final_report(
    role,
    interview_history
):

    try:

        prompt = PromptTemplate(
            template=FINAL_REPORT_PROMPT,
            input_variables=[
                "role",
                "interview_history"
            ]
        )

        chain = prompt | llm

        response = chain.invoke(
            {
                "role": role,
                "interview_history": str(
                    interview_history
                )
            }
        )

        logging.info(
            "Final report generated successfully"
        )

        return response.content

    except Exception as e:

        logging.error(
            f"Final report error: {str(e)}"
        )

        return (
            "Unable to generate final report."
        )
