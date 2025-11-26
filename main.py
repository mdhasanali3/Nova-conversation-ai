import streamlit as st
import json
from chain import ConversationChain
from retriever import ProductRetriever

QUESTIONS = [
    "What problem are you trying to solve?",
    "What is your company size?",
    "What is your timeline to implement the solution?"
]

if 'chain' not in st.session_state:
    st.session_state.chain = ConversationChain()
    st.session_state.retriever = ProductRetriever()
    st.session_state.messages = []
    st.session_state.answers = []
    st.session_state.question_index = 0
    st.session_state.stage = 'greeting'
    st.session_state.lead_json = None

st.title("💬 AI Sales Assistant")

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

if st.session_state.lead_json:
    st.success("✅ Lead Profile Generated!")
    st.json(st.session_state.lead_json)
    if st.button("Start New Conversation"):
        st.session_state.clear()
        st.rerun()
    st.stop()

if st.session_state.stage == 'greeting' and len(st.session_state.messages) == 0:
    greeting = st.session_state.chain.generate_greeting()
    st.session_state.messages.append({'role': 'assistant', 'content': greeting})
    st.session_state.messages.append({'role': 'assistant', 'content': QUESTIONS[0]})
    st.session_state.stage = 'asking'
    st.rerun()

if prompt := st.chat_input("Type your answer..."):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.session_state.chain.save_answer(prompt)

    if st.session_state.stage == 'asking':
        st.session_state.answers.append(prompt)
        st.session_state.question_index += 1

        if st.session_state.question_index < len(QUESTIONS):
            next_question = QUESTIONS[st.session_state.question_index]
            st.session_state.chain.ask_question(next_question)
            st.session_state.messages.append({'role': 'assistant', 'content': next_question})
        else:
            st.session_state.stage = 'summarizing'

    if st.session_state.stage == 'summarizing':
        summary = st.session_state.chain.generate_summary(QUESTIONS, st.session_state.answers)

        rag_context = st.session_state.retriever.get_context(st.session_state.answers)

        closing_message = f"{summary}\n\nLet me prepare your lead profile..."
        st.session_state.messages.append({'role': 'assistant', 'content': closing_message})

        lead_json_text = st.session_state.chain.generate_lead_json(
            QUESTIONS,
            st.session_state.answers,
            summary
        )

        try:
            json_start = lead_json_text.find('{')
            json_end = lead_json_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = lead_json_text[json_start:json_end]
                st.session_state.lead_json = json.loads(json_str)
        except:
            st.session_state.lead_json = {
                "lead_name": "Not provided",
                "company": "Not provided",
                "qualification": {
                    "problem": st.session_state.answers[0],
                    "company_size": st.session_state.answers[1],
                    "timeline": st.session_state.answers[2]
                },
                "summary": summary
            }

        st.session_state.stage = 'complete'

    st.rerun()
