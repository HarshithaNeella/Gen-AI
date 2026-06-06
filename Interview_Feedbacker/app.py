import streamlit as st

from data.roles import ROLES

from services.gemini_service import (
    generate_question,
    generate_final_report
)

st.set_page_config(
    page_title="AI Interview Feedback Coach",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Interview Feedback Coach")

st.markdown(
    """
Practice role-specific mock interviews powered by Gemini.
"""
)

# -------------------------------
# Session State
# -------------------------------

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

if "question_history" not in st.session_state:
    st.session_state.question_history = []

if "answer_history" not in st.session_state:
    st.session_state.answer_history = []

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "interview_plan" not in st.session_state:
    st.session_state.interview_plan = []

if "final_report" not in st.session_state:
    st.session_state.final_report = ""

# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.header("Interview Setup")

role = st.sidebar.selectbox(
    "Select Role",
    list(ROLES.keys())
)

selected_skills = st.sidebar.multiselect(
    "Select Skills",
    ROLES[role]
)

questions_per_skill = st.sidebar.number_input(
    "Questions Per Skill",
    min_value=1,
    max_value=5,
    value=2
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

# -------------------------------
# Start Interview
# -------------------------------

if st.sidebar.button("Start Interview"):

    if not selected_skills:

        st.warning(
            "Please select at least one skill."
        )

    else:

        st.session_state.interview_started = True

        st.session_state.question_history = []

        st.session_state.answer_history = []

        st.session_state.final_report = ""

        st.session_state.question_index = 0

        interview_plan = []

        for skill in selected_skills:

            for _ in range(
                questions_per_skill
            ):
                interview_plan.append(
                    skill
                )

        st.session_state.interview_plan = (
            interview_plan
        )

        first_skill = interview_plan[0]

        first_question = generate_question(
            role=role,
            skill=first_skill,
            difficulty=difficulty,
            previous_questions=[]
        )

        st.session_state.current_question = (
            first_question
        )

        st.session_state.question_history.append(
            first_question
        )

        st.rerun()

# -------------------------------
# Interview Screen
# -------------------------------

if st.session_state.interview_started:

    total_questions = len(
        st.session_state.interview_plan
    )

    current_index = (
        st.session_state.question_index
    )

    current_skill = (
        st.session_state.interview_plan[
            current_index
        ]
    )

    st.progress(
        (current_index + 1)
        / total_questions
    )

    st.markdown(
        f"### Skill: {current_skill}"
    )

    st.subheader(
        f"Question {current_index + 1} / {total_questions}"
    )

    st.info(
        st.session_state.current_question
    )

    answer = st.text_area(
        "Your Answer",
        height=200
    )

    if st.button("Save & Next"):

        if answer.strip() == "":

            st.warning(
                "Please enter your answer."
            )

        else:

            st.session_state.answer_history.append(
                {
                    "skill": current_skill,
                    "question": st.session_state.current_question,
                    "answer": answer
                }
            )

            # Last Question

            if (
                current_index
                ==
                total_questions - 1
            ):

                st.success(
                    "Interview Completed!"
                )

            else:

                st.session_state.question_index += 1

                next_skill = (
                    st.session_state.interview_plan[
                        st.session_state.question_index
                    ]
                )

                next_question = (
                    generate_question(
                        role=role,
                        skill=next_skill,
                        difficulty=difficulty,
                        previous_questions=
                        st.session_state.question_history
                    )
                )

                st.session_state.current_question = (
                    next_question
                )

                st.session_state.question_history.append(
                    next_question
                )

                st.rerun()

# -------------------------------
# Final Report
# -------------------------------

if (
    st.session_state.interview_started
    and
    len(
        st.session_state.answer_history
    )
    ==
    len(
        st.session_state.interview_plan
    )
):

    st.markdown("---")

    st.subheader(
        "📊 Interview Report"
    )

    if st.button(
        "Generate Final Report"
    ):

        with st.spinner(
            "Generating Report..."
        ):

            report = (
                generate_final_report(
                    role,
                    st.session_state.answer_history
                )
            )

            st.session_state.final_report = (
                report
            )

    if st.session_state.final_report:

        st.markdown(
            st.session_state.final_report
        )
