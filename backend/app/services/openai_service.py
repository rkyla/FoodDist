import os
from pydantic import BaseModel
from openai import OpenAI
from typing import List, Type, TypeVar
from dotenv import load_dotenv

T = TypeVar('T', bound=BaseModel)

class OpenAIService:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    def extract_structured_information(self, user_input: str, output_class: Type[T], system_prompt: str) -> T:
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",  # Using a more recent model that supports function calling
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            response_format=output_class,
        )
        
        return completion.choices[0].message.parsed

    def chat_completion(self, prompt, model="gpt-4o-mini"):
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
