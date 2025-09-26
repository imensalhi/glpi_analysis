# text_cleaner.py
# Nettoyage des textes
import re
import string

class TextCleaner:
    def __init__(self):
        # Patterns pour codes techniques (plus détaillés)
        self.tech_patterns = {
            'error_codes': r'\b(?:0x[0-9A-Fa-f]+|E\d+|P\d+|ERR[-_]\d+|ERROR\d+)\b',
            'versions': r'\bv?\d+\.\d+(?:\.\d+)*(?:\.\d+)*\b',
            'ip_addresses': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'ports': r'\b(?:port\s+)?\d{1,5}\b',
            'file_paths': r'[A-Za-z]:\\(?:[^\\\s]+\\)*[^\\\s]+',
            'urls': r'https?://[^\s]+',
            'server_names': r'\b[A-Z]+-[A-Z]+-\d+\b',
            'mac_addresses': r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',
            'hex_codes': r'\b0x[0-9A-Fa-f]+\b',
            'process_ids': r'\bPID\s*:?\s*\d+\b',
            'memory_addresses': r'\b0x[0-9A-Fa-f]{8,16}\b'
        }
    
    def normalize_text(self, text):
        """Normalisation basique du texte"""
        if not text:
            return ''
        
        # Supprimer caractères de contrôle
        text = ''.join(char for char in text if char.isprintable())
        
        # Normaliser les espaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def identify_tech_codes(self, text):
        """Identifier et catégoriser les codes techniques"""
        tech_codes_found = {}
        
        for code_type, pattern in self.tech_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                tech_codes_found[code_type] = list(set(matches))
        
        return tech_codes_found
    
    def is_tech_code(self, word):
        """Vérifier si un mot est un code technique"""
        for pattern in self.tech_patterns.values():
            if re.match(pattern, word, re.IGNORECASE):
                return True
        return False
    
    def get_tech_code_type(self, word):
        """Déterminer le type de code technique"""
        for code_type, pattern in self.tech_patterns.items():
            if re.match(pattern, word, re.IGNORECASE):
                return code_type
        return None