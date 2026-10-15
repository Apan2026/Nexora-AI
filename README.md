# Nexora AI

Nexora AI is a Streamlit-based AI assistant powered by Groq models. It supports:

- General chat
- Study help
- Coding assistant
- Math solver
- Writing assistant
- File attachment support for text/PDF files

## Prerequisites

- Python 3.10+
- A Groq API key

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows:
   ```bash
   .\.venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Add your Groq API key to `.env`:
   ```env
   GROQ_API_KEY=your_api_key_here
   GROQ_MODEL=openai/gpt-oss-20b
   ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Project Files

- `app.py` — main Streamlit app
- `requirements.txt` — Python dependencies
- `.env.example` — environment template

## Notes

This app includes a dark theme, chat history management, and a file preview feature for uploaded documents.
