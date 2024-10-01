import re
import os
from transformers import pipeline

class DataMasker:
    def __init__(self):
        self.rules = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
            'ip': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b'
        }
        self.ner_model = pipeline("ner", model="dslim/bert-base-NER")
        self.masked_entities = {}

    def mask_data(self, text):
        # Mask directory paths
        text = self.mask_directory_paths(text)

        # Rule-based masking
        for key, pattern in self.rules.items():
            text = re.sub(pattern, lambda m: self.get_mask(key, m.group()), text)

        # AI-powered masking
        entities = self.ner_model(text)
        print("Detected entities:", entities)
        
        # Sort entities by start index in descending order to avoid masking issues
        entities.sort(key=lambda x: x['start'], reverse=True)
            
        for entity in entities:
            if entity['entity'].startswith('I-'):  # Check for all entity types
                entity_type = entity['entity'][2:]  # Remove 'I-' prefix
                word = text[entity['start']:entity['end']]
                mask = self.get_mask(entity_type, word)
                text = text[:entity['start']] + mask + text[entity['end']:]

        # Rule-based masking (if you want to keep this)
        for key, pattern in self.rules.items():
            text = re.sub(pattern, lambda m: self.get_mask(key, m.group()), text)

        return text
    def mask_directory_paths(self, text):
        # Pattern to match both Windows and Unix-like paths
        windows_pattern = r'[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*'
        unix_pattern = r'/(?:[^/\s:*?"<>|\r\n]+/)*[^/\s:*?"<>|\r\n]*'
        
        def mask_path(match):
            path = match.group(0)
            # Check if the path contains an email address
            email_match = re.search(self.rules['email'], path)
            if email_match:
                email = email_match.group(0)
                masked_email = self.get_mask('EMAIL', email)
                path = path.replace(email, masked_email)
            return self.get_mask('DIRECTORY', path)

        # Mask Windows paths
        text = re.sub(windows_pattern, mask_path, text)
        # Mask Unix-like paths
        text = re.sub(unix_pattern, mask_path, text)

        return text

    def get_mask(self, entity_type, value):
        key = f"{entity_type}:{value}"
        if key not in self.masked_entities:
            self.masked_entities[key] = f"[{entity_type.upper()}_{len(self.masked_entities)}]"
        return self.masked_entities[key]

    def unmask_response(self, masked_response):
        for key, masked in self.masked_entities.items():
            entity_type, original = key.split(':', 1)
            masked_response = masked_response.replace(masked, original)
        return masked_response
