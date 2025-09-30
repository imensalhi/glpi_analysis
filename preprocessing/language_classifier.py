# language_classifier.py
import re
from collections import Counter

class LanguageClassifier:
    def __init__(self, dictionaries_obj, arabic_detector, text_cleaner):
        self.dictionaries = dictionaries_obj.dictionaries  # Accédez au dict des mots
        self.arabic_detector = arabic_detector
        self.text_cleaner = text_cleaner
        self.letter_freq = dictionaries_obj.letter_frequencies  # Accédez aux fréquences
        
    
    def tokenize(self, text):
        """Tokenisation multilingue avancée"""
        if not text:
            return []
        
        # Normaliser
        text = self.text_cleaner.normalize_text(text)
        
        # Tokenisation incluant apostrophes et chiffres
        tokens = re.findall(r'\b[\w\'\d]+\b', text, re.UNICODE)
        
        return [token for token in tokens if token and len(token) > 0]
    
    def classify_word_with_confidence(self, word):
        """
        NOUVEAU: Classification avec SCORE DE CONFIANCE
        Retourne (langue, score_confiance)
        """
        word_lower = word.lower()
        scores = {
            'french': 0,
            'english': 0,
            'arabic_script': 0,
            'tunisian_latin': 0,
            'technical': 0
        }
        
        # === 1. CODES TECHNIQUES (priorité absolue, score 100) ===
        if self.text_cleaner.is_tech_code(word):
            tech_type = self.text_cleaner.get_tech_code_type(word)
            return (f'tech_{tech_type}' if tech_type else 'tech_general', 100)
        
        # === 2. CARACTÈRES ARABES (score 100) ===
        if self.arabic_detector.has_arabic(word):
            return ('arabic_script', 100)
        
        # === 3. DICTIONNAIRES (score 100 pour match exact) ===
        dict_matches = []
        if word_lower in self.dictionaries['french']:
            scores['french'] = 100
            dict_matches.append('french')
        if word_lower in self.dictionaries['english']:
            scores['english'] = 100
            dict_matches.append('english')
        if word_lower in self.dictionaries['tunisian_latin']:
            scores['tunisian_latin'] = 100
            dict_matches.append('tunisian_latin')
        if word_lower in self.dictionaries['arabic_standard']:
            scores['arabic_script'] = 100
            dict_matches.append('arabic_script')
        
        # Si match unique, retourner immédiatement
        if len(dict_matches) == 1:
            return (dict_matches[0], 100)
        
        # Si plusieurs matches (ex: "change" en français et anglais)
        if len(dict_matches) > 1:
            # Priorité: français > tunisien > anglais
            if 'french' in dict_matches:
                return ('french', 90)  # Légère pénalité pour ambiguïté
            elif 'tunisian_latin' in dict_matches:
                return ('tunisian_latin', 90)
            elif 'english' in dict_matches:
                return ('english', 90)
        
        # === 4. ANALYSE FRÉQUENCE DES LETTRES (score 50-70) ===
        letter_scores = self._analyze_letter_frequency(word_lower)
        for lang, score in letter_scores.items():
            scores[lang] += score
        
        # === 5. PATTERNS LINGUISTIQUES (score 40-60) ===
        pattern_scores = self._analyze_patterns(word_lower)
        for lang, score in pattern_scores.items():
            scores[lang] += score
        
        # === 6. DÉTECTION TUNISIEN PAR CHIFFRES (score 80) ===
        if self._has_tunisian_digits(word):
            scores['tunisian_latin'] += 80
        
        # === 7. DÉTERMINER LANGUE FINALE ===
        max_lang = max(scores, key=scores.get)
        max_score = scores[max_lang]
        
        # Si score trop faible, marquer comme unknown
        if max_score < 30:
            return ('unknown', max_score)
        
        return (max_lang, max_score)
    
    def _analyze_letter_frequency(self, word):
        """Analyser fréquence des lettres caractéristiques"""
        scores = {'french': 0, 'english': 0, 'tunisian_latin': 0}
        
        if len(word) < 3:
            return scores
        
        # Français: accents
        french_accents = self.letter_freq['french']['accents']
        if any(char in french_accents for char in word):
            scores['french'] += 60
        
        # Français: lettres haute fréquence
        french_high = self.letter_freq['french']['high']
        french_ratio = sum(1 for c in word if c in french_high) / len(word)
        scores['french'] += int(french_ratio * 30)
        
        # Anglais: combinaisons typiques
        english_combos = self.letter_freq['english']['typical_combos']
        for combo in english_combos:
            if combo in word:
                scores['english'] += 20
        
        # Tunisien: chiffres caractéristiques
        tunisian_digits = self.letter_freq['tunisian']['key_digits']
        if any(d in word for d in tunisian_digits):
            scores['tunisian_latin'] += 50
        
        return scores
    
    def _analyze_patterns(self, word):
        """Analyser patterns linguistiques"""
        scores = {'french': 0, 'english': 0, 'tunisian_latin': 0}
        
        # Terminaisons françaises
        french_endings = ['tion', 'sion', 'ment', 'ique', 'isme', 'eur', 'euse', 'ation', 'ité', 'age']
        for ending in french_endings:
            if word.endswith(ending):
                scores['french'] += 50
                break
        
        # Terminaisons anglaises
        english_endings = ['ing', 'tion', 'ed', 'er', 'ly', 'ness', 'ful', 'less', 'able', 'ible']
        for ending in english_endings:
            if word.endswith(ending):
                scores['english'] += 50
                break
        
        # Patterns français
        french_patterns = ['qu', 'gu', 'eau', 'eux', 'oux', 'ail', 'euil']
        for pattern in french_patterns:
            if pattern in word:
                scores['french'] += 15
        
        # Patterns anglais
        english_patterns = ['th', 'sh', 'ch', 'ck', 'igh', 'ough']
        for pattern in english_patterns:
            if pattern in word:
                scores['english'] += 15
        
        # Patterns tunisiens
        tunisian_endings = ['ech', 'ch', 'ou', 'a']
        for ending in tunisian_endings:
            if word.endswith(ending) and len(word) > 3:
                scores['tunisian_latin'] += 10
        
        return scores
    
    def _has_tunisian_digits(self, word):
        """Vérifier présence de chiffres arabes latinisés"""
        tunisian_digits = set('379825')
        return any(digit in word for digit in tunisian_digits)
    
    def analyze_text_with_context(self, text):
        """
        NOUVEAU: Analyse avec CONTEXTE (n-grams)
        """
        if not text:
            return self._empty_results()
        
        # Identifier codes techniques
        tech_codes_found = self.text_cleaner.identify_tech_codes(text)
        
        # Tokeniser
        tokens = self.tokenize(text)
        
        if len(tokens) == 0:
            return self._empty_results()
        
        # Classification initiale de chaque mot
        initial_classifications = []
        for token in tokens:
            lang, confidence = self.classify_word_with_confidence(token)
            initial_classifications.append({
                'word': token,
                'language': lang,
                'confidence': confidence,
                'is_technical': lang.startswith('tech_')
            })
        
        # AMÉLIORATION CONTEXTUELLE (tri-grams)
        improved_classifications = self._improve_with_context(initial_classifications)
        
        # Comptage final
        results = self._count_classifications(improved_classifications, tech_codes_found)
        
        return results
    
    def _improve_with_context(self, classifications):
        """Améliorer classification par analyse contextuelle"""
        if len(classifications) < 3:
            return classifications
        
        improved = classifications.copy()
        
        # Analyser par groupes de 3 mots
        for i in range(len(classifications) - 2):
            trigram = classifications[i:i+3]
            
            # Compter langues dans le tri-gram
            lang_counter = Counter()
            for item in trigram:
                if not item['is_technical'] and item['language'] != 'unknown':
                    lang_counter[item['language']] += 1
            
            if len(lang_counter) == 0:
                continue
            
            # Langue dominante dans le tri-gram
            dominant_lang = lang_counter.most_common(1)[0][0]
            dominant_count = lang_counter[dominant_lang]
            
            # Si 2/3 mots sont de la même langue
            if dominant_count >= 2:
                # Réévaluer le mot du milieu s'il est 'unknown' ou faible confiance
                middle_idx = i + 1
                middle_word = improved[middle_idx]
                
                if (middle_word['language'] == 'unknown' or 
                    middle_word['confidence'] < 50) and \
                   not middle_word['is_technical']:
                    # Attribuer la langue dominante avec confiance contextuelle
                    improved[middle_idx]['language'] = dominant_lang
                    improved[middle_idx]['confidence'] = 60  # Confiance contextuelle
                    improved[middle_idx]['context_improved'] = True
        
        return improved
    
    def _count_classifications(self, classifications, tech_codes):
        """Compter les classifications finales"""
        counter = Counter()
        tech_counter = 0
        tech_details = {}
        word_details = []
        confidence_sum = 0
        
        for item in classifications:
            lang = item['language']
            confidence = item['confidence']
            
            if item['is_technical']:
                tech_counter += 1
                tech_type = lang.replace('tech_', '')
                tech_details[tech_type] = tech_details.get(tech_type, 0) + 1
            else:
                counter[lang] += 1
            
            word_details.append(item)
            confidence_sum += confidence
        
        # Calculer confiance moyenne
        avg_confidence = confidence_sum / len(classifications) if classifications else 0
        
        results = {
            'total_words': len(classifications),
            'french': counter.get('french', 0),
            'english': counter.get('english', 0),
            'arabic_script': counter.get('arabic_script', 0),
            'tunisian_latin': counter.get('tunisian_latin', 0),
            'technical_codes': tech_counter,
            'tech_details': tech_details,
            'unknown': counter.get('unknown', 0),
            'word_details': word_details,
            'identified_tech_codes': tech_codes,
            'average_confidence': round(avg_confidence, 2)
        }
        
        return results
    
    def _empty_results(self):
        """Résultats vides"""
        return {
            'total_words': 0,
            'french': 0,
            'english': 0,
            'arabic_script': 0,
            'tunisian_latin': 0,
            'technical_codes': 0,
            'tech_details': {},
            'unknown': 0,
            'word_details': [],
            'identified_tech_codes': {},
            'average_confidence': 0.0
        }
    
    def analyze_text(self, text):
        """Méthode publique - utilise la nouvelle analyse contextuelle"""
        return self.analyze_text_with_context(text)
    
    def calculate_confidence(self, results):
        """Calculer confiance globale"""
        if 'average_confidence' in results:
            return results['average_confidence']
        
        total_words = results['total_words']
        if total_words == 0:
            return 0.0
        
        recognized = total_words - results['unknown']
        confidence = (recognized / total_words) * 100
        
        return round(confidence, 2)