# main_analyzer.py
from glpi_database import GLPIDatabase
from glpi_data_extractor import GLPIDataExtractor
from text_cleaner import TextCleaner
from language_dictionaries import LanguageDictionaries
from arabic_detector import ArabicDetector
from language_classifier import LanguageClassifier
import pandas as pd
from datetime import datetime

def main():
    print("=" * 70)
    print("   ANALYSE LINGUISTIQUE AVANCÉE DES TICKETS GLPI")
    print("   Version 2.0 - Avec scoring et analyse contextuelle")
    print("=" * 70)
    
    # Initialiser la base de données
    db = GLPIDatabase('config.ini')
    if not db.connect():
        print("\n[ERREUR] Impossible de se connecter à la base de données")
        return
    
    print("\n[1/6] Connexion à la base de données réussie")
    
    # Extraire les données
    extractor = GLPIDataExtractor(db)
    df = extractor.extract_tickets_data()
    df = extractor.prepare_dataset(df)
    
    print(f"[2/6] {len(df)} tickets extraits et nettoyés")
    
    # Initialiser les composants
    print("[3/6] Initialisation des composants d'analyse...")
    text_cleaner = TextCleaner()
    dictionaries = LanguageDictionaries()
    arabic_detector = ArabicDetector()
    classifier = LanguageClassifier(
        dictionaries, 
        arabic_detector, 
        text_cleaner
    )
    
    print(f"    - Dictionnaire français: {len(dictionaries.dictionaries['french'])} mots")
    print(f"    - Dictionnaire anglais: {len(dictionaries.dictionaries['english'])} mots")
    print(f"    - Dictionnaire arabe: {len(dictionaries.dictionaries['arabic_standard'])} mots")
    print(f"    - Dictionnaire tunisien: {len(dictionaries.dictionaries['tunisian_latin'])} mots")
    
    # Analyser les tickets
    print(f"\n[4/6] Analyse de {len(df)} tickets en cours...")
    results = []
    start_time = datetime.now()
    
    for idx, row in df.iterrows():
        ticket_analysis = classifier.analyze_text(row['full_text'])
        ticket_analysis['ticket_id'] = row['id']
        ticket_analysis['title'] = row['clean_title']
        ticket_analysis['confidence'] = classifier.calculate_confidence(ticket_analysis)
        results.append(ticket_analysis)
        
        # Progression
        if (idx + 1) % 100 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = (idx + 1) / elapsed
            remaining = (len(df) - idx - 1) / rate
            print(f"    Progression: {idx + 1}/{len(df)} tickets "
                  f"({(idx+1)/len(df)*100:.1f}%) - "
                  f"Temps restant: ~{int(remaining)}s")
    
    total_time = (datetime.now() - start_time).total_seconds()
    print(f"    Analyse terminée en {total_time:.1f}s ({len(df)/total_time:.1f} tickets/s)")
    
    # Créer DataFrame des résultats
    results_df = pd.DataFrame(results)
    
    # Afficher statistiques
    print("\n[5/6] Génération des statistiques...")
    print_global_statistics(results_df)
    print_confidence_analysis(results_df)
    print_language_distribution(results_df)
    print_technical_codes_analysis(results)
    print_detailed_examples(results, df)
    
    # Sauvegarder
    print("\n[6/6] Sauvegarde des résultats...")
    output_file = f'analysis_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    results_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"    Fichier créé: {output_file}")
    
    # Sauvegarder détails par mot
    detailed_file = f'word_details_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    save_word_details(results, detailed_file)
    print(f"    Détails par mot: {detailed_file}")
    
    db.close()
    print("\n" + "=" * 70)
    print("   ANALYSE TERMINÉE AVEC SUCCÈS")
    print("=" * 70)

def print_global_statistics(results_df):
    """Statistiques globales améliorées"""
    total_tickets = len(results_df)
    total_words = results_df['total_words'].sum()
    
    print("\n" + "=" * 70)
    print("   STATISTIQUES GLOBALES")
    print("=" * 70)
    print(f"\nTickets analysés: {total_tickets:,}")
    print(f"Mots totaux analysés: {total_words:,}")
    print(f"Moyenne mots/ticket: {total_words/total_tickets:.1f}")
    
    # Répartition des langues
    french_total = results_df['french'].sum()
    english_total = results_df['english'].sum()
    arabic_total = results_df['arabic_script'].sum()
    tunisian_total = results_df['tunisian_latin'].sum()
    tech_total = results_df['technical_codes'].sum()
    unknown_total = results_df['unknown'].sum()
    
    print(f"\n{'Langue':<20} {'Mots':>10} {'Pourcentage':>12}")
    print("-" * 42)
    print(f"{'Français':<20} {french_total:>10,} {french_total/total_words*100:>11.1f}%")
    print(f"{'Anglais':<20} {english_total:>10,} {english_total/total_words*100:>11.1f}%")
    print(f"{'Arabe (script)':<20} {arabic_total:>10,} {arabic_total/total_words*100:>11.1f}%")
    print(f"{'Tunisien latin':<20} {tunisian_total:>10,} {tunisian_total/total_words*100:>11.1f}%")
    print(f"{'Codes techniques':<20} {tech_total:>10,} {tech_total/total_words*100:>11.1f}%")
    print(f"{'Non identifiés':<20} {unknown_total:>10,} {unknown_total/total_words*100:>11.1f}%")

def print_confidence_analysis(results_df):
    """Analyse de confiance détaillée"""
    print("\n" + "=" * 70)
    print("   ANALYSE DE CONFIANCE")
    print("=" * 70)
    
    avg_confidence = results_df['confidence'].mean()
    median_confidence = results_df['confidence'].median()
    min_confidence = results_df['confidence'].min()
    max_confidence = results_df['confidence'].max()
    
    print(f"\nConfiance moyenne: {avg_confidence:.1f}%")
    print(f"Confiance médiane: {median_confidence:.1f}%")
    print(f"Confiance minimale: {min_confidence:.1f}%")
    print(f"Confiance maximale: {max_confidence:.1f}%")
    
    # Distribution par tranches
    print(f"\nDistribution de confiance:")
    bins = [0, 50, 70, 85, 95, 100]
    labels = ['Très faible (<50%)', 'Faible (50-70%)', 'Moyenne (70-85%)', 
              'Bonne (85-95%)', 'Excellente (95-100%)']
    
    results_df['confidence_bin'] = pd.cut(results_df['confidence'], bins=bins, labels=labels)
    distribution = results_df['confidence_bin'].value_counts().sort_index()
    
    for label, count in distribution.items():
        percentage = count / len(results_df) * 100
        print(f"  {label:<25} {count:>6} tickets ({percentage:>5.1f}%)")

def print_language_distribution(results_df):
    """Distribution par langue dominante"""
    print("\n" + "=" * 70)
    print("   LANGUE DOMINANTE PAR TICKET")
    print("=" * 70)
    
    # Déterminer langue dominante pour chaque ticket
    def get_dominant_language(row):
        lang_counts = {
            'Français': row['french'],
            'Anglais': row['english'],
            'Arabe': row['arabic_script'],
            'Tunisien': row['tunisian_latin'],
            'Technique': row['technical_codes']
        }
        if sum(lang_counts.values()) == 0:
            return 'Vide'
        return max(lang_counts, key=lang_counts.get)
    
    results_df['dominant_language'] = results_df.apply(get_dominant_language, axis=1)
    dominant_dist = results_df['dominant_language'].value_counts()
    
    print(f"\n{'Langue dominante':<20} {'Tickets':>10} {'Pourcentage':>12}")
    print("-" * 42)
    for lang, count in dominant_dist.items():
        percentage = count / len(results_df) * 100
        print(f"{lang:<20} {count:>10} {percentage:>11.1f}%")

def print_technical_codes_analysis(results):
    """Analyse des codes techniques"""
    print("\n" + "=" * 70)
    print("   ANALYSE DES CODES TECHNIQUES")
    print("=" * 70)
    
    all_tech_details = {}
    total_tech_codes = 0
    tickets_with_tech = 0
    
    for result in results:
        tech_count = result.get('technical_codes', 0)
        if tech_count > 0:
            tickets_with_tech += 1
            total_tech_codes += tech_count
            
        tech_details = result.get('tech_details', {})
        for tech_type, count in tech_details.items():
            all_tech_details[tech_type] = all_tech_details.get(tech_type, 0) + count
    
    print(f"\nTotal codes techniques détectés: {total_tech_codes:,}")
    print(f"Tickets contenant des codes: {tickets_with_tech} ({tickets_with_tech/len(results)*100:.1f}%)")
    
    if all_tech_details:
        print(f"\nTypes de codes détectés:")
        sorted_tech = sorted(all_tech_details.items(), key=lambda x: x[1], reverse=True)
        for tech_type, count in sorted_tech:
            percentage = count / total_tech_codes * 100 if total_tech_codes > 0 else 0
            readable_type = tech_type.replace('_', ' ').title()
            print(f"  {readable_type:<25} {count:>6} ({percentage:>5.1f}%)")
    
    # Exemples de codes trouvés
    print(f"\nExemples de codes techniques trouvés:")
    examples_shown = 0
    for result in results[:20]:
        tech_codes = result.get('identified_tech_codes', {})
        if tech_codes and examples_shown < 3:
            print(f"\n  Ticket #{result['ticket_id']}:")
            for code_type, codes in tech_codes.items():
                readable_type = code_type.replace('_', ' ').title()
                sample = ', '.join(str(c) for c in codes[:3])
                if len(codes) > 3:
                    sample += f"... (+{len(codes)-3})"
                print(f"    {readable_type}: {sample}")
            examples_shown += 1

def print_detailed_examples(results, df):
    """Exemples détaillés d'analyse"""
    print("\n" + "=" * 70)
    print("   EXEMPLES D'ANALYSE DÉTAILLÉE")
    print("=" * 70)
    
    # Sélectionner exemples variés
    examples_indices = [
        0,  # Premier ticket
        len(results) // 4,  # 25%
        len(results) // 2,  # 50%
        3 * len(results) // 4,  # 75%
        len(results) - 1  # Dernier
    ]
    
    for idx_result, result_idx in enumerate(examples_indices[:5]):
        if result_idx >= len(results):
            continue
            
        result = results[result_idx]
        ticket_text = df.iloc[result_idx]['full_text']
        
        print(f"\n--- Exemple {idx_result + 1}: Ticket #{result['ticket_id']} ---")
        print(f"Titre: {result['title'][:60]}{'...' if len(result['title']) > 60 else ''}")
        print(f"Texte: {ticket_text[:100]}{'...' if len(ticket_text) > 100 else ''}")
        print(f"\nAnalyse:")
        print(f"  Total mots: {result['total_words']}")
        print(f"  Français: {result['french']}, Anglais: {result['english']}")
        print(f"  Arabe: {result['arabic_script']}, Tunisien: {result['tunisian_latin']}")
        print(f"  Codes techniques: {result['technical_codes']}")
        print(f"  Non identifiés: {result['unknown']}")
        print(f"  Confiance: {result['confidence']}%")
        
        # Afficher quelques mots avec leur classification
        word_details = result.get('word_details', [])
        if word_details:
            print(f"\n  Détail de quelques mots:")
            for i, detail in enumerate(word_details[:8]):
                lang_label = detail['language'].replace('_', ' ').title()
                conf = detail.get('confidence', 0)
                context_flag = ' [Contexte]' if detail.get('context_improved', False) else ''
                print(f"    '{detail['word']}' → {lang_label} ({conf}%){context_flag}")
            if len(word_details) > 8:
                print(f"    ... et {len(word_details) - 8} autres mots")

def save_word_details(results, filename):
    """Sauvegarder détails par mot dans un CSV"""
    all_word_details = []
    
    for result in results:
        ticket_id = result['ticket_id']
        word_details = result.get('word_details', [])
        
        for detail in word_details:
            all_word_details.append({
                'ticket_id': ticket_id,
                'word': detail['word'],
                'language': detail['language'],
                'confidence': detail.get('confidence', 0),
                'is_technical': detail.get('is_technical', False),
                'context_improved': detail.get('context_improved', False)
            })
    
    df_words = pd.DataFrame(all_word_details)
    df_words.to_csv(filename, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    main()