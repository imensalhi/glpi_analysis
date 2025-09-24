from glpi_database import GLPIDatabase
from glpi_data_extractor import GLPIDataExtractor
from text_cleaner import TextCleaner
from language_dictionaries import LanguageDictionaries
from arabic_detector import ArabicDetector
from language_classifier import LanguageClassifier
import pandas as pd
import json  # Ajout pour stocker groupes en JSON

def main():
    print("🎯 ANALYSE LINGUISTIQUE DES TICKETS GLPI")
    print("=" * 50)
    
    # Initialiser les composants
    db = GLPIDatabase('config.ini')
    if not db.connect():
        print("❌ Erreur de connexion")
        return
    
    # Extraire les données
    extractor = GLPIDataExtractor(db)
    df = extractor.extract_tickets_data()
    df = extractor.prepare_dataset(df)
    
    # Initialiser l'analyseur
    text_cleaner = TextCleaner()
    dictionaries = LanguageDictionaries()
    arabic_detector = ArabicDetector()
    classifier = LanguageClassifier(dictionaries.dictionaries, arabic_detector, text_cleaner)
    
    print(f"\n🔄 Analyse de {len(df)} tickets...")
    
    # Analyser chaque ticket
    results = []
    for idx, row in df.iterrows():
        ticket_analysis = classifier.analyze_text(row['full_text'])
        # Ajout : Grouper les mots par langue
        grouped_words = group_words_by_language(ticket_analysis['word_details'])
        ticket_analysis['grouped_words'] = grouped_words  # Pour affichage et CSV
        ticket_analysis['ticket_id'] = row['id']
        ticket_analysis['title'] = row['clean_title']
        ticket_analysis['confidence'] = classifier.calculate_confidence(ticket_analysis)
        results.append(ticket_analysis)
        
        # Afficher progression
        if (idx + 1) % 10 == 0:
            print(f"   Analysé {idx + 1}/{len(df)} tickets...")
    
    # Créer DataFrame des résultats
    results_df = pd.DataFrame(results)
    # Convertir grouped_words en JSON pour CSV (sinon pandas ne gère pas les dicts bien)
    results_df['grouped_words'] = results_df['grouped_words'].apply(json.dumps)
    
    # Afficher statistiques globales
    print_global_statistics(results_df)
    
    # Afficher exemples détaillés
    print_detailed_examples(results, df)
    
    # Sauvegarder les résultats
    results_df.to_csv('analysis_results.csv', index=False)
    print("\n✅ Résultats sauvegardés dans 'analysis_results.csv'")
    
    db.close()

def group_words_by_language(word_details):
    """Grouper les mots par langue/catégorie pour affichage détaillé"""
    groups = {
        'french': [],
        'english': [],
        'arabic_script': [],
        'tunisian_latin': [],
        'tech_codes': [],
        'unknown': []
    }
    for detail in word_details:
        lang = detail['language']
        if lang in groups:  # Vérifie pour éviter clés manquantes
            groups[lang].append(detail['word'])
    return groups

def print_global_statistics(results_df):
    """Afficher les statistiques globales de manière claire et organisée (table Markdown)"""
    total_tickets = len(results_df)
    total_words = results_df['total_words'].sum()
    
    print(f"\n📊 STATISTIQUES GLOBALES")
    print("=" * 30)
    print(f"Total tickets analysés: {total_tickets}")
    print(f"Total mots analysés: {total_words}")
    
    # Sommes par langue
    french_total = results_df['french'].sum()
    english_total = results_df['english'].sum()
    arabic_total = results_df['arabic_script'].sum()
    tunisian_total = results_df['tunisian_latin'].sum()
    tech_total = results_df['tech_codes'].sum()
    unknown_total = results_df['unknown'].sum()
    
    # Créer un DataFrame pour table claire
    stats_data = {
        'Langue/Catégorie': ['Français', 'Anglais', 'Arabe (script)', 'Tunisien latin', 'Codes techniques', 'Inconnus'],
        'Nombre de mots': [french_total, english_total, arabic_total, tunisian_total, tech_total, unknown_total],
        'Pourcentage (%)': [
            round(french_total / total_words * 100, 1) if total_words > 0 else 0,
            round(english_total / total_words * 100, 1) if total_words > 0 else 0,
            round(arabic_total / total_words * 100, 1) if total_words > 0 else 0,
            round(tunisian_total / total_words * 100, 1) if total_words > 0 else 0,
            round(tech_total / total_words * 100, 1) if total_words > 0 else 0,
            round(unknown_total / total_words * 100, 1) if total_words > 0 else 0
        ]
    }
    stats_df = pd.DataFrame(stats_data)
    print("\nRépartition des mots (table claire) :")
    print(stats_df.to_markdown(index=False))  # Affichage organisé en table Markdown
    
    # Confiance moyenne
    avg_confidence = results_df['confidence'].mean()
    print(f"\nConfiance moyenne: {avg_confidence:.1f}%")

def print_detailed_examples(results, df):
    """Afficher des exemples détaillés avec mots groupés par langue"""
    print(f"\n📋 EXEMPLES D'ANALYSE DÉTAILLÉE")
    print("=" * 40)
    
    for i in range(min(5, len(results))):
        result = results[i]
        ticket_text = df.iloc[i]['full_text']
        
        print(f"\n--- Ticket #{result['ticket_id']} ---")
        print(f"Titre: {result['title']}")
        print(f"Texte complet: {ticket_text[:100]}...")  # Limité pour clarté
        print(f"Total mots: {result['total_words']}")
        print(f"Confiance: {result['confidence']}%")
        
        # Affichage des comptes (comme avant)
        print("\nComptes par catégorie :")
        print(f"  • Français: {result['french']}")
        print(f"  • Anglais: {result['english']}")
        print(f"  • Arabe (script): {result['arabic_script']}")
        print(f"  • Tunisien latin: {result['tunisian_latin']}")
        print(f"  • Codes techniques: {result['tech_codes']}")
        print(f"  • Inconnus: {result['unknown']}")
        
        # Nouvel ajout : Liste des mots spécifiques par catégorie (seulement si >0)
        print("\nDétails des mots par catégorie :")
        for lang, words in result['grouped_words'].items():
            if words:  # Seulement si liste non vide
                print(f"  {lang.capitalize()} : {', '.join(words)}")
        
        if result['extracted_tech_codes']:
            print(f"\nCodes techniques extraits: {result['extracted_tech_codes']}")

if __name__ == "__main__":
    main()