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
git clone https://github.com/WpythonW/LLMLinguaGroq.git
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

## Dynamic Parameters

The application allows you to adjust key parameters before each new message, providing flexible control over the conversation:

### Adjustable Parameters

1. **Compression Level (0-100)**
   - Controls how much the input message is compressed
   - 0: Maximum compression (empty message)
   - 100: No compression (full message)
   - Useful for managing token usage in long conversations
   - Can be adjusted before each new message

2. **Temperature (0.0-1.0)**
   - Controls response randomness
   - 0.1: More focused, consistent responses
   - 0.7: More creative, varied responses
   - Adjust based on whether you need factual or creative replies
   - Can be changed between messages

3. **System Message**
   - Defines the AI's role and behavior
   - Can be updated at any time
   - Changes take effect with the next message
   - Useful for switching conversation context or AI behavior

All parameters can be adjusted between messages without resetting the chat, allowing you to fine-tune the interaction as the conversation progresses.

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