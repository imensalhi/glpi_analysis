# analysis_reporter.py
import pandas as pd
import json
from datetime import datetime
#fichier optionelle 
class AnalysisReporter:
    def __init__(self, results_file='analysis_results.csv'):
        self.results_file = results_file
        self.df = pd.read_csv(results_file)
    
    def generate_readable_report(self, output_file='readable_analysis_report.txt'):
        """Générer un rapport lisible"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("📊 RAPPORT D'ANALYSE LINGUISTIQUE DES TICKETS GLPI\n")
            f.write("=" * 60 + "\n\n")
            
            # Statistiques globales
            self._write_global_stats(f)
            
            # Détail par ticket
            self._write_ticket_details(f)
            
            # Analyse par langue
            self._write_language_analysis(f)
            
            # Recommandations
            self._write_recommendations(f)
    
    def _write_global_stats(self, f):
        """Écrire les statistiques globales"""
        total_tickets = len(self.df)
        total_words = self.df['total_words'].sum()
        
        f.write("🎯 STATISTIQUES GLOBALES\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total tickets analysés: {total_tickets}\n")
        f.write(f"Total mots analysés: {total_words}\n\n")
        
        # Calcul des pourcentages
        languages = ['french', 'english', 'arabic_script', 'tunisian_latin']
        language_totals = {}
        
        for lang in languages:
            lang_total = self.df[lang].sum()
            percentage = (lang_total / total_words) * 100 if total_words > 0 else 0
            language_totals[lang] = {'total': lang_total, 'percentage': percentage}
        
        f.write("📈 RÉPARTITION DES LANGUES :\n")
        for lang, stats in language_totals.items():
            lang_name = self._get_language_name(lang)
            f.write(f"  • {lang_name}: {stats['total']} mots ({stats['percentage']:.1f}%)\n")
        
        f.write(f"  • Codes techniques: {self.df['tech_codes'].sum()} mots\n")
        f.write(f"  • Non identifiés: {self.df['unknown'].sum()} mots\n")
        
        avg_confidence = self.df['confidence'].mean()
        f.write(f"\n✅ Confiance moyenne de classification: {avg_confidence:.1f}%\n\n")
    
    def _write_ticket_details(self, f):
        """Écrire le détail par ticket de façon lisible"""
        f.write("📋 ANALYSE DÉTAILLÉE PAR TICKET\n")
        f.write("=" * 50 + "\n\n")
        
        for idx, row in self.df.iterrows():
            f.write(f"🎫 TICKET #{row['ticket_id']}\n")
            f.write(f"Titre: {row['title']}\n")
            
            # Statistiques du ticket
            f.write("📊 Composition linguistique :\n")
            langs = ['french', 'english', 'arabic_script', 'tunisian_latin']
            for lang in langs:
                if row[lang] > 0:
                    lang_name = self._get_language_name(lang)
                    percentage = (row[lang] / row['total_words']) * 100
                    f.write(f"  - {lang_name}: {row[lang]} mots ({percentage:.1f}%)\n")
            
            if row['tech_codes'] > 0:
                f.write(f"  - Codes techniques: {row['tech_codes']} mots\n")
            if row['unknown'] > 0:
                f.write(f"  - Non identifiés: {row['unknown']} mots\n")
            
            f.write(f"🎯 Confiance: {row['confidence']}%\n")
            
            # Afficher quelques mots examples
            try:
                word_details = json.loads(row['word_details'])
                f.write("🔤 Exemples de mots :\n")
                
                # Grouper par langue
                words_by_lang = {}
                for word_info in word_details[:10]:  # Premier 10 mots
                    lang = word_info['language']
                    if lang not in words_by_lang:
                        words_by_lang[lang] = []
                    words_by_lang[lang].append(word_info['word'])
                
                for lang, words in words_by_lang.items():
                    lang_name = self._get_language_name(lang)
                    f.write(f"  - {lang_name}: {', '.join(words[:5])}\n")
                        
            except (json.JSONDecodeError, KeyError):
                pass
            
            f.write("-" * 50 + "\n\n")
    
    def _write_language_analysis(self, f):
        """Analyser les patterns linguistiques"""
        f.write("🌐 ANALYSE DES PATTERNS LINGUISTIQUES\n")
        f.write("=" * 50 + "\n\n")
        
        # Tickets par langue dominante
        dominant_languages = []
        for idx, row in self.df.iterrows():
            langs = {
                'french': row['french'],
                'english': row['english'], 
                'arabic_script': row['arabic_script'],
                'tunisian_latin': row['tunisian_latin']
            }
            dominant_lang = max(langs, key=langs.get)
            if row[dominant_lang] > 0:
                dominant_languages.append(dominant_lang)
        
        f.write("📊 RÉPARTITION DES TICKETS PAR LANGUE DOMINANTE :\n")
        for lang in set(dominant_languages):
            count = dominant_languages.count(lang)
            percentage = (count / len(dominant_languages)) * 100
            lang_name = self._get_language_name(lang)
            f.write(f"  • {lang_name}: {count} tickets ({percentage:.1f}%)\n")
        
        # Mix linguistique
        mixed_tickets = len([idx for idx, row in self.df.iterrows() 
                           if self._is_mixed_language(row)])
        f.write(f"\n🔀 Tickets multilingues: {mixed_tickets} ({mixed_tickets/len(self.df)*100:.1f}%)\n")
    
    def _write_recommendations(self, f):
        """Écrire des recommandations basées sur l'analyse"""
        f.write("\n💡 RECOMMANDATIONS POUR LE SUPPORT\n")
        f.write("=" * 50 + "\n\n")
        
        total_tickets = len(self.df)
        french_tickets = len(self.df[self.df['french'] > self.df['total_words'] * 0.5])
        arabic_tickets = len(self.df[self.df['arabic_script'] > self.df['total_words'] * 0.5])
        english_tickets = len(self.df[self.df['english'] > self.df['total_words'] * 0.5])
        
        f.write(f"🎯 BESOINS LINGUISTIQUES IDENTIFIÉS :\n")
        f.write(f"  • Support français nécessaire: {french_tickets} tickets\n")
        f.write(f"  • Support arabe nécessaire: {arabic_tickets} tickets\n") 
        f.write(f"  • Support anglais technique: {english_tickets} tickets\n")
        
        if arabic_tickets > 0:
            f.write(f"\n⚠️  {arabic_tickets} tickets en arabe détectés →\n")
            f.write("   Penser à un support bilingue français/arabe\n")
        
        mixed_count = len([idx for idx, row in self.df.iterrows() 
                          if self._is_mixed_language(row)])
        if mixed_count > 0:
            f.write(f"\n🔀 {mixed_count} tickets multilingues →\n")
            f.write("   Adapter les réponses au mélange de langues\n")
    
    def _get_language_name(self, lang_code):
        """Convertir code langue en nom lisible"""
        names = {
            'french': 'Français',
            'english': 'Anglais', 
            'arabic_script': 'Arabe (script)',
            'tunisian_latin': 'Tunisien (latin)',
            'tech_codes': 'Codes techniques',
            'unknown': 'Non identifié'
        }
        return names.get(lang_code, lang_code)
    
    def _is_mixed_language(self, row):
        """Déterminer si un ticket est multilingue"""
        langs = ['french', 'english', 'arabic_script', 'tunisian_latin']
        active_langs = [lang for lang in langs if row[lang] > 0]
        return len(active_langs) >= 2 and max(row[lang] for lang in langs) < row['total_words'] * 0.7

def main():
    reporter = AnalysisReporter('analysis_results.csv')
    reporter.generate_readable_report()
    print("✅ Rapport lisible généré: 'readable_analysis_report.txt'")

if __name__ == "__main__":
    main()