FROM huggingface/transformers-torch-light:latest

WORKDIR /app

# Install only required packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/
COPY app.py /app/
COPY .env /app/

# Create and configure models directory
RUN mkdir -p /app/models
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_HOME=/app/models

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]