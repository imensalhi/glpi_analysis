# language_classifier.py
 # Classification linguistique
import re
from collections import Counter

class LanguageClassifier:
    def __init__(self, dictionaries, arabic_detector, text_cleaner):
        self.dictionaries = dictionaries
        self.arabic_detector = arabic_detector
        self.text_cleaner = text_cleaner
    
    def tokenize(self, text):
        """Tokenisation multilingue"""
        if not text:
            return []
        
        # Normaliser le texte
        text = self.text_cleaner.normalize_text(text)
        
        # Tokenisation basique (espaces et ponctuation)
        tokens = re.findall(r'\b\w+(?:\'\w+)?\b', text, re.UNICODE)
        
        return [token for token in tokens if token]
    
    def classify_word(self, word):
        """Classifier un mot selon sa langue - GARDE LES CODES TECHNIQUES"""
        word_lower = word.lower()
        
        # MODIFICATION: Vérifier les codes techniques EN PREMIER
        # mais les retourner comme catégorie à part
        if self.text_cleaner.is_tech_code(word):
            tech_type = self.text_cleaner.get_tech_code_type(word)
            return f'tech_{tech_type}' if tech_type else 'tech_general'
        
        # Vérifier la présence de caractères arabes
        if self.arabic_detector.has_arabic(word):
            return 'arabic_script'
        
        # Vérifier dans les dictionnaires
        if word_lower in self.dictionaries['french']:
            return 'french'
        elif word_lower in self.dictionaries['english']:
            return 'english'
        elif word_lower in self.dictionaries['tunisian_latin']:
            return 'tunisian_latin'
        elif word_lower in self.dictionaries['arabic_standard']:
            return 'arabic_standard'
        
        # Classification par patterns
        if self.looks_like_french(word):
            return 'french'
        elif self.looks_like_english(word):
            return 'english'
        elif self.looks_like_tunisian_latin(word):
            return 'tunisian_latin'
        
        return 'unknown'
    
    def looks_like_french(self, word):
        """Heuristiques pour détecter le français"""
        french_endings = ['tion', 'sion', 'ment', 'ique', 'isme', 'eur', 'euse']
        french_patterns = ['qu', 'gu', 'eau', 'eux', 'oux']
        
        word_lower = word.lower()
        
        # Terminaisons françaises
        if any(word_lower.endswith(ending) for ending in french_endings):
            return True
        
        # Patterns français
        if any(pattern in word_lower for pattern in french_patterns):
            return True
        
        return False
    
    def looks_like_english(self, word):
        """Heuristiques pour détecter l'anglais"""
        english_endings = ['ing', 'tion', 'ed', 'er', 'ly', 'ness', 'ful']
        english_patterns = ['th', 'sh', 'ch', 'ck']
        
        word_lower = word.lower()
        
        # Terminaisons anglaises
        if any(word_lower.endswith(ending) for ending in english_endings):
            return True
        
        # Patterns anglais
        if any(pattern in word_lower for pattern in english_patterns):
            return True
        
        return False
    
    def looks_like_tunisian_latin(self, word):
        """Heuristiques pour détecter le tunisien latin"""
        tunisian_patterns = ['3', '7', '9', '5', '8', '2', '6']
        tunisian_endings = ['ech', 'ch']
        
        word_lower = word.lower()
        
        # Chiffres utilisés en arabe tunisien
        if any(digit in word_lower for digit in tunisian_patterns):
            return True
        
        # Terminaisons typiques
        if any(word_lower.endswith(ending) for ending in tunisian_endings):
            return True
        
        return False
    
    def analyze_text(self, text):
        """Analyser un texte complet - INCLUT LES CODES TECHNIQUES"""
        if not text:
            return {
                'total_words': 0,
                'french': 0,
                'english': 0,
                'arabic_script': 0,
                'tunisian_latin': 0,
                'technical_codes': 0,  # NOUVEAU: compteur global des codes techniques
                'tech_details': {},    # NOUVEAU: détail par type de code technique
                'unknown': 0,
                'word_details': [],
                'identified_tech_codes': {}  # NOUVEAU: codes techniques trouvés
            }
        
        # Identifier les codes techniques avant tokenisation
        tech_codes_found = self.text_cleaner.identify_tech_codes(text)
        
        # Tokeniser
        tokens = self.tokenize(text)
        
        # Classifier chaque mot
        classification_results = Counter()
        word_details = []
        tech_counter = 0
        tech_details = {}
        
        for token in tokens:
            lang = self.classify_word(token)
            classification_results[lang] += 1
            
            # NOUVEAU: Gérer les codes techniques
            if lang.startswith('tech_'):
                tech_counter += 1
                tech_type = lang.replace('tech_', '')
                if tech_type in tech_details:
                    tech_details[tech_type] += 1
                else:
                    tech_details[tech_type] = 1
            
            word_details.append({
                'word': token,
                'language': lang,
                'is_technical': lang.startswith('tech_')  # NOUVEAU: flag technique
            })
        
        # Préparer les résultats
        results = {
            'total_words': len(tokens),
            'french': classification_results.get('french', 0),
            'english': classification_results.get('english', 0),
            'arabic_script': classification_results.get('arabic_script', 0),
            'tunisian_latin': classification_results.get('tunisian_latin', 0),
            'technical_codes': tech_counter,  # NOUVEAU: total codes techniques
            'tech_details': tech_details,     # NOUVEAU: détail par type
            'unknown': classification_results.get('unknown', 0),
            'word_details': word_details,
            'identified_tech_codes': tech_codes_found  # NOUVEAU: codes identifiés
        }
        
        return results
    
    def calculate_confidence(self, results):
        """Calculer le niveau de confiance de la classification"""
        total_words = results['total_words']
        if total_words == 0:
            return 0.0
        
        # MODIFICATION: Les codes techniques sont maintenant considérés comme "reconnus"
        recognized = total_words - results['unknown']
        confidence = (recognized / total_words) * 100
        
        return round(confidence, 2)