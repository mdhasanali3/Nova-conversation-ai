import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class ConversationChain:
    def __init__(self):
        os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
        self.client = genai.Client()
        self.model = "gemini-2.0-flash-exp"
        self.memory = []

        with open('prompts/greeting.txt', 'r') as f:
            self.greeting_prompt = f.read()
        with open('prompts/qualification.txt', 'r') as f:
            self.qualification_prompt = f.read()
        with open('prompts/summary.txt', 'r') as f:
            self.summary_prompt = f.read()

    def add_to_memory(self, role, content):
        self.memory.append({"role": role, "content": content})

    def generate_greeting(self):
        prompt = f"{self.greeting_prompt}\n\nGenerate a warm greeting message."
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        greeting = response.text
        self.add_to_memory("assistant", greeting)
        return greeting

    def ask_question(self, question):
        self.add_to_memory("assistant", question)
        return question

    def save_answer(self, answer):
        self.add_to_memory("user", answer)

    def generate_summary(self, questions, answers):
        conversation_text = ""
        for q, a in zip(questions, answers):
            conversation_text += f"Q: {q}\nA: {a}\n\n"

        prompt = f"""{self.summary_prompt}

Conversation:
{conversation_text}

Create a brief summary for CRM notes."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text

    def generate_lead_json(self, questions, answers, summary):
        prompt = f"""Based on this conversation, generate a JSON lead object with this structure:
{{
  "lead_name": "extract if mentioned, otherwise 'Not provided'",
  "company": "extract if mentioned, otherwise 'Not provided'",
  "qualification": {{
    "problem": "answer to problem question",
    "company_size": "answer to company size question",
    "timeline": "answer to timeline question"
  }},
  "summary": "the summary text"
}}

Questions and Answers:
Q: {questions[0]}
A: {answers[0]}

Q: {questions[1]}
A: {answers[1]}

Q: {questions[2]}
A: {answers[2]}

Summary: {summary}

Output ONLY valid JSON, nothing else."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
