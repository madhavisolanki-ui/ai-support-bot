# AI Support Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-RAG-6f42c1.svg)](https://www.llamaindex.ai/)
[![Groq](https://img.shields.io/badge/Groq-LLM-black.svg)](https://groq.com/)
[![GitHub stars](https://img.shields.io/github/stars/madhavisolanki-ui/ai-support-bot?style=flat-square)](https://github.com/madhavisolanki-ui/ai-support-bot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/madhavisolanki-ui/ai-support-bot?style=flat-square)](https://github.com/madhavisolanki-ui/ai-support-bot/network/members)
[![GitHub issues](https://img.shields.io/github/issues/madhavisolanki-ui/ai-support-bot?style=flat-square)](https://github.com/madhavisolanki-ui/ai-support-bot/issues)
[![License](https://img.shields.io/github/license/madhavisolanki-ui/ai-support-bot?style=flat-square)](https://github.com/madhavisolanki-ui/ai-support-bot/blob/main/LICENSE)

An AI-powered internal support chatbot that answers company IT and policy questions using a retrieval-augmented generation workflow.
It uses Streamlit for the UI, LlamaIndex for document retrieval, Hugging Face embeddings for semantic search, and Groq for fast LLM responses.

## Features

- Chat-style Streamlit interface
- Answers grounded in local knowledge-base documents
- Semantic search over internal text files
- Streaming responses for a smoother user experience
- Source document references in answers
- Clean sidebar with quick actions and usage guidance
- Polished, corporate-style interface

## Tech Stack

- Python
- Streamlit
- LlamaIndex
- Groq API
- Hugging Face embeddings
- python-dotenv

## Project Structure

```text
ai-support-bot/
|-- app.py
|-- engine.py
|-- requirements.txt
|-- README.md
|-- .env
|-- data/
|   |-- hr_policy.txt
|   |-- it_policy.txt
|   |-- project_mng.txt
|-- storage/
```

## Screenshots

Add your app screenshots here before publishing on GitHub.

```text
assets/
|-- screenshot-home.png
|-- screenshot-chat.png
```

Example:

```md
![Home view](assets/screenshot-home.png)
```

## Architecture

```mermaid
flowchart TD
    A[User question] --> B[Streamlit UI]
    B --> C[LlamaIndex chat engine]
    C --> D[Retrieve relevant chunks from data/]
    D --> E[Groq LLM]
    E --> F[Answer with source references]
    F --> B
```

## How It Works

1. Documents inside the `data/` folder are loaded.
2. The text is converted into embeddings using `BAAI/bge-small-en-v1.5`.
3. LlamaIndex builds or loads a vector index from `storage/`.
4. When a user asks a question, the most relevant chunks are retrieved.
5. Groq generates a response based on the retrieved context.
6. The app shows the source documents used for the answer.

## Requirements

- Python 3.10 or later
- `GROQ_API_KEY` in a `.env` file
- Internet access for the first embedding model download
- Documents in the `data/` folder

## API Setup

### Groq API

1. Create or sign in to your Groq account.
2. Generate an API key from your Groq dashboard.
3. Add the key to `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Optional Model Setting

You can override the default model by setting:

```env
LLM_MODEL=llama-3.3-70b-versatile
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/madhavisolanki-ui/ai-support-bot.git
cd ai-support-bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and add:

```env
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=llama-3.3-70b-versatile
```

Keep `.env` private and never commit real API keys to version control.

## Run the App

```bash
streamlit run app.py
```

## Example Questions

- How do I reset my password?
- What is the VPN request process?
- Where can I find the leave policy?
- What is the reimbursement process?
- How do I contact HR?

## Troubleshooting

- If the app says the support engine is not ready, check that `GROQ_API_KEY` is set correctly.
- If the knowledge base is empty, make sure there are text files inside the `data/` folder.
- If embeddings fail to load the first time, check your internet connection.
- If you change documents in `data/`, delete the `storage/` folder so the index can rebuild.

## Future Improvements

- File upload support
- Conversation memory
- Authentication for multiple users
- Better source citations
- Chat export

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Madhavi Solanki

B.Tech CSE Student

AI | Data Science | Generative AI
