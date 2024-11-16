# prompt_compressor.py
from llmlingua import PromptCompressor
from typing import List, Optional, Dict

class PromptCompressorService:
    def __init__(
        self,
        model_name: str = "microsoft/llmlingua-2-xlm-roberta-large-meetingbank",
    ):
        self.compressor = PromptCompressor(
            model_name=model_name,
            device_map="cpu",
            use_llmlingua2=True,
        )
    
    def compress(
        self,
        text: str,
        compression_percent: float = 50,
        force_tokens: Optional[List[str]] = None
    ) -> Dict[str, str | int]:
        """
        Simple compression based on percentage. 
        0% = no compression (return original), 
        100% = maximum compression
        """
        original_tokens = self.compressor.tokenizer(text)["input_ids"]
        token_count = len(original_tokens)
        
        # Return original text for 0% compression
        if compression_percent <= 0:
            return {
                "compressed_prompt": '',
                "original_tokens": token_count,
                "compressed_tokens": 2
            }
            
        # Return minimum possible for 100% compression
        if compression_percent >= 100:
            return {
                "compressed_prompt": text,
                "original_tokens": token_count,
                "compressed_tokens": token_count
            }
        
        # Normal compression for values between 0 and 100
        rate = compression_percent / 100
        compressed = self.compressor.compress_prompt(
            text,
            rate=rate,
            force_tokens=force_tokens if force_tokens else ["!", ".", "?", "\n"],
            drop_consecutive=True,
        )
        
        compressed_text = compressed["compressed_prompt"]
        compressed_tokens = self.compressor.tokenizer(compressed_text)["input_ids"]
        
        return {
            "compressed_prompt": compressed_text,
            "original_tokens": token_count,
            "compressed_tokens": len(compressed_tokens)
        }