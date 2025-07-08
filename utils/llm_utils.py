from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config.settings import settings
import json

class LLMUtils():
    def __init__(self):
        self.llm = ChatOpenAI(
            model = settings.OPENAI_MODEL,
            temperature = settings.TEMPERATURE,
            max_tokens = settings.MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY
        )


    def get_completion(self, system_prompt:str, user_prompt:str) -> str:
        """Get completion from OpenAI using langchain_openai"""
        try: 
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            response = self.llm.invoke(messages)
            return response.content

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise e
    

    def get_json_completion(self, system_prompt: str, user_prompt: str) -> dict:
        """Get JSON completion from OpenAI"""
        try:
            response_text = self.get_completion(system_prompt, user_prompt)
            
            # Clean up response if it has markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON response: {e}")
            raise e
