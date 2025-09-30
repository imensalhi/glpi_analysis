# text_cleaner.py
import re
import string

class TextCleaner:
    def __init__(self):
        # Patterns pour codes techniques (DÉTAILLÉS)
        self.tech_patterns = {
            'error_codes': r'\b(?:0x[0-9A-Fa-f]+|E\d+|P\d+|ERR[-_]?\d+|ERROR\d+)\b',
            'versions': r'\bv?\d+\.\d+(?:\.\d+)*\b',
            'ip_addresses': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'ports': r'\b(?:port\s*)?\d{2,5}\b',
            'file_paths': r'[A-Za-z]:\\(?:[^\\\s]+\\)*[^\\\s]+',
            'urls': r'https?://[^\s]+',
            'server_names': r'\b[A-Z]+-[A-Z]+-\d+\b',
            'mac_addresses': r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',
            'hex_codes': r'\b0x[0-9A-Fa-f]+\b',
            'process_ids': r'\bPID\s*:?\s*\d+\b',
            'memory_addresses': r'\b0x[0-9A-Fa-f]{8,16}\b',
        }
        
        # Abréviations IT courantes
        self.it_abbreviations = {
            'svp', 'stp', 'asap', 'fyi', 'pc', 'pcs', 'os', 'db', 'sql',
            'usb', 'lan', 'wan', 'vpn', 'dns', 'dhcp', 'ip', 'tcp', 'udp',
            'http', 'https', 'ftp', 'smtp', 'imap', 'pop', 'ssl', 'tls',
            'cpu', 'gpu', 'ram', 'rom', 'hdd', 'ssd', 'bios', 'uefi',
            'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt',
            'jpg', 'jpeg', 'png', 'gif', 'mp3', 'mp4', 'avi', 'mkv',
            'zip', 'rar', 'tar', 'gz', 'exe', 'dll', 'bat', 'sh',
            'html', 'css', 'js', 'php', 'py', 'java', 'cpp', 'xml', 'json'
        }
        
        # Mapping chiffres arabes → lettres arabes
        self.arabic_digit_map = {
            '2': 'أ',  # hamza
            '3': 'ع',  # ayn
            '5': 'خ',  # kha
            '6': 'ط',  # ta
            '7': 'ح',  # ha
            '8': 'غ',  # ghayn 
            '9': 'ق',  # qaf
        }
    
    def normalize_text(self, text):
        """Normalisation avancée du texte"""
        if not text:
            return ''
        
        # Supprimer caractères de contrôle
        text = ''.join(char for char in text if char.isprintable())
        
        # Normaliser les espaces
        text = re.sub(r'\s+', ' ', text)
        
        # Normaliser les apostrophes
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('"', '"').replace('"', '"')
        
        return text.strip()
    
    def normalize_tunisian_to_arabic(self, text):
        """Convertir chiffres latins en équivalent arabe pour analyse"""
        normalized = text
        for digit, arabic in self.arabic_digit_map.items():
            normalized = normalized.replace(digit, arabic)
        return normalized
    
    def identify_tech_codes(self, text):
        """Identifier et catégoriser les codes techniques"""
        tech_codes_found = {}
        
        for code_type, pattern in self.tech_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Nettoyer les matches (parfois tuples)
                clean_matches = []
                for match in matches:
                    if isinstance(match, tuple):
                        clean_matches.append(''.join(match))
                    else:
                        clean_matches.append(match)
                tech_codes_found[code_type] = list(set(clean_matches))
        
        return tech_codes_found
    
    def is_tech_code(self, word):
        """Vérifier si un mot est un code technique"""
        # Vérifier abréviations IT
        if word.lower() in self.it_abbreviations:
            return True
        
        # Vérifier patterns techniques
        for pattern in self.tech_patterns.values():
            if re.match(pattern, word, re.IGNORECASE):
                return True
        return False
    
    def get_tech_code_type(self, word):
        """Déterminer le type de code technique"""
        # Vérifier abréviations
        if word.lower() in self.it_abbreviations:
            return 'it_abbreviation'
        
        # Vérifier patterns
        for code_type, pattern in self.tech_patterns.items():
            if re.match(pattern, word, re.IGNORECASE):
                return code_type
        return None
    
    def detect_stuck_words(self, text):
        """Détecter les mots collés (ex: 'bonjourmerci')"""
        # Pattern: alternance minuscule puis majuscule
        stuck_pattern = r'([a-zà-ÿ]+)([A-ZÀ-Ÿ][a-zà-ÿ]+)'
        matches = re.findall(stuck_pattern, text)
        
        if matches:
            return [f"{m[0]} {m[1]}" for m in matches]
        return []