
A lightweight conversational AI workflow that behaves like a helpful SDR (Sales Development Representative).
The system greets website visitors, asks 3 qualification questions, summarizes their answers, and outputs a structured JSON **Lead Object**.

## Features

### 1. Warm Greeting

The AI introduces itself with a friendly SDR persona.

### 2. Asks 3 Qualification Questions

You can configure any set of qualification questions, such as:

1. What problem are you trying to solve?
2. What is your company size?
3. What is your timeline to implement the solution?

### 3. Summarizes Visitor Responses

AI produces a short summary suitable for CRM notes.

### 4. Generates a Structured JSON Lead Object

Example:

```json
{
  "lead_name": "John Doe",
  "company": "TechNova",
  "qualification": {
    "problem": "...",
    "company_size": "...",
    "timeline": "..."
  },
  "summary": "..."
}
```


## Project Structure

```
Nova-conversation-ai
│── main.py                # Orchestrates the conversation flow
│── chain.py               # LLM chain + memory + persona
│── retriever.py           # Optional RAG retriever
│── prompts/
│     ├── greeting.txt
│     ├── qualification.txt
│     ├── summary.txt
│── sample_conversation.md
│── README.md
│── requirements.txt
```

---

## Installation

```bash
git clone https://github.com/mdhasanali3/Nova-conversation-ai
cd Nova-conversation-ai

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```


## Run the Project

```bash
python main.py
```

AI will start a mock conversation in the terminal.

---

## How It Works (Workflow)

1. **Chatbot greets the visitor** using a persona prompt.
2. **Asks question 1 → saves answer**
3. **Asks question 2 → saves answer**
4. **Asks question 3 → saves answer**
5. **Generates summary** using an LLM chain
6. **Generates JSON lead object**
7. **Ends conversation politely**

---

## Sample Conversation

**AI:** Hey there! I’m Nova from the sales team. Happy to help!
What problem are you looking to solve today?

**User:** We want to automate lead scoring.

**AI:** Great! And what’s your team size?

**User:** Around 50 people.

**AI:** Awesome. Final question — when are you planning to deploy a solution?

**User:** Within 2–3 months.

**AI:** Thanks! Let me summarize and prepare your lead profile…

---

## Generated Lead JSON

```json
{
  "lead_name": "Unknown (not provided)",
  "company": "Unknown (not provided)",
  "qualification": {
    "problem": "Automating lead scoring",
    "company_size": "50 employees",
    "timeline": "2–3 months"
  },
  "summary": "The user wants a lead-scoring automation solution for a mid-sized team and plans to implement it within 2–3 months."
}
```
