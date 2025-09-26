# arabic_detector.py
# Détection des caractères arabes
import re

class ArabicDetector:
    def __init__(self):
        # Plages Unicode pour l'arabe
        self.arabic_ranges = [
            (0x0600, 0x06FF),  # Arabic
            (0x0750, 0x077F),  # Arabic Supplement
            (0x08A0, 0x08FF),  # Arabic Extended-A
            (0xFB50, 0xFDFF),  # Arabic Presentation Forms-A
            (0xFE70, 0xFEFF),  # Arabic Presentation Forms-B
        ]
    
    def is_arabic_char(self, char):
        """Vérifier si un caractère est arabe"""
        char_code = ord(char)
        return any(start <= char_code <= end for start, end in self.arabic_ranges)
    
    def count_arabic_chars(self, text):
        """Compter les caractères arabes dans un texte"""
        return sum(1 for char in text if self.is_arabic_char(char))
    
    def has_arabic(self, text):
        """Vérifier si le texte contient de l'arabe"""
        return any(self.is_arabic_char(char) for char in text)
    
    def arabic_percentage(self, text):
        """Calculer le pourcentage de caractères arabes"""
        if not text:
            return 0.0
        
        arabic_count = self.count_arabic_chars(text)
        total_chars = len([c for c in text if c.isalnum()])
        
        return (arabic_count / total_chars * 100) if total_chars > 0 else 0.0