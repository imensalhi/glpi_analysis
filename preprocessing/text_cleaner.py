# text_cleaner.py
import re
import string
# ficheir pour Normalise (supprime contrôles, espaces multiples), extrait/sépare codes techniques via regex (ex. E23 → error_codes).
class TextCleaner:
    def __init__(self):
        # Patterns pour codes techniques
        self.tech_patterns = {
            'error_codes': r'\b(?:0x[0-9A-Fa-f]+|E\d+|P\d+|ERR[-_]\d+)\b',
            'versions': r'\bv?\d+\.\d+(?:\.\d+)*\b',
            'ip_addresses': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'ports': r'\b(?:port\s+)?\d{1,5}\b',
            'file_paths': r'[A-Za-z]:\\(?:[^\\\s]+\\)*[^\\\s]+',
            'urls': r'https?://[^\s]+',
            'server_names': r'\b[A-Z]+-[A-Z]+-\d+\b'
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
    
    def extract_tech_codes(self, text):
        """Extraire les codes techniques"""
        codes = {}
        
        for code_type, pattern in self.tech_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                codes[code_type] = list(set(matches))
        
        return codes
    
    def remove_tech_codes(self, text):
        """Supprimer les codes techniques pour l'analyse linguistique"""
        clean_text = text
        
        for pattern in self.tech_patterns.values():
            clean_text = re.sub(pattern, ' [TECH_CODE] ', clean_text, flags=re.IGNORECASE)
        
        # Nettoyer les espaces multiples
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        return clean_text.strip()