# language_dictionaries.py
import nltk
from nltk.corpus import words, stopwords

class LanguageDictionaries:
    def __init__(self):
        self.download_nltk_resources()
        self.dictionaries = {
            'french': self.load_french_words(),
            'english': self.load_english_words(),
            'arabic_standard': self.load_arabic_words(),
            'tunisian_latin': self.load_tunisian_latin_words()
        }
        
        # Statistiques de fréquence des lettres par langue
        self.letter_frequencies = self.get_letter_frequencies()
    
    def download_nltk_resources(self):
        """Télécharger NLTK"""
        try:
            nltk.download('words', quiet=True)
            nltk.download('stopwords', quiet=True)
        except:
            pass
    
    def get_letter_frequencies(self):
        """Fréquences caractéristiques des lettres par langue"""
        return {
            'french': {
                'high': set('eatsiunroél'),  # Lettres très fréquentes en français
                'medium': set('dcmpvbfghjqàèùç'),
                'rare': set('kwyxzêîôûëïü'),
                'accents': set('éèêëàâùûîïôçœæ')
            },
            'english': {
                'high': set('etaoinshrdlu'),  # Lettres très fréquentes en anglais
                'medium': set('cmwfgypbvk'),
                'rare': set('jqxz'),
                'typical_combos': ['th', 'he', 'in', 'er', 'an', 'ed', 'ing', 'ion']
            },
            'tunisian': {
                'digits': set('0123456789'),  # Chiffres arabes latinisés
                'key_digits': set('37925'),  # Chiffres les plus caractéristiques
                'typical_combos': ['3a', '7a', '9a', '5a', '2a', 'ch', 'kh']
            }
        }
    
    def load_french_words(self):
        """Dictionnaire français complet avec NLTK"""
        french_set = set()
        
        # NLTK stopwords français
        try:
            french_set.update(stopwords.words('french'))
        except:
            pass
        
        # Dictionnaire manuel massif
        french_manual = {
            # === ARTICLES, PRÉPOSITIONS, CONJONCTIONS ===
            'le', 'la', 'les', 'l', 'un', 'une', 'des', 'du', 'de', 'd', 'au', 'aux',
            'et', 'ou', 'mais', 'donc', 'or', 'ni', 'car', 'soit', 'voire',
            'avec', 'sans', 'pour', 'par', 'sur', 'sous', 'dans', 'entre', 'vers', 'envers',
            'depuis', 'pendant', 'avant', 'après', 'chez', 'contre', 'selon', 'parmi',
            'sauf', 'malgré', 'via', 'hormis', 'outre', 'dès', 'durant',
            
            # === PRONOMS ===
            'je', 'j', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles',
            'me', 'm', 'te', 't', 'se', 's', 'le', 'la', 'les', 'lui', 'leur', 'y', 'en',
            'moi', 'toi', 'soi', 'eux',
            'ce', 'c', 'ceci', 'cela', 'ça', 'cet', 'cette', 'ces',
            'mon', 'ma', 'mes', 'ton', 'ta', 'tes', 'son', 'sa', 'ses',
            'notre', 'nos', 'votre', 'vos', 'leur', 'leurs',
            'qui', 'que', 'qu', 'quoi', 'dont', 'où', 'lequel', 'laquelle', 'lesquels', 'lesquelles',
            'auquel', 'auxquels', 'duquel', 'desquels',
            
            # === ÊTRE (toutes conjugaisons) ===
            'être', 'étant', 'été',
            'suis', 'es', 'est', 'sommes', 'êtes', 'sont',
            'étais', 'était', 'étions', 'étiez', 'étaient',
            'fus', 'fut', 'fûmes', 'fûtes', 'furent',
            'serai', 'seras', 'sera', 'serons', 'serez', 'seront',
            'serais', 'serait', 'serions', 'seriez', 'seraient',
            'sois', 'soit', 'soyons', 'soyez', 'soient',
            'fusse', 'fusses', 'fût', 'fussions', 'fussiez', 'fussent',
            
            # === AVOIR (toutes conjugaisons) ===
            'avoir', 'ayant', 'eu', 'eue', 'eus', 'eues',
            'ai', 'as', 'a', 'avons', 'avez', 'ont',
            'avais', 'avait', 'avions', 'aviez', 'avaient',
            'eus', 'eut', 'eûmes', 'eûtes', 'eurent',
            'aurai', 'auras', 'aura', 'aurons', 'aurez', 'auront',
            'aurais', 'aurait', 'aurions', 'auriez', 'auraient',
            'aie', 'aies', 'ait', 'ayons', 'ayez', 'aient',
            'eusse', 'eusses', 'eût', 'eussions', 'eussiez', 'eussent',
            
            # === FAIRE (toutes formes) ===
            'faire', 'faisant', 'fait', 'faite', 'faits', 'faites',
            'fais', 'fait', 'faisons', 'faites', 'font',
            'faisais', 'faisait', 'faisions', 'faisiez', 'faisaient',
            'fis', 'fit', 'fîmes', 'fîtes', 'firent',
            'ferai', 'feras', 'fera', 'ferons', 'ferez', 'feront',
            'ferais', 'ferait', 'ferions', 'feriez', 'feraient',
            'fasse', 'fasses', 'fasse', 'fassions', 'fassiez', 'fassent',
            'refaire', 'défaire', 'satisfaire', 'refait', 'défait',
            
            # === ALLER ===
            'aller', 'allant', 'allé', 'allée', 'allés', 'allées',
            'vais', 'vas', 'va', 'allons', 'allez', 'vont',
            'allais', 'allait', 'allions', 'alliez', 'allaient',
            'allai', 'alla', 'allâmes', 'allâtes', 'allèrent',
            'irai', 'iras', 'ira', 'irons', 'irez', 'iront',
            'irais', 'irait', 'irions', 'iriez', 'iraient',
            'aille', 'ailles', 'aille', 'allions', 'alliez', 'aillent',
            
            # === AUTRES VERBES FRÉQUENTS ===
            'voir', 'vois', 'voit', 'voyons', 'voyez', 'voient', 'voyais', 'voyait', 'vu', 'vue', 'vus', 'vues',
            'savoir', 'sais', 'sait', 'savons', 'savez', 'savent', 'savais', 'savait', 'su', 'sue', 'sus', 'sues',
            'pouvoir', 'peux', 'peut', 'pouvons', 'pouvez', 'peuvent', 'pouvais', 'pouvait', 'pu', 'pourrai', 'pourrais',
            'vouloir', 'veux', 'veut', 'voulons', 'voulez', 'veulent', 'voulais', 'voulait', 'voulu', 'voudrai', 'voudrais',
            'venir', 'viens', 'vient', 'venons', 'venez', 'viennent', 'venais', 'venait', 'venu', 'venue', 'venus', 'venues',
            'dire', 'dis', 'dit', 'disons', 'dites', 'disent', 'disais', 'disait', 'dit', 'dite', 'dits', 'dites',
            'prendre', 'prends', 'prend', 'prenons', 'prenez', 'prennent', 'prenais', 'prenait', 'pris', 'prise', 'prit',
            'donner', 'donne', 'donnes', 'donnons', 'donnez', 'donnent', 'donnais', 'donnait', 'donné', 'donnée', 'donnés',
            'mettre', 'mets', 'met', 'mettons', 'mettez', 'mettent', 'mettais', 'mettait', 'mis', 'mise', 'mit',
            'partir', 'pars', 'part', 'partons', 'partez', 'partent', 'partais', 'partait', 'parti', 'partie', 'partis',
            'trouver', 'trouve', 'trouves', 'trouvons', 'trouvez', 'trouvent', 'trouvé', 'trouvée', 'trouvés', 'trouvées',
            'passer', 'passe', 'passes', 'passons', 'passez', 'passent', 'passé', 'passée', 'passés', 'passées',
            'comprendre', 'comprends', 'comprend', 'comprenons', 'comprenez', 'comprennent', 'compris', 'comprise',
            'rester', 'reste', 'restes', 'restons', 'restez', 'restent', 'resté', 'restée', 'restés', 'restées',
            'arriver', 'arrive', 'arrives', 'arrivons', 'arrivez', 'arrivent', 'arrivé', 'arrivée', 'arrivés', 'arrivées',
            'demander', 'demande', 'demandes', 'demandons', 'demandez', 'demandent', 'demandé', 'demandée',
            'essayer', 'essaie', 'essaies', 'essayons', 'essayez', 'essaient', 'essayé', 'essayée',
            'marcher', 'marche', 'marches', 'marchons', 'marchez', 'marchent', 'marché', 'marchée',
            'fonctionner', 'fonctionne', 'fonctionnes', 'fonctionnons', 'fonctionnez', 'fonctionnent', 'fonctionné',
            'utiliser', 'utilise', 'utilises', 'utilisons', 'utilisez', 'utilisent', 'utilisé', 'utilisée',
            'cliquer', 'clique', 'cliques', 'cliquons', 'cliquez', 'cliquent', 'cliqué', 'cliquée',
            'taper', 'tape', 'tapes', 'tapons', 'tapez', 'tapent', 'tapé', 'tapée',
            'chercher', 'cherche', 'cherches', 'cherchons', 'cherchez', 'cherchent', 'cherché', 'cherchée',
            'attendre', 'attends', 'attend', 'attendons', 'attendez', 'attendent', 'attendu', 'attendue',
            'répondre', 'réponds', 'répond', 'répondons', 'répondez', 'répondent', 'répondu', 'répondue',
            'ouvrir', 'ouvre', 'ouvres', 'ouvrons', 'ouvrez', 'ouvrent', 'ouvert', 'ouverte',
            'fermer', 'ferme', 'fermes', 'fermons', 'fermez', 'ferment', 'fermé', 'fermée',
            'afficher', 'affiche', 'affiches', 'affichons', 'affichez', 'affichent', 'affiché', 'affichée',
            'envoyer', 'envoie', 'envoies', 'envoyons', 'envoyez', 'envoient', 'envoyé', 'envoyée',
            'recevoir', 'reçois', 'reçoit', 'recevons', 'recevez', 'reçoivent', 'reçu', 'reçue',
            'charger', 'charge', 'charges', 'chargeons', 'chargez', 'chargent', 'chargé', 'chargée',
            'démarrer', 'démarre', 'démarres', 'démarrons', 'démarrez', 'démarrent', 'démarré', 'démarrée',
            
            # === VOCABULAIRE IT FRANÇAIS MASSIF ===
            'ordinateur', 'ordinateurs', 'pc', 'pcs', 'bureau', 'bureaux', 'poste', 'postes',
            'imprimante', 'imprimantes', 'imprimer', 'impression', 'impressions', 'imprimé', 'imprimée',
            'scanner', 'scanners', 'numériser', 'numériseur', 'scan', 'scans',
            'écran', 'écrans', 'moniteur', 'moniteurs', 'affichage', 'affichages',
            'clavier', 'claviers', 'touche', 'touches', 'raccourci', 'raccourcis',
            'souris', 'pointeur', 'curseur', 'clic', 'clics', 'double-clic',
            'problème', 'problèmes', 'souci', 'soucis', 'panne', 'pannes', 'bug', 'bugs', 'bogue', 'bogues',
            'erreur', 'erreurs', 'défaut', 'défauts', 'dysfonctionnement', 'dysfonctionnements',
            'installation', 'installations', 'installer', 'installé', 'installée', 'désinstaller', 'désinstallé',
            'connexion', 'connexions', 'connecter', 'connecté', 'connectée', 'déconnexion', 'déconnecté',
            'réseau', 'réseaux', 'internet', 'wifi', 'ethernet', 'câble', 'câbles', 'filaire', 'sans-fil',
            'logiciel', 'logiciels', 'programme', 'programmes', 'application', 'applications', 'appli', 'applis',
            'fichier', 'fichiers', 'dossier', 'dossiers', 'répertoire', 'répertoires', 'document', 'documents',
            'sauvegarde', 'sauvegardes', 'backup', 'backups', 'copie', 'copies', 'duplication',
            'restauration', 'restaurer', 'restauré', 'restaurée', 'récupération', 'récupérer',
            'mise', 'jour', 'update', 'updates', 'mettre', 'version', 'versions', 'patch', 'patchs',
            'serveur', 'serveurs', 'client', 'clients', 'base', 'données', 'donnée', 'data',
            'système', 'systèmes', 'exploitation', 'windows', 'linux', 'ubuntu', 'debian', 'macos', 'mac',
            'mot', 'passe', 'password', 'mdp', 'identifiant', 'identifiants', 'login',
            'compte', 'comptes', 'utilisateur', 'utilisateurs', 'user', 'profil', 'profils', 'session', 'sessions',
            'messagerie', 'email', 'emails', 'mail', 'mails', 'courrier', 'courriel', 'courriels',
            'outlook', 'thunderbird', 'gmail', 'webmail', 'imap', 'pop', 'smtp',
            'navigateur', 'navigateurs', 'firefox', 'chrome', 'explorer', 'safari', 'edge', 'brave',
            'site', 'sites', 'web', 'page', 'pages', 'lien', 'liens', 'url', 'urls', 'adresse',
            'antivirus', 'firewall', 'pare-feu', 'sécurité', 'protection', 'virus', 'malware', 'trojan',
            'disque', 'disques', 'dur', 'durs', 'ssd', 'hdd', 'partition', 'partitions',
            'mémoire', 'ram', 'vive', 'processeur', 'cpu', 'puce', 'core', 'cores',
            'carte', 'cartes', 'graphique', 'graphiques', 'vidéo', 'son', 'audio', 'réseau',
            'port', 'ports', 'usb', 'hdmi', 'vga', 'displayport', 'thunderbolt', 'jack',
            'bluetooth', 'wifi', 'nfc', 'infrarouge', 'sans-fil', 'wireless',
            'pilote', 'pilotes', 'driver', 'drivers', 'firmware', 'bios', 'uefi',
            'périphérique', 'périphériques', 'matériel', 'hardware', 'composant', 'composants',
            'plantage', 'crash', 'crashe', 'crashé', 'freeze', 'gel', 'geler', 'gelé', 'figé',
            'blocage', 'bloqué', 'bloquée', 'bloque', 'lent', 'lente', 'lenteur', 'lenteurs', 'ralenti',
            'redémarrage', 'restart', 'reboot', 'redémarrer', 'redémarré', 'relancer',
            'arrêt', 'shutdown', 'éteindre', 'éteint', 'éteinte', 'extinction',
            'veille', 'hibernation', 'suspendre', 'suspendu', 'suspendue', 'mise-en-veille',
            'téléchargement', 'télécharger', 'téléchargé', 'download', 'downloads', 'téléchargements',
            'upload', 'téléverser', 'téléversement', 'envoi', 'envoyer',
            'partage', 'partagé', 'partagée', 'dossiers-partagés', 'réseau-partagé',
            'accès', 'autorisations', 'droits', 'permission', 'permissions', 'admin', 'administrateur',
            'config', 'configuration', 'configurations', 'paramètre', 'paramètres', 'réglage', 'réglages',
            'échoué', 'échouée', 'échec', 'échecs', 'réussi', 'réussie', 'succès', 'réussite',
            'actif', 'active', 'inactif', 'inactive', 'activé', 'activée', 'désactivé', 'désactivée',
            'disponible', 'indisponible', 'accessible', 'inaccessible', 'connecté', 'déconnecté',
            'valide', 'invalide', 'correct', 'incorrect', 'erroné', 'faux', 'vrai',
            'lancer', 'lancé', 'lancée', 'exécuter', 'exécuté', 'exécutée', 'démarrer', 'démarré',
            'stopper', 'stoppé', 'arrêter', 'arrêté', 'terminer', 'terminé', 'finir', 'fini',
            'créer', 'créé', 'créée', 'création', 'supprimer', 'supprimé', 'supprimée', 'suppression',
            'modifier', 'modifié', 'modifiée', 'modification', 'éditer', 'édité', 'édition',
            'copier', 'copié', 'copiée', 'coller', 'collé', 'couper', 'coupé',
            'renommer', 'renommé', 'renommée', 'déplacer', 'déplacé', 'déplacée','message'
            
            # === EXPRESSIONS COURANTES ===
            'bonjour', 'bonsoir', 'bonne', 'journée', 'salut', 'coucou', 'hey',
            'merci', 'remerciements', 'svp', 'sil', 'plaît', 'plait', 'stp',
            'aide', 'aidez', 'aider', 'aidé', 'assistance', 'support', 'dépannage',
            'urgent', 'urgence', 'rapide', 'rapidement', 'vite', 'lent', 'lentement',
            'depuis', 'matin', 'midi', 'après-midi', 'soir', 'nuit', 'journée', 'soirée',
            'hier', 'aujourdhui', 'aujourd-hui', 'demain', 'semaine', 'mois', 'année',
            'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche',
            'toujours', 'jamais', 'parfois', 'souvent', 'rarement', 'encore', 'déjà',
            'très', 'assez', 'trop', 'plus', 'moins', 'beaucoup', 'peu', 'plusieurs',
            'bien', 'mal', 'mieux', 'pire', 'meilleur', 'meilleure', 'bon', 'bonne', 'mauvais', 'mauvaise',
            'possible', 'impossible', 'facile', 'difficile', 'simple', 'compliqué', 'complexe',
            'nouveau', 'nouvelle', 'neuf', 'neuve', 'vieux', 'vieille', 'ancien', 'ancienne',
            'comment', 'quand', 'pourquoi', 'combien', 'où', 'quel', 'quelle', 'quels', 'quelles',
            'oui', 'non', 'si', 'peut-être', 'certainement', 'sûrement', 'évidemment',
            
            # === MOTS AVEC APOSTROPHE ===
            "j'ai", "j'avais", "j'aurai", "j'aurais", "j'étais", "j'irai", "j'irais",
            "n'ai", "n'avais", "n'est", "n'était", "n'ont", "n'avaient",
            "c'est", "c'était", "c'était", "c'était", "c'étaient",
            "s'il", "s'ils", "s'est", "s'était", "s'étaient",
            "qu'il", "qu'ils", "qu'elle", "qu'elles", "qu'est", "qu'était",
            "d'un", "d'une", "d'autres", "d'abord", "d'accord", "aujourd'hui",
            "l'ordinateur", "l'écran", "l'imprimante", "l'erreur", "l'application",
            "l'utilisateur", "l'internet", "l'installation", "l'email",
            "m'aider", "t'aider", "m'envoyer", "t'envoyer",
            
            # === NOMBRES ===
            'zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept',
            'huit', 'neuf', 'dix', 'onze', 'douze', 'treize', 'quatorze',
            'quinze', 'seize', 'vingt', 'trente', 'quarante', 'cinquante',
            'soixante', 'cent', 'mille', 'million', 'milliard',
            'premier', 'première', 'deuxième', 'second', 'seconde', 'troisième',
            
            # === ADJECTIFS COURANTS ===
            'petit', 'petite', 'petits', 'petites', 'grand', 'grande', 'grands', 'grandes',
            'gros', 'grosse', 'long', 'longue', 'court', 'courte', 'haut', 'haute', 'bas', 'basse',
            'autre', 'autres', 'même', 'mêmes', 'tout', 'toute', 'tous', 'toutes',
            'chaque', 'certain', 'certaine', 'certains', 'certaines',
            'aucun', 'aucune', 'nul', 'nulle', 'quelque', 'quelques',
            'propre', 'sale', 'neuf', 'vieux', 'jeune', 'âgé',
            
            # === NÉGATIONS ===
            'ne', 'n', 'pas', 'plus', 'jamais', 'rien', 'personne', 'aucun', 'nul', 'guère',
            
            # === ADVERBES ===
            'ici', 'là', 'là-bas', 'partout', 'nulle-part', 'ailleurs',
            'maintenant', 'alors', 'ensuite', 'puis', 'enfin', 'dabord',
            'rapidement', 'lentement', 'facilement', 'difficilement',
            'vraiment', 'certainement', 'probablement', 'peut-être',
            'tellement', 'vraiment', 'complètement', 'totalement',
        }
        
        french_set.update(french_manual)
        
        # Ajouter variations automatiques
        french_set.update(self._generate_french_variations(french_manual))
        
        return french_set
    
    def _generate_french_variations(self, base_words):
        """Générer variations françaises automatiques"""
        variations = set()
        
        for word in base_words:
            if len(word) < 3:
                continue
                
            # Pluriels
            if not word.endswith('s') and not word.endswith('x') and not word.endswith('z'):
                variations.add(word + 's')
            if word.endswith('au') or word.endswith('eu') or word.endswith('ou'):
                variations.add(word + 'x')
            if word.endswith('al'):
                variations.add(word[:-2] + 'aux')
            
            # Féminins
            if word.endswith('eur'):
                variations.add(word[:-3] + 'euse')
            if word.endswith('if'):
                variations.add(word[:-2] + 'ive')
            if not word.endswith('e'):
                variations.add(word + 'e')
        
        return variations
    
    def load_english_words(self):
        """Dictionnaire anglais massif avec NLTK"""
        english_set = set()
        
        # NLTK dictionary
        try:
            english_set.update(w.lower() for w in words.words())
            english_set.update(stopwords.words('english'))
        except:
            pass
        
        # Manuel IT étendu
        english_manual = {
            # === ARTICLES, PREPOSITIONS ===
            'the', 'a', 'an', 'and', 'or', 'but', 'with', 'without', 'nor', 'yet', 'so',
            'for', 'by', 'on', 'in', 'at', 'to', 'from', 'about', 'of', 'off',
            'into', 'onto', 'through', 'throughout', 'during', 'before', 'after',
            'above', 'below', 'over', 'under', 'up', 'down', 'between', 'among',
            'across', 'along', 'around', 'behind', 'beside', 'near', 'towards',
            
            # === PRONOUNS ===
            'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them',
            'my', 'mine', 'your', 'yours', 'his', 'hers', 'its', 'our', 'ours', 'their', 'theirs',
            'this', 'that', 'these', 'those',
            'who', 'whom', 'whose', 'what', 'which', 'where', 'when', 'why', 'how',
            'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves',
            
            # === BE (all forms) ===
            'be', 'am', 'is', 'are', 'was', 'were', 'been', 'being',
            'ain\'t', 'isn\'t', 'aren\'t', 'wasn\'t', 'weren\'t',
            
            # === HAVE (all forms) ===
            'have', 'has', 'had', 'having', 'haven\'t', 'hasn\'t', 'hadn\'t',
            
            # === DO (all forms) ===
            'do', 'does', 'did', 'done', 'doing', 'don\'t', 'doesn\'t', 'didn\'t',
            
            # === MODAL VERBS ===
            'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must',
            'shall', 'ought', 'won\'t', 'wouldn\'t', 'couldn\'t', 'shouldn\'t',
            'can\'t', 'cannot', 'mustn\'t',
            
            # === COMMON VERBS (all forms) ===
            'go', 'goes', 'went', 'gone', 'going',
            'get', 'gets', 'got', 'gotten', 'getting',
            'make', 'makes', 'made', 'making',
            'take', 'takes', 'took', 'taken', 'taking',
            'come', 'comes', 'came', 'coming',
            'see', 'sees', 'saw', 'seen', 'seeing',
            'know', 'knows', 'knew', 'known', 'knowing',
            'think', 'thinks', 'thought', 'thinking',
            'want', 'wants', 'wanted', 'wanting',
            'use', 'uses', 'used', 'using',
            'work', 'works', 'worked', 'working',
            'try', 'tries', 'tried', 'trying',
            'need', 'needs', 'needed', 'needing',
            'find', 'finds', 'found', 'finding',
            'give', 'gives', 'gave', 'given', 'giving',
            'tell', 'tells', 'told', 'telling',
            'ask', 'asks', 'asked', 'asking',
            'start', 'starts', 'started', 'starting',
            'stop', 'stops', 'stopped', 'stopping',
            'run', 'runs', 'ran', 'running',
            'open', 'opens', 'opened', 'opening',
            'close', 'closes', 'closed', 'closing',
            'show', 'shows', 'showed', 'shown', 'showing',
            'call', 'calls', 'called', 'calling',
            'keep', 'keeps', 'kept', 'keeping',
            'move', 'moves', 'moved', 'moving',
            'turn', 'turns', 'turned', 'turning',
            'bring', 'brings', 'brought', 'bringing',
            'write', 'writes', 'wrote', 'written', 'writing',
            'read', 'reads', 'reading',
            'change', 'changes', 'changed', 'changing',
            'click', 'clicks', 'clicked', 'clicking',
            'type', 'types', 'typed', 'typing',
            'send', 'sends', 'sent', 'sending',
            'receive', 'receives', 'received', 'receiving',
            'load', 'loads', 'loaded', 'loading',
            'save', 'saves', 'saved', 'saving',
            'delete', 'deletes', 'deleted', 'deleting',
            'remove', 'removes', 'removed', 'removing',
            'add', 'adds', 'added', 'adding',
            'create', 'creates', 'created', 'creating',
            'install', 'installs', 'installed', 'installing',
            'uninstall', 'uninstalls', 'uninstalled', 'uninstalling',
            'update', 'updates', 'updated', 'updating',
            'upgrade', 'upgrades', 'upgraded', 'upgrading',
            'downgrade', 'downgrades', 'downgraded', 'downgrading',
            'fix', 'fixes', 'fixed', 'fixing',
            'repair', 'repairs', 'repaired', 'repairing',
            'connect', 'connects', 'connected', 'connecting',
            'disconnect', 'disconnects', 'disconnected', 'disconnecting',
            'log', 'logs', 'logged', 'logging',
            'login', 'logins',
            'logout', 'logouts',
            'reboot', 'reboots', 'rebooted', 'rebooting',
            'restart', 'restarts', 'restarted', 'restarting',
            'shutdown', 'shutdowns',
            'crash', 'crashes', 'crashed', 'crashing',
            'freeze', 'freezes', 'froze', 'frozen', 'freezing',
            'hang', 'hangs', 'hung', 'hanging',
            
            # === IT VOCABULARY MASSIVE ===
            'computer', 'computers', 'pc', 'pcs', 'laptop', 'laptops', 'notebook', 'notebooks',
            'desktop', 'desktops', 'workstation', 'workstations', 'tower', 'towers',
            'printer', 'printers', 'print', 'printing', 'printed', 'printout', 'printouts',
            'scanner', 'scanners', 'scan', 'scans', 'scanned', 'scanning',
            'screen', 'screens', 'monitor', 'monitors', 'display', 'displays',
            'keyboard', 'keyboards', 'key', 'keys', 'keypad', 'keypads',
            'mouse', 'mice', 'pointer', 'cursor', 'trackpad', 'touchpad',
            'network', 'networks', 'internet', 'intranet', 'extranet',
            'wifi', 'wi-fi', 'ethernet', 'lan', 'wan', 'vpn',
            'cable', 'cables', 'wire', 'wires', 'wireless', 'wired',
            'connection', 'connections', 'connect', 'connected', 'connecting',
            'disconnect', 'disconnected', 'disconnecting', 'disconnection',
            'error', 'errors', 'problem', 'problems', 'issue', 'issues',
            'bug', 'bugs', 'crash', 'crashes', 'failure', 'failures',
            'help', 'support', 'assistance', 'assist', 'tech-support', 'helpdesk',
            'software', 'program', 'programs', 'application', 'applications',
            'app', 'apps', 'tool', 'tools', 'utility', 'utilities',
            'hardware', 'device', 'devices', 'equipment', 'peripheral', 'peripherals',
            'system', 'systems', 'operating', 'os',
            'windows', 'linux', 'ubuntu', 'debian', 'centos', 'redhat',
            'mac', 'macos', 'osx', 'unix', 'dos',
            'server', 'servers', 'client', 'clients', 'host', 'hosts',
            'database', 'databases', 'db', 'sql', 'mysql', 'postgresql', 'oracle',
            'data', 'table', 'tables', 'record', 'records', 'field', 'fields',
            'file', 'files', 'folder', 'folders', 'directory', 'directories',
            'document', 'documents', 'doc', 'docs', 'pdf', 'txt',
            'backup', 'backups', 'restore', 'restored', 'restoring', 'restoration',
            'save', 'saved', 'saving', 'autosave',
            'download', 'downloaded', 'downloading', 'downloads',
            'upload', 'uploaded', 'uploading', 'uploads',
            'install', 'installation', 'installed', 'installing', 'installer',
            'uninstall', 'uninstalled', 'uninstalling', 'uninstaller',
            'update', 'updated', 'updating', 'upgrade', 'upgraded', 'upgrading',
            'version', 'versions', 'release', 'releases', 'build', 'builds',
            'patch', 'patches', 'patched', 'patching', 'hotfix', 'hotfixes',
            'user', 'users', 'username', 'usernames',
            'account', 'accounts', 'profile', 'profiles',
            'password', 'passwords', 'pass', 'passphrase', 'pin', 'code',
            'login', 'logout', 'logon', 'logoff', 'signin', 'signout',
            'email', 'emails', 'e-mail', 'mail', 'mails',
            'outlook', 'gmail', 'yahoo', 'thunderbird', 'webmail',
            'message', 'messages', 'inbox', 'outbox', 'sent', 'draft', 'spam',
            'attachment', 'attachments', 'attach', 'attached',
            'browser', 'browsers', 'firefox', 'chrome', 'safari', 'edge', 'explorer', 'ie', 'opera', 'brave',
            'website', 'websites', 'site', 'sites', 'webpage', 'webpages', 'page', 'pages',
            'url', 'urls', 'link', 'links', 'hyperlink', 'hyperlinks',
            'search', 'google', 'bing', 'yahoo', 'searches', 'searched', 'searching',
            'antivirus', 'anti-virus', 'firewall', 'security', 'protection',
            'virus', 'viruses', 'malware', 'spyware', 'adware', 'ransomware',
            'trojan', 'trojans', 'worm', 'worms', 'rootkit', 'phishing',
            'memory', 'ram', 'rom', 'cache', 'buffer',
            'disk', 'drive', 'drives', 'hard-drive', 'harddrive', 'hdd', 'ssd',
            'storage', 'capacity', 'space', 'gigabyte', 'terabyte', 'gb', 'tb', 'mb',
            'processor', 'cpu', 'core', 'cores', 'multicore', 'dual-core', 'quad-core',
            'graphics', 'gpu', 'video-card', 'videocard',
            'card', 'cards', 'motherboard', 'mainboard',
            'sound', 'audio', 'speaker', 'speakers', 'headphone', 'headphones',
            'microphone', 'mic', 'webcam', 'camera',
            'port', 'ports', 'usb', 'hdmi', 'vga', 'dvi', 'displayport',
            'bluetooth', 'infrared', 'nfc', 'thunderbolt',
            'driver', 'drivers', 'firmware', 'bios', 'uefi',
            'boot', 'booting', 'booted', 'bootup', 'startup', 'reboot', 'rebooting',
            'restart', 'restarting', 'restarted',
            'shutdown', 'shutting', 'shutdowns', 'power-off',
            'sleep', 'hibernate', 'standby', 'suspend',
            'freeze', 'freezing', 'frozen', 'hang', 'hanging', 'hung',
            'slow', 'slower', 'slowest', 'lag', 'lagging', 'lagged', 'latency',
            'fast', 'faster', 'fastest', 'speed', 'performance',
            'access', 'accessing', 'accessed', 'inaccessible',
            'permission', 'permissions', 'rights', 'privilege', 'privileges',
            'admin', 'administrator', 'administrators', 'root', 'sudo',
            'share', 'shared', 'sharing', 'shares', 'network-share',
            'configuration', 'config', 'configs', 'configure', 'configured',
            'settings', 'setting', 'option', 'options', 'preferences',
            'service', 'services', 'daemon', 'daemons',
            'process', 'processes', 'thread', 'threads', 'task', 'tasks',
            'job', 'jobs', 'queue', 'queues',
            'log', 'logs', 'event', 'events', 'alert', 'alerts',
            'fail', 'failed', 'failing', 'failure', 'error-code',
            'success', 'successful', 'successfully', 'succeed', 'succeeded',
            'active', 'inactive', 'enabled', 'disabled', 'on', 'off',
            'available', 'unavailable', 'online', 'offline',
            'valid', 'invalid', 'correct', 'incorrect', 'wrong',
            'run', 'running', 'ran', 'execute', 'executing', 'executed',
            'start', 'starting', 'started', 'launch', 'launching', 'launched',
            'stop', 'stopping', 'stopped', 'terminate', 'terminating', 'terminated',
            'kill', 'killing', 'killed', 'end', 'ending', 'ended',
            'copy', 'copied', 'copying', 'paste', 'pasted', 'pasting',
            'cut', 'cutting', 'move', 'moved', 'moving',
            'rename', 'renamed', 'renaming',
            'compress', 'compressed', 'compressing', 'compression',
            'decompress', 'decompressed', 'decompressing',
            'zip', 'zipped', 'zipping', 'unzip', 'unzipped', 'unzipping',
            'archive', 'archived', 'archiving', 'rar', 'tar', 'gzip',
            'encrypt', 'encrypted', 'encrypting', 'encryption',
            'decrypt', 'decrypted', 'decrypting', 'decryption',
            'format', 'formatted', 'formatting', 'reformat', 'reformatted',
            'partition', 'partitioned', 'partitioning', 'repartition',
            
            # === COMMON EXPRESSIONS ===
            'hello', 'hi', 'hey', 'greetings', 'howdy',
            'thanks', 'thank', 'thankyou', 'thx', 'ty',
            'please', 'pls', 'plz',
            'sorry', 'apologize', 'apologies', 'excuse',
            'help', 'urgent', 'asap', 'emergency', 'critical',
            'quick', 'quickly', 'fast', 'slow', 'slowly',
            'today', 'yesterday', 'tomorrow', 'tonight',
            'morning', 'afternoon', 'evening', 'night',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'week', 'month', 'year', 'day', 'hour', 'minute', 'second',
            'always', 'never', 'sometimes', 'often', 'rarely', 'usually', 'frequently',
            'very', 'quite', 'too', 'so', 'such',
            'more', 'less', 'most', 'least', 'much', 'many', 'few', 'several',
            'good', 'bad', 'better', 'worse', 'best', 'worst',
            'fine', 'ok', 'okay', 'alright', 'great', 'excellent',
            'possible', 'impossible', 'maybe', 'perhaps', 'probably',
            'easy', 'easier', 'easiest', 'difficult', 'harder', 'hardest',
            'hard', 'simple', 'complex', 'complicated',
            'new', 'newer', 'newest', 'old', 'older', 'oldest',
            'latest', 'current', 'previous', 'next', 'last', 'first',
            'yes', 'no', 'not', 'none', 'nothing', 'everything', 'something', 'anything',
            'all', 'any', 'some', 'every', 'each', 'both', 'either', 'neither',
            
            # === NUMBERS ===
            'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
            'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
            'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',
            'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
            'hundred', 'thousand', 'million', 'billion',
            'first', 'second', 'third', 'fourth', 'fifth', 'sixth',
        }
        
        english_set.update(english_manual)
        return english_set
    
    def load_arabic_words(self):
        """Dictionnaire arabe étendu"""
        return {
            # === MOTS DE BASE ===
            'في', 'من', 'إلى', 'على', 'عن', 'مع', 'بعد', 'قبل', 'تحت', 'فوق', 'أمام', 'وراء', 'بين',
            'هذا', 'هذه', 'ذلك', 'تلك', 'هؤلاء', 'أولئك',
            'التي', 'الذي', 'اللذان', 'اللتان', 'الذين', 'اللواتي',
            'ما', 'ماذا', 'لا', 'نعم', 'كلا', 'بلى',
            'أو', 'و', 'لكن', 'إذا', 'لو', 'إن', 'أن',
            'كيف', 'أين', 'متى', 'لماذا', 'من', 'كم',
            'هل', 'ألا', 'ألم', 'أليس',
            
            # === PRONOMS ===
            'أنا', 'أنت', 'أنتِ', 'هو', 'هي', 'نحن', 'أنتم', 'أنتن', 'هم', 'هن',
            'لي', 'لك', 'لكِ', 'له', 'لها', 'لنا', 'لكم', 'لكن', 'لهم', 'لهن',
            'بي', 'بك', 'بكِ', 'به', 'بها', 'بنا', 'بكم', 'بكن', 'بهم', 'بهن',
            'معي', 'معك', 'معكِ', 'معه', 'معها', 'معنا', 'معكم', 'معكن', 'معهم', 'معهن',
            'عندي', 'عندك', 'عندكِ', 'عنده', 'عندها', 'عندنا', 'عندكم', 'عندكن', 'عندهم', 'عندهن',
            
            # === VOCABULAIRE IT ARABE MASSIF ===
            'الحاسوب', 'الحاسب', 'الكمبيوتر', 'الكومبيوتر', 'حاسوب', 'حاسب', 'كمبيوتر',
            'الطابعة', 'طابعة', 'طباعة', 'طبع', 'يطبع', 'مطبوع',
            'الشاشة', 'شاشة', 'المراقب', 'مراقب', 'العرض', 'عرض',
            'لوحة', 'المفاتيح', 'الفأرة', 'الماوس', 'فأرة', 'ماوس',
            'الشبكة', 'شبكة', 'الإنترنت', 'إنترنت', 'انترنت', 'النت',
            'البرنامج', 'برنامج', 'برامج', 'التطبيق', 'تطبيق', 'تطبيقات',
            'النظام', 'نظام', 'أنظمة', 'التشغيل', 'تشغيل',
            'الخادم', 'خادم', 'خوادم', 'السيرفر', 'سيرفر', 'العميل', 'عميل',
            'مشكلة', 'مشاكل', 'خطأ', 'أخطاء', 'عطل', 'أعطال',
            'مساعدة', 'دعم', 'إصلاح', 'حل', 'حلول',
            'تثبيت', 'تحديث', 'ترقية', 'تحديثات', 'نسخة', 'إصدار',
            'ملف', 'ملفات', 'مجلد', 'مجلدات', 'وثيقة', 'وثائق', 'مستند', 'مستندات',
            'نسخ', 'احتياطي', 'استعادة', 'حفظ', 'محفوظ',
            'تحميل', 'رفع', 'تنزيل', 'تحميلات',
            'مستخدم', 'مستخدمين', 'حساب', 'حسابات', 'ملف', 'شخصي',
            'كلمة', 'مرور', 'سر', 'رمز', 'باسورد', 'باسوورد',
            'دخول', 'خروج', 'تسجيل', 'الدخول', 'الخروج',
            'بريد', 'إلكتروني', 'إيميل', 'ايميل', 'ميل', 'رسالة', 'رسائل',
            'متصفح', 'مستعرض', 'متصفحات', 'كروم', 'فايرفوكس', 'سفاري',
            'موقع', 'مواقع', 'صفحة', 'صفحات', 'ويب', 'رابط', 'روابط',
            'مضاد', 'فيروسات', 'جدار', 'حماية', 'أمان', 'أمن', 'حماية',
            'فيروس', 'فيروسات', 'برمجيات', 'خبيثة',
            'ذاكرة', 'رام', 'قرص', 'صلب', 'تخزين', 'مساحة',
            'معالج', 'بروسيسور', 'بطاقة', 'رسومات', 'صوت',
            'واي', 'فاي', 'سلكي', 'لاسلكي', 'كابل', 'سلك', 'كيبل',
            'منفذ', 'منافذ', 'يو', 'اس', 'بي',
            'برنامج', 'تشغيل', 'سائق', 'درايفر', 'جهاز', 'أجهزة', 'أداة', 'أدوات',
            'إعادة', 'تشغيل', 'إغلاق', 'سكون', 'إسبات',
            'بطيء', 'سريع', 'متوقف', 'معطل', 'يعمل', 'لا', 'يعمل',
            
            # === EXPRESSIONS COURANTES ===
            'السلام', 'عليكم', 'وعليكم', 'أهلا', 'مرحبا', 'أهلاً', 'مرحباً',
            'شكرا', 'شكراً', 'من', 'فضلك', 'فضلك', 'لو', 'سمحت',
            'مساعدة', 'عاجل', 'سريع', 'بطيء', 'ممكن', 'يمكن',
            'اليوم', 'أمس', 'غدا', 'غداً', 'الصباح', 'المساء', 'الليل',
            'دائما', 'دائماً', 'أبدا', 'أبداً', 'أحيانا', 'أحياناً', 'غالبا', 'غالباً',
            'نادرا', 'نادراً', 'عادة', 'عادةً',
            'جدا', 'جداً', 'كثيرا', 'كثيراً', 'قليلا', 'قليلاً',
            'أكثر', 'أقل', 'كثير', 'قليل', 'بعض', 'كل', 'جميع',
            'جيد', 'سيء', 'أفضل', 'أسوأ', 'ممتاز', 'رائع',
            'سهل', 'صعب', 'بسيط', 'معقد',
            'ممكن', 'مستحيل', 'ربما', 'حتماً', 'بالتأكيد',
            'نعم', 'لا', 'حسناً', 'طيب', 'تمام',
            
            # === NOMBRES ===
            'صفر', 'واحد', 'اثنان', 'اثنين', 'ثلاثة', 'أربعة', 'خمسة',
            'ستة', 'سبعة', 'ثمانية', 'تسعة', 'عشرة',
            'عشرون', 'ثلاثون', 'أربعون', 'خمسون', 'ستون', 'سبعون', 'ثمانون', 'تسعون',
            'مئة', 'مائة', 'ألف', 'مليون', 'مليار',
            'الأول', 'الثاني', 'الثالث', 'الرابع', 'الخامس',
            
            # === VERBES COURANTS ===
            'أريد', 'تريد', 'يريد', 'نريد', 'أكون', 'تكون', 'يكون', 'نكون',
            'أعمل', 'تعمل', 'يعمل', 'نعمل', 'أفعل', 'تفعل', 'يفعل', 'نفعل',
            'أذهب', 'تذهب', 'يذهب', 'نذهب', 'آتي', 'تأتي', 'يأتي', 'نأتي',
            'أعرف', 'تعرف', 'يعرف', 'نعرف', 'أفهم', 'تفهم', 'يفهم', 'نفهم',
            'أستطيع', 'تستطيع', 'يستطيع', 'نستطيع', 'أحتاج', 'تحتاج', 'يحتاج', 'نحتاج',
            'أحب', 'تحب', 'يحب', 'نحب', 'أجد', 'تجد', 'يجد', 'نجد',
            'أقول', 'تقول', 'يقول', 'نقول', 'أرى', 'ترى', 'يرى', 'نرى',
        }
    
    def load_tunisian_latin_words(self):
        """Dictionnaire tunisien latin massif"""
        return {
            # === SALUTATIONS ÉTENDUES ===
            'salam', 'salem', 'salaam', 'slm', 'ahla', 'ahlen', 'ahla', 'ahlein',
            'kifek', 'kifkom', 'kifkm', 'kefekkif', 'kifach',
            'sbah', 'sbeh', 'khir', 'kheir', 'elkheir', 'nour',
            'masa', 'msa', 'labes', 'labess', 'labas',
            'hamdoulah', 'hamdolah', 'hamdoullah', 'elhamdoulilah',
            'barak', 'allahou', 'fik', 'fikom', 'fikoum',
            'inchallah', 'inchalah', 'machallah', 'machalah', 'yarbi', 'yarbbi',
            'besslama', 'b7a9', 'yesslmek', 'ya3tik', 'essa7a',
            
            # === PRONOMS TUNISIENS ===
            '3andi', '3andek', '3andou', '3andha', '3andna', '3andkom', '3andhom',
            'ani', 'eni', 'enti', 'enta', 'entouma', 'entoma',
            'houa', 'houwa', 'hiya', 'hia', 'a7na', 'ah7na', 'houma', 'houm',
            'eli', 'elli', 'ili', 'illi', 'elliii',
            'mata3i', 'mata3ek', 'mata3ou', 'mata3ha', 'mata3na', 'mata3kom', 'mata3hom',
            'ta3i', 'ta3ek', 'ta3ou', 'ta3ha', 'ta3na', 'ta3kom', 'ta3hom',
            'm3a', 'ma3a', 'm3ak', 'ma3ak', 'm3ah', 'ma3ah', 'm3aha', 'ma3aha',
            
            # === VERBES COURANTS TUNISIENS (TOUTES FORMES) ===
            'nejjem', 'najjem', 'tnejjem', 'ynejjem', 'tnejjem', 'nejmou', 'tenjmou', 'yenjmou',
            'n7eb', 't7eb','n7eb', 't7eb', 'y7eb', 't7eb', 'n7ebou', 't7ebou', 'y7ebou',
            'n7ebbek', 't7ebbek', 'y7ebbek', 'n7ebbha', 't7ebbha', 'y7ebbha',
            'bech', 'bch', 'bach', 'nak', 'tak', 'yak', 'nakhou', 'takou', 'yakou',
            'na3mel', 'ta3mel', 'ya3mel', 'ta3mel', 'na3mlou', 'ta3mlou', 'ya3mlou',
            'nkamel', 'tkamel', 'ykamel', 'tkamel', 'nkamlou', 'tkamlou', 'ykamlou',
            'nrou7', 'trou7', 'yrou7', 'trou7', 'nrou7ou', 'trou7ou', 'yrou7ou',
            'tji', 'yji', 'nja', 'njou', 'tjou', 'yjou', 'jey', 'jeya',
            'nekteb', 'tekteb', 'yekteb', 'tekteb', 'nekbou', 'tekbou', 'yekbou',
            'n7el', 't7el', 'y7el', 't7el', 'n7elou', 't7elou', 'y7elou',
            'nekhou', 'te5ou', 'ye5ou', 'te5ou', 'ne5dhou', 'te5dhou', 'ye5dhou',
            'na3ti', 'ta3ti', 'ya3ti', 'ta3ti', 'na3tiou', 'ta3tiou', 'ya3tiou',
            'nems7i', 'tems7i', 'yems7i', 'tems7i', 'nemssiou', 'temssiou', 'yemssiou',
            'n9ra', 't9ra', 'y9ra', 't9ra', 'n9raw', 't9raw', 'y9raw',
            'nchuf', 'tchuf', 'ychuf', 'tchuf', 'nchoufu', 'tchoufu', 'ychoufu',
            'na3ref', 'ta3ref', 'ya3ref', 'ta3ref', 'na3rfu', 'ta3rfu', 'ya3rfu',
            'nfhem', 'tfhem', 'yfhem', 'tfhem', 'nfhmu', 'tfhmu', 'yfhmu',
            'n7ot', 't7ot', 'y7ot', 't7ot', 'n7ottou', 't7ottou', 'y7ottou',
            'n5arrej', 't5arrej', 'y5arrej', 't5arrej', 'n5arjou', 't5arjou', 'y5arjou',
            'nodhom', 'todhom', 'yodhom', 'todhom', 'nodhomou', 'todhomou', 'yodhomou',
            'nsebbi', 'tsebbi', 'ysebbi', 'tsebbi', 'nsebbiw', 'tsebbiw', 'ysebbiw',
            
            # === MOTS COURANTS TUNISIENS ===
            'barcha', 'برشا', 'برشة', 'beaucoup', 'bcp',
            'chwaya', 'chwaya', 'chwiya', 'chway', 'peu',
            'ki', 'kif', 'kima', 'comme', 'comment',
            'wakt', 'wa9t', 'temps', 'moment',
            'lyoum', 'lyouma', 'elyoum', 'el youm', 'aujourdhui',
            'ghodwa', 'ghodwa', 'غدوة', 'demain',
            'emes', 'emess', 'البارح', 'hier',
            'tawa', 'taw', 'توة', 'maintenant', 'now',
            'ba3d', 'ba3ad', 'après', 'apres',
            '9bal', '9bel', 'gbal', 'avant',
            'kol', 'koll', 'كل', 'tout', 'tous',
            'wa7ed', 'wa7d', 'w7ed', 'واحد', 'un',
            'w7da', 'wa7da', 'وحدة', 'une',
            'moch', 'mouch', 'mech', 'mesh', 'mch', 'pas', 'non',
            'chay', 'chey', 'شي', 'quelquechose',
            '7aja', 'haja', 'حاجة', 'chose', 'truc',
            'haya', 'heya', 'هية', 'cela',
            'heka', 'hakka', 'هكة', 'comme-ca',
            'hedheka', 'hadheka', 'هذاكة', 'celui-la',
            'hethi', 'hedhi', 'hadhihi', 'هاذي', 'celle-ci',
            'wa9tech', 'wa9tach', 'waktech', 'quand',
            'chkoun', 'chkoon', 'shkoun', 'qui',
            'chneya', 'chnowa', 'chnoua', 'quoi',
            'kifech', 'kifach', 'kifash', 'comment',
            'win', 'winou', 'fein', 'ou',
            '3lech', '3lach', 'علاش', 'pourquoi',
            '9addech', '9adech', 'kadech', 'combien',
            'ey', 'eya', 'oui', 'yes',
            'le', 'lé', 'non', 'no',
            'yezzi', 'yezi', 'يزّي', 'assez', 'stop',
            'zeda', 'zada', 'زادة', 'aussi', 'encore',
            'ken', 'kén', 'كان', 'si', 'seulement',
            'ama', 'emma', 'أما', 'mais',
            'w', 'wel', 'walla', 'ou', 'et',
            
            # === VOCABULAIRE IT TUNISIEN ===
            'pc', 'ordi', 'ordinateur', 'micro', 'portable',
            'imprimante', 'imprimant', 'طابعة', 'tabe3a',
            'ecran', 'écran', 'شاشة', 'chacha',
            'clavier', 'كلافي', 'klafi', 'touche', 'touches',
            'souris', 'mouse', 'فارة', 'fara',
            'internet', 'net', 'انترنات', 'wifi', 'réseau', 'reseau',
            'email', 'mail', 'ميل', 'mel', 'message',
            'password', 'pass', 'mdp', 'mot-passe',
            'programme', 'برنامج', 'barnamej', 'logiciel',
            'fichier', 'فيشي', 'fichi', 'ملف', 'mlef',
            'dossier', 'dossi', 'مجلد', 'mejled',
            'backup', 'sauvegarde', 'copie',
            'serveur', 'سيرفور', 'serveur', 'server',
            'windows', 'وندوز', 'windoz', 'system', 'système',
            'mochkla', 'mochkl', 'مشكلة', 'mushkla', 'problème', 'probleme',
            'erreur', 'ارور', 'error', 'غلطة', 'ghalta',
            'aide', 'help', 'aidez-moi', 'sa3edni', 'sa3douni',
            'urgent', 'مستعجل', 'moste3jel', 'vite', 'rapide',
            'marche', 'pas', 'يخدم', 'ye5dem', 'khdem', 'work',
            'bloqué', 'مسدود', 'masdoud', 'block', 'freeze',
            'lent', 'بطيء', 'bati', 'slow', 'ralenti',
            'installation', 'install', 'نصب', 'nasseb',
            'télécharger', 'download', 'تحميل', 'ta7mil', '7ammel',
            'connexion', 'كونكسيون', 'conecté', 'connecté',
            
            # === EXPRESSIONS MIXTES TUNISO-FRANÇAISES ===
            'makanch', 'mknch', 'makench', 'يما-كانش', 'pas-il-y-a',
            'famma', 'fema', 'فمة', 'il-y-a',
            'maaneha', 'ma3neha', 'معناها', 'ca-veut-dire',
            'yaani', 'ya3ni', 'يعني', 'cest-a-dire',
            'behi', 'behya', 'باهي', 'ok', 'bien',
            'bahi', 'bahia', 'bon', 'bonne',
            'mahla', 'ma7la', 'ماحلى', 'comme-cest-beau',
            'wallah', 'walla', 'والله', 'je-jure',
            'ma3lich', 'ma3leech', 'معليش', 'pas-grave',
            'rabi', 'rabbi', 'ربي', 'mon-dieu',
            'yesser', 'yasser', 'ياسر', 'beaucoup',
            'chbik', 'chbeek', 'شبيك', 'quoi-toi',
            'mala', 'mela', 'ما-لا', 'quoi-non',
            'ama', 'amma', 'أما', 'alors',
            'normalment', 'normalma', 'normalement',
            
            # === CHIFFRES ARABES EN LATIN (pour detection) ===
            '3ayn', '3ein', '7', '9', '5', '8', '2', '6',
            'gh', 'kh', 'th', 'dh', 'sh', 'ch',
        }