import requests
from .data_masker import DataMasker
import logging

class SafeGPTProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.masker = DataMasker()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def process_prompt(self, prompt):
        # Mask sensitive data
        self.logger.info(f"Original prompt: {prompt}")
        masked_prompt = self.masker.mask_data(prompt)
        self.logger.info(f"Masked prompt: {masked_prompt}")

        # Send masked prompt to Perplexity API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-sonar-small-128k-chat",  # or another model offered by Perplexity
            "messages": [{"role": "user", "content": masked_prompt}]
        }
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()  # This will raise an exception for HTTP errors

        # Extract and unmask the response
        response_content = response.json()['choices'][0]['message']['content']
        self.logger.info(f"API response: {response_content}")
        unmasked_response = self.unmask_response(response_content)
        self.logger.info(f"Unmasked response: {unmasked_response}")
        return unmasked_response

    def unmask_response(self, masked_response):
        for original, masked in self.masker.masked_entities.items():
            masked_response = masked_response.replace(masked, original)
        return masked_response
