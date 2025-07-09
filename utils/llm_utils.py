# ==================== utils/llm_utils.py ====================
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config.settings import settings
import json
import re

class LLMUtils:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY
        )
    
    def get_completion(self, system_prompt: str, user_prompt: str) -> str:
        """Get completion from OpenAI using langchain_openai"""
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            print(f"❌ Error calling OpenAI API: {e}")
            raise e
    
    def get_json_completion(self, system_prompt: str, user_prompt: str) -> dict:
        """Get JSON completion from OpenAI with robust parsing"""
        try:
            response_text = self.get_completion(system_prompt, user_prompt)
            
            # Clean up response if it has markdown formatting
            cleaned_response = self._clean_json_response(response_text)
            
            # Attempt to parse JSON
            return json.loads(cleaned_response)
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON response: {e}")
            print(f"📝 Raw response excerpt: {response_text[:200]}...")
            
            # Try to extract JSON from the response
            extracted_json = self._extract_json_from_text(response_text)
            if extracted_json:
                try:
                    return json.loads(extracted_json)
                except json.JSONDecodeError:
                    pass
            
            # If all parsing fails, raise the original error
            raise e
    
    def _clean_json_response(self, response_text: str) -> str:
        """Clean JSON response text"""
        # Remove markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()
        
        # Remove any leading/trailing whitespace and newlines
        response_text = response_text.strip()
        
        # Find the first { and last } to extract just the JSON
        start_idx = response_text.find('{')
        if start_idx != -1:
            # For arrays, look for [
            array_start = response_text.find('[')
            if array_start != -1 and array_start < start_idx:
                start_idx = array_start
                end_char = ']'
                end_idx = response_text.rfind(end_char)
            else:
                end_char = '}'
                end_idx = response_text.rfind(end_char)
            
            if end_idx != -1:
                response_text = response_text[start_idx:end_idx + 1]
        
        return response_text
    
    def _extract_json_from_text(self, text: str) -> str:
        """Extract JSON from text using regex"""
        # Try to find JSON object
        json_pattern = r'\{.*\}'
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            return match.group(0)
        
        # Try to find JSON array
        array_pattern = r'\[.*\]'
        match = re.search(array_pattern, text, re.DOTALL)
        if match:
            return match.group(0)
        
        return None