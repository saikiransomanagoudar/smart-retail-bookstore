# user_proxy_agent.py

import re
from typing import Dict, Any

class UserProxyAgent:
    def __init__(self):
        pass

    def preprocess_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
    
        user_message = message.get('message', '').strip()
        user_message = user_message.strip()
        user_message = self.normalize_unicode(user_message)
        user_message = self.sanitize_input(user_message)
        message['message'] = user_message
        metadata = message.get('metadata', {})

        return message

    def normalize_unicode(self, text: str) -> str:
        import unicodedata
        normalized_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        return normalized_text

    def sanitize_input(self, text: str) -> str:
    
        sanitized_text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)

        return sanitized_text

    def postprocess_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        response_type = response.get('type', '')
        response_content = response.get('response', '')

        if not isinstance(response_content, str):
            response_content = str(response_content)
        response_content = self.sanitize_output(response_content)
        if response_type == 'error':
            response_content = f"Error: {response_content}"
        elif response_type == 'order_confirmation':
            response_content = f"Order Confirmation:\n{response_content}"
        elif response_type == 'out_of_context':
            response_content = f"{response_content}"

        response['response'] = response_content

        return response

    def sanitize_output(self, text: str) -> str:
        sanitized_text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
        sanitized_text = re.sub(r'\s+', ' ', sanitized_text)
        sanitized_text = sanitized_text.strip()

        return sanitized_text

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        
        return self.preprocess_message(state)