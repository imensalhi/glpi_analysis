# language_dictionaries.py
import json
import os

class LanguageDictionaries:
    def __init__(self):
        self.dictionaries = {
            'french': self.load_french_words(),
            'english': self.load_english_words(),
            'arabic_standard': self.load_arabic_words(),
            'tunisian_latin': self.load_tunisian_latin_words()
        }
    
    def load_french_words(self):
        """Mots français courants"""
        return {
            # Mots de base
            'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
            'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'ou', 'mais',
            'avec', 'sans', 'pour', 'par', 'sur', 'sous', 'dans', 'entre',
            
            # Verbes courants
            'avoir', 'être', 'faire', 'aller', 'voir', 'savoir', 'pouvoir',
            'vouloir', 'venir', 'dire', 'prendre', 'donner', 'mettre',
            'ai', 'as', 'avez', 'avons', 'ont', 'est', 'sont', 'suis',
            
            # Vocabulaire IT français
            'ordinateur', 'imprimante', 'écran', 'clavier', 'souris',
            'problème', 'erreur', 'installation', 'connexion', 'réseau',
            'logiciel', 'programme', 'fichier', 'dossier', 'sauvegarde',
            'mot', 'passe', 'utilisateur', 'compte', 'serveur',
            
            # Expressions courantes
            'bonjour', 'salut', 'merci', 'svp', 'aide', 'urgent',
            'depuis', 'matin', 'hier', 'aujourdhui', 'demain',
            'très', 'bien', 'mal', 'plus', 'moins', 'assez',
            
            # Mots avec apostrophe
            "j'ai", "n'ai", "c'est", "s'il", "qu'il", "d'un"
        }
    
    def load_english_words(self):
        """Mots anglais courants"""
        return {
            # Mots de base
            'i', 'you', 'he', 'she', 'we', 'they', 'it',
            'the', 'a', 'an', 'and', 'or', 'but', 'with', 'without',
            'for', 'by', 'on', 'in', 'at', 'to', 'from',
            
            # Verbes courants
            'be', 'have', 'do', 'will', 'would', 'could', 'should',
            'can', 'may', 'might', 'must', 'go', 'get', 'make',
            'take', 'come', 'see', 'know', 'think', 'want',
            'is', 'are', 'was', 'were', 'been', 'being',
            'has', 'had', 'having', 'does', 'did', 'done',
            
            # Vocabulaire IT anglais
            'computer', 'laptop', 'printer', 'screen', 'monitor',
            'keyboard', 'mouse', 'network', 'internet', 'wifi',
            'error', 'problem', 'issue', 'help', 'support',
            'software', 'hardware', 'system', 'server', 'database',
            'file', 'folder', 'document', 'backup', 'restore',
            'install', 'update', 'upgrade', 'fix', 'repair',
            
            # Expressions courantes
            'hello', 'hi', 'thanks', 'please', 'help', 'urgent',
            'today', 'yesterday', 'tomorrow', 'morning', 'evening',
            'very', 'good', 'bad', 'better', 'best', 'working'
        }
    
    def load_arabic_words(self):
        """Mots arabes courants (script arabe)"""
        return {
            # Mots de base
            'في', 'من', 'إلى', 'على', 'عن', 'مع', 'بعد', 'قبل',
            'هذا', 'هذه', 'ذلك', 'تلك', 'التي', 'الذي', 'ما', 'لا',
            'نعم', 'كلا', 'أو', 'لكن', 'إذا', 'كيف', 'أين', 'متى',
            
            # Pronoms
            'أنا', 'أنت', 'هو', 'هي', 'نحن', 'أنتم', 'هم', 'هن',
            
            # Vocabulaire IT arabe
            'الحاسوب', 'الكمبيوتر', 'الطابعة', 'الشاشة', 'لوحة', 'المفاتيح',
            'الفأرة', 'الشبكة', 'الإنترنت', 'البرنامج', 'النظام',
            'مشكلة', 'خطأ', 'مساعدة', 'دعم', 'تثبيت', 'تحديث',
            'ملف', 'مجلد', 'نسخ', 'احتياطي', 'استعادة',
            
            # Expressions courantes
            'السلام', 'عليكم', 'أهلا', 'مرحبا', 'شكرا', 'من', 'فضلك',
            'اليوم', 'أمس', 'غدا', 'الصباح', 'المساء', 'جدا', 'جيد'
        }
    
    def load_tunisian_latin_words(self):
        """Mots tunisiens en lettres latines (style Facebook)"""
        return {
            # Salutations
            'salam', 'salem', 'ahla', 'kifek', 'kifkom', 'sbah', 'khir',
            'masa', 'labes', 'hamdoulah',
            
            # Pronoms
            '3andi', '3andek', '3andou', '3andha', '3andna', '3andhom',
            'ani', 'enti', 'houa', 'hiya', 'a7na', 'entoma', 'houma',
            
            # Verbes courants
            'nejjem', 'najjem', 'n7eb', 't7eb', 'y7eb', 'bech', 'nak',
            'nkamel', 'na3mel', 'ta3mel', 'ya3mel', 'nrou7', 'tji', 'yji',
            'n7el', 't7el', 'y7el', 'nekhou', 'te5ou', 'ye5ou',
            
            # Mots courants
            'barcha', 'chwaya', 'bech', 'ki', 'wakt', 'lyoum', 'ghodwa',
            'emes', 'tawa', 'ba3d', '9bal', 'kol', 'wa7ed', 'w7da',
            'moch', 'mech', 'chay', '7aja', 'haja',
            
            # Vocabulaire IT tunisien
            'pc', 'ordi', 'ordinateur', 'imprimante', 'ecran', 'clavier',
            'souris', 'internet', 'wifi', 'reseau', 'email', 'password',
            'programme', 'logiciel', 'fichier', 'dossier', 'backup',
            'mochkla', 'problème', 'erreur', 'aide', 'help', 'urgent',
            
            # Expressions mixtes
            'chneya', 'chnowa', 'kifech', 'kifach', 'win', 'wakt',
            'heka', 'hedheka', 'hethi', 'hedhi'
        }