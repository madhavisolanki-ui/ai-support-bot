# 🤖 IT Support AI

An AI-powered IT Support chatbot built using Streamlit, LlamaIndex, HuggingFace Embeddings, and Groq API.

The chatbot allows users to ask questions about company policies, documents, and procedures by retrieving information from uploaded documents.

---

## 🚀 Features

- 📄 Document-based Question Answering
- 🔍 Semantic Search using Embeddings
- 🤖 AI-generated responses
- 💬 Chat Interface
- 🧠 Retrieval-Augmented Generation (RAG)
- ⚡ Fast inference with Groq API
- 📂 Supports multiple documents

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LlamaIndex
- Groq API
- HuggingFace Embeddings
- python-dotenv

---

## 📁 Project Structure

```text
ai-support-bot/

│ app.py
│ engine.py
│ .env
│ requirements.txt
│ README.md

├── data/
│   ├── company_policy.pdf
│   ├── employee_handbook.pdf
│   └── leave_policy.pdf
```

---

## ⚙️ How It Works

### Step 1: Load Documents

Documents are stored inside the `data/` folder.

### Step 2: Create Embeddings

The application converts documents into vector embeddings using:

```python
BAAI/bge-small-en-v1.5
```

### Step 3: Build Vector Index

LlamaIndex creates a searchable vector index.

### Step 4: User Asks a Question

Example:

```
How do I reset my password?
```

### Step 5: Retrieve Relevant Information

The system searches the most relevant document chunks.

### Step 6: Generate Response

The Groq LLM generates an answer based on the retrieved information.

---

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/ai-support-bot.git
```

Move to the project folder:

```bash
cd ai-support-bot
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 💡 Example Questions

- How do I reset my password?
- What is the leave policy?
- What are office timings?
- How do I contact HR?
- What are the company holidays?
- What is the reimbursement process?

---

## 🧠 Architecture

```text
Documents
   ↓

LlamaIndex
   ↓

Embeddings
   ↓

Vector Store
   ↓

Retriever
   ↓

Groq LLM
   ↓

Response
```

---

## 📌 Future Improvements

- File upload support
- Multi-user authentication
- Chat export
- Source citations
- Conversation memory

---

## 👩‍💻 Author

Madhavi Solanki

B.Tech CSE Student

AI | Data Science | Generative AI
