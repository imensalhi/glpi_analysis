 # Script principal
from glpi_database import GLPIDatabase
from glpi_data_extractor import GLPIDataExtractor
from text_cleaner import TextCleaner
from language_dictionaries import LanguageDictionaries
from arabic_detector import ArabicDetector
from language_classifier import LanguageClassifier
import pandas as pd

def main():
    print("🎯 ANALYSE LINGUISTIQUE DES TICKETS GLPI (avec codes techniques)")
    print("=" * 60)
    
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
    classifier = LanguageClassifier(
        dictionaries.dictionaries, 
        arabic_detector, 
        text_cleaner
    )
    
    print(f"\n🔄 Analyse de {len(df)} tickets...")
    
    # Analyser chaque ticket
    results = []
    for idx, row in df.iterrows():
        ticket_analysis = classifier.analyze_text(row['full_text'])
        ticket_analysis['ticket_id'] = row['id']
        ticket_analysis['title'] = row['clean_title']
        ticket_analysis['confidence'] = classifier.calculate_confidence(ticket_analysis)
        results.append(ticket_analysis)
        
        # Afficher progression
        if (idx + 1) % 10 == 0:
            print(f"   Analysé {idx + 1}/{len(df)} tickets...")
    
    # Créer DataFrame des résultats
    results_df = pd.DataFrame(results)
    
    # Afficher statistiques globales
    print_global_statistics(results_df)
    
    # Afficher exemples détaillés
    print_detailed_examples(results, df)
    
    # NOUVEAU: Afficher analyse des codes techniques
    print_technical_codes_analysis(results)
    
    # Sauvegarder les résultats
    results_df.to_csv('analysis_results.csv', index=False)
    print("\n✅ Résultats sauvegardés dans 'analysis_results.csv'")
    
    db.close()

def print_global_statistics(results_df):
    """Afficher les statistiques globales - INCLUT LES CODES TECHNIQUES"""
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
    tech_total = results_df['technical_codes'].sum()  # MODIFIÉ: nouveau nom
    unknown_total = results_df['unknown'].sum()
    
    # Pourcentages
    print(f"\n📈 RÉPARTITION DES MOTS:")
    print(f"  • 🇫🇷 Français: {french_total} ({french_total/total_words*100:.1f}%)")
    print(f"  • 🇬🇧 Anglais: {english_total} ({english_total/total_words*100:.1f}%)")
    print(f"  • 🇹🇳 Arabe (script): {arabic_total} ({arabic_total/total_words*100:.1f}%)")
    print(f"  • 🏴‍☠️ Tunisien latin: {tunisian_total} ({tunisian_total/total_words*100:.1f}%)")
    print(f"  • 💻 CODES TECHNIQUES: {tech_total} ({tech_total/total_words*100:.1f}%)")  # NOUVEAU
    print(f"  • ❓ Non identifiés: {unknown_total} ({unknown_total/total_words*100:.1f}%)")
    
    # Confiance moyenne
    avg_confidence = results_df['confidence'].mean()
    print(f"\n🎯 Confiance moyenne: {avg_confidence:.1f}%")

def print_technical_codes_analysis(results):
    """NOUVELLE FONCTION: Analyser les codes techniques trouvés"""
    print(f"\n💻 ANALYSE DES CODES TECHNIQUES")
    print("=" * 35)
    
    # Compter tous les types de codes techniques
    all_tech_details = {}
    total_tech_codes = 0
    
    for result in results:
        total_tech_codes += result.get('technical_codes', 0)
        tech_details = result.get('tech_details', {})
        
        for tech_type, count in tech_details.items():
            if tech_type in all_tech_details:
                all_tech_details[tech_type] += count
            else:
                all_tech_details[tech_type] = count
    
    print(f"Total codes techniques détectés: {total_tech_codes}")
    
    if all_tech_details:
        print(f"\n🔧 TYPES DE CODES DÉTECTÉS:")
        for tech_type, count in sorted(all_tech_details.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_tech_codes * 100) if total_tech_codes > 0 else 0
            print(f"  • {tech_type.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
    
    # Montrer quelques exemples
    print(f"\n📋 EXEMPLES DE CODES TROUVÉS:")
    examples_shown = 0
    for result in results[:10]:  # Regarder les 10 premiers tickets
        tech_codes = result.get('identified_tech_codes', {})
        if tech_codes and examples_shown < 3:
            print(f"  Ticket #{result['ticket_id']}:")
            for code_type, codes in tech_codes.items():
                print(f"    {code_type}: {', '.join(codes[:3])}{'...' if len(codes) > 3 else ''}")
            examples_shown += 1
        if examples_shown >= 3:
            break

def print_detailed_examples(results, df):
    """Afficher des exemples détaillés - INCLUT LES CODES TECHNIQUES"""
    print(f"\n📋 EXEMPLES D'ANALYSE DÉTAILLÉE")
    print("=" * 40)
    
    for i in range(min(5, len(results))):
        result = results[i]
        ticket_text = df.iloc[i]['full_text']
        
        print(f"\n--- Ticket #{result['ticket_id']} ---")
        print(f"Titre: {result['title']}")
        print(f"Texte: {ticket_text[:100]}...")
        print(f"Total mots: {result['total_words']}")
        print(f"🇫🇷 Français: {result['french']}, 🇬🇧 Anglais: {result['english']}")
        print(f"🇹🇳 Arabe: {result['arabic_script']}, 🏴‍☠️ Tunisien: {result['tunisian_latin']}")
        print(f"💻 CODES TECHNIQUES: {result['technical_codes']}")  # NOUVEAU
        print(f"❓ Inconnus: {result['unknown']}")
        print(f"🎯 Confiance: {result['confidence']}%")
        
        # NOUVEAU: Afficher les codes techniques trouvés
        if result.get('technical_codes', 0) > 0:
            tech_details = result.get('tech_details', {})
            print(f"🔧 Détail codes techniques: {dict(tech_details)}")
            
            tech_codes = result.get('identified_tech_codes', {})
            if tech_codes:
                print(f"📝 Exemples de codes: ", end="")
                examples = []
                for code_type, codes in tech_codes.items():
                    examples.extend(codes[:2])  # Prendre 2 exemples par type
                print(", ".join(examples[:5]))  # Afficher max 5 exemples

if __name__ == "__main__":
    main()