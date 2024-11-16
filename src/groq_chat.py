# groq_chat.py
from typing import List, Dict, Optional, AsyncGenerator
import asyncio
from groq import AsyncGroq
from src.prompt_compressor import PromptCompressorService

class GroqChatService:
    """Asynchronous service for chat interactions with Groq API"""
    def __init__(self, api_key: str):
        self.client = AsyncGroq(api_key=api_key)
        self.compressor = PromptCompressorService()
        self.system_message = "You are a helpful and accurate assistant."
        self.conversation_history: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": self.system_message
            }
        ]
        
    def update_system_message(self, message: str):
        """Update system message without affecting the rest of the history"""
        self.system_message = message
        if self.conversation_history[0]["role"] == "system":
            self.conversation_history[0]["content"] = message
        else:
            self.conversation_history.insert(0, {"role": "system", "content": message})
        
    def reset_conversation(self, system_message: Optional[str] = None):
        """Reset conversation history with optional new system message"""
        self.system_message = system_message or self.system_message
        self.conversation_history = [
            {
                "role": "system",
                "content": self.system_message
            }
        ]
        
    def compress_message(
        self, 
        message: str,
        compression_percent: float = 50
    ) -> Dict[str, any]:
        """Compress single message and return compression data"""
        token_count = len(self.compressor.compressor.tokenizer(message)["input_ids"])
            
        # For the rest cases use compressor
        compressed_data = self.compressor.compress(
            message,
            compression_percent=compression_percent
        )
        
        return {
            "compressed_prompt": compressed_data["compressed_prompt"],
            "stats": {
                "original": token_count,
                "compressed": len(self.compressor.compressor.tokenizer(compressed_data["compressed_prompt"])["input_ids"])
            }
        }
        
    async def get_response(
        self,
        message: str,
        compression_percent: float = 50,
        model: str = "llama3-8b-8192",
        temperature: float = 0.7,
        stream: bool = True
    ) -> AsyncGenerator[str, None]:
        """Get streaming response from Groq API"""
        compressed_data = self.compress_message(
            message,
            compression_percent=compression_percent
        )
        
        # Add message to history
        self.conversation_history.append({
            "role": "user",
            "content": compressed_data["compressed_prompt"]
        })
        
        # Create chat completion request
        stream = await self.client.chat.completions.create(
            messages=self.conversation_history,
            model=model,
            temperature=temperature,
            stream=stream,
            max_tokens=8192
        )
        
        full_response = ""
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                yield content
                
        # Add assistant's response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": full_response
        })