from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import sys

# Ajouter le dossier parent au PATH pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.glpi_database import GLPIDatabase
from preprocessing.glpi_data_extractor import GLPIDataExtractor
from preprocessing.text_cleaner import TextCleaner
from preprocessing.language_dictionaries import LanguageDictionaries
from preprocessing.arabic_detector import ArabicDetector
from preprocessing.language_classifier import LanguageClassifier

app = Flask(__name__, static_folder='../static', static_url_path='/')
CORS(app)

# Initialiser les composants avec le bon chemin
try:
    db = GLPIDatabase('config.ini')
    extractor = GLPIDataExtractor(db)
    text_cleaner = TextCleaner()
    dictionaries = LanguageDictionaries()
    arabic_detector = ArabicDetector()
    classifier = LanguageClassifier(dictionaries.dictionaries, arabic_detector, text_cleaner)
    print("✅ Tous les composants initialisés avec succès")
except Exception as e:
    print(f"❌ Erreur initialisation: {e}")
    sys.exit(1)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    try:
        if not db.connect():
            return jsonify({'error': 'Database connection failed'}), 500
        
        df = extractor.extract_tickets_data()
        df = extractor.prepare_dataset(df)
        
        # Convertir en format attendu par l'interface
        tickets = []
        for idx, row in df.iterrows():
            tickets.append({
                'id': int(row['id']),
                'clean_title': str(row['clean_title']),
                'full_text': str(row['full_text'])
            })
        
        return jsonify(tickets)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.connection:
            db.close()

@app.route('/api/analyze/<int:ticket_id>', methods=['GET'])
def analyze_ticket(ticket_id):
    try:
        if not db.connect():
            return jsonify({'error': 'Database connection failed'}), 500
        
        df = extractor.extract_tickets_data()
        df = extractor.prepare_dataset(df)
        ticket = df[df['id'] == ticket_id]
        
        if ticket.empty:
            return jsonify({'error': 'Ticket not found'}), 404
        
        ticket_text = ticket.iloc[0]['full_text']
        analysis = classifier.analyze_text(ticket_text)
        
        # MODIFICATION: Adapter les noms des champs pour correspondre au nouveau format
        # Renommer les champs pour la compatibilité avec l'interface
        standardized_analysis = {
            'ticket_id': ticket_id,
            'title': ticket.iloc[0]['clean_title'],
            'total_words': analysis.get('total_words', 0),
            'french': analysis.get('french', 0),
            'english': analysis.get('english', 0),
            'arabic_script': analysis.get('arabic_script', 0),
            'tunisian_latin': analysis.get('tunisian_latin', 0),
            'technical_codes': analysis.get('technical_codes', 0),  # NOUVEAU: Codes techniques
            'tech_details': analysis.get('tech_details', {}),      # NOUVEAU: Détail par type
            'unknown': analysis.get('unknown', 0),
            'word_details': analysis.get('word_details', []),
            'identified_tech_codes': analysis.get('identified_tech_codes', {}),  # NOUVEAU
            'confidence': classifier.calculate_confidence(analysis)
        }
        
        return jsonify(standardized_analysis)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.connection:
            db.close()

@app.route('/api/analyze-all', methods=['POST'])
def analyze_all_tickets():
    try:
        if not db.connect():
            return jsonify({'error': 'Database connection failed'}), 500
        
        df = extractor.extract_tickets_data()
        df = extractor.prepare_dataset(df)
        
        results = []
        for idx, row in df.iterrows():
            ticket_analysis = classifier.analyze_text(row['full_text'])
            
            # MODIFICATION: Standardiser les noms des champs
            standardized_analysis = {
                'ticket_id': int(row['id']),
                'title': str(row['clean_title']),
                'total_words': ticket_analysis.get('total_words', 0),
                'french': ticket_analysis.get('french', 0),
                'english': ticket_analysis.get('english', 0),
                'arabic_script': ticket_analysis.get('arabic_script', 0),
                'tunisian_latin': ticket_analysis.get('tunisian_latin', 0),
                'technical_codes': ticket_analysis.get('technical_codes', 0),  # NOUVEAU
                'tech_details': ticket_analysis.get('tech_details', {}),
                'unknown': ticket_analysis.get('unknown', 0),
                'word_details': ticket_analysis.get('word_details', []),
                'identified_tech_codes': ticket_analysis.get('identified_tech_codes', {}),
                'confidence': classifier.calculate_confidence(ticket_analysis)
            }
            results.append(standardized_analysis)
        
        # Calculer les statistiques globales avec les nouveaux champs
        results_df = pd.DataFrame(results)
        total_tickets = len(results_df)
        total_words = results_df['total_words'].sum() if len(results_df) > 0 else 0
        
        # MODIFICATION: Inclure les codes techniques dans les stats
        stats = {
            'total_tickets': total_tickets,
            'total_words': int(total_words),
            'french': int(results_df['french'].sum()) if len(results_df) > 0 else 0,
            'english': int(results_df['english'].sum()) if len(results_df) > 0 else 0,
            'arabic_script': int(results_df['arabic_script'].sum()) if len(results_df) > 0 else 0,
            'tunisian_latin': int(results_df['tunisian_latin'].sum()) if len(results_df) > 0 else 0,
            'technical_codes': int(results_df['technical_codes'].sum()) if len(results_df) > 0 else 0,  # NOUVEAU
            'unknown': int(results_df['unknown'].sum()) if len(results_df) > 0 else 0,
            'avg_confidence': round(results_df['confidence'].mean(), 2) if len(results_df) > 0 else 0
        }
        
        # NOUVEAU: Ajouter les statistiques des codes techniques
        tech_stats = {}
        if len(results_df) > 0:
            # Compter tous les types de codes techniques
            all_tech_details = {}
            for _, row in results_df.iterrows():
                tech_details = row.get('tech_details', {})
                for tech_type, count in tech_details.items():
                    if tech_type in all_tech_details:
                        all_tech_details[tech_type] += count
                    else:
                        all_tech_details[tech_type] = count
            
            tech_stats = {
                'total_tech_codes': stats['technical_codes'],
                'tech_breakdown': all_tech_details,
                'tickets_with_tech': len([r for r in results if r['technical_codes'] > 0])
            }
        
        return jsonify({
            'results': results, 
            'stats': stats,
            'tech_stats': tech_stats  # NOUVEAU: Statistiques techniques séparées
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.connection:
            db.close()

@app.route('/api/tech-codes-analysis', methods=['GET'])
def get_tech_codes_analysis():
    """NOUVEAU: Endpoint spécialisé pour l'analyse des codes techniques"""
    try:
        if not db.connect():
            return jsonify({'error': 'Database connection failed'}), 500
        
        df = extractor.extract_tickets_data()
        df = extractor.prepare_dataset(df)
        
        # Analyser tous les tickets pour les codes techniques
        tech_analysis = {
            'total_tickets_analyzed': 0,
            'tickets_with_tech_codes': 0,
            'total_tech_codes_found': 0,
            'tech_types_breakdown': {},
            'examples_by_type': {},
            'top_tickets_with_tech': []
        }
        
        ticket_tech_counts = []
        
        for idx, row in df.iterrows():
            ticket_analysis = classifier.analyze_text(row['full_text'])
            tech_analysis['total_tickets_analyzed'] += 1
            
            tech_codes_count = ticket_analysis.get('technical_codes', 0)
            tech_details = ticket_analysis.get('tech_details', {})
            identified_codes = ticket_analysis.get('identified_tech_codes', {})
            
            if tech_codes_count > 0:
                tech_analysis['tickets_with_tech_codes'] += 1
                tech_analysis['total_tech_codes_found'] += tech_codes_count
                
                # Compter par type
                for tech_type, count in tech_details.items():
                    if tech_type in tech_analysis['tech_types_breakdown']:
                        tech_analysis['tech_types_breakdown'][tech_type] += count
                    else:
                        tech_analysis['tech_types_breakdown'][tech_type] = count
                
                # Collecter des exemples
                for tech_type, codes in identified_codes.items():
                    if tech_type not in tech_analysis['examples_by_type']:
                        tech_analysis['examples_by_type'][tech_type] = set()
                    tech_analysis['examples_by_type'][tech_type].update(codes[:3])  # Max 3 exemples par type
                
                # Garder trace des tickets avec le plus de codes techniques
                ticket_tech_counts.append({
                    'ticket_id': int(row['id']),
                    'title': str(row['clean_title']),
                    'tech_count': tech_codes_count,
                    'tech_details': tech_details
                })
        
        # Convertir les sets en listes pour la sérialisation JSON
        for tech_type in tech_analysis['examples_by_type']:
            tech_analysis['examples_by_type'][tech_type] = list(tech_analysis['examples_by_type'][tech_type])
        
        # Top 5 des tickets avec le plus de codes techniques
        tech_analysis['top_tickets_with_tech'] = sorted(
            ticket_tech_counts, 
            key=lambda x: x['tech_count'], 
            reverse=True
        )[:5]
        
        return jsonify(tech_analysis)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.connection:
            db.close()

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Flask...")
    print("📡 Interface disponible sur: http://localhost:5001")
    print("💻 Support des codes techniques activé")
    app.run(debug=True, host='0.0.0.0', port=5001)