# StreamLingua

Chat application with prompt compression using Groq API and LLMLingua.

## Project structure
```
StreamLingua/
├── src/
│   ├── __init__.py
│   ├── prompt_compressor.py
│   └── groq_chat.py
│   
├── models/
│   └── .gitkeep
├── app.py
├── .env
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd StreamLingua
```

2. Create and configure environment variables:
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your API keys
# GROQ_API_KEY=your-groq-api-key-here
```

3. Build and run with Docker:
```bash
docker compose up --build
```

The application will be available at http://localhost:8501

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| GROQ_API_KEY | Your Groq API key | Yes |
| MODEL_NAME | Model to use (default: llama3-8b-8192) | No |

## Development

For local development:
1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```