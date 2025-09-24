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
    db = GLPIDatabase('../config.ini')
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
        
        # Ajouter les métadonnées
        analysis['ticket_id'] = ticket_id
        analysis['title'] = ticket.iloc[0]['clean_title']
        analysis['confidence'] = classifier.calculate_confidence(analysis)
        
        return jsonify(analysis)
        
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
            ticket_analysis['ticket_id'] = int(row['id'])
            ticket_analysis['title'] = str(row['clean_title'])
            ticket_analysis['confidence'] = classifier.calculate_confidence(ticket_analysis)
            results.append(ticket_analysis)
        
        # Calculer les statistiques globales
        results_df = pd.DataFrame(results)
        total_tickets = len(results_df)
        total_words = results_df['total_words'].sum() if len(results_df) > 0 else 0
        
        stats = {
            'total_tickets': total_tickets,
            'total_words': int(total_words),
            'french': int(results_df['french'].sum()) if len(results_df) > 0 else 0,
            'english': int(results_df['english'].sum()) if len(results_df) > 0 else 0,
            'arabic_script': int(results_df['arabic_script'].sum()) if len(results_df) > 0 else 0,
            'tunisian_latin': int(results_df['tunisian_latin'].sum()) if len(results_df) > 0 else 0,
            'tech_codes': int(results_df['tech_codes'].sum()) if len(results_df) > 0 else 0,
            'unknown': int(results_df['unknown'].sum()) if len(results_df) > 0 else 0,
            'avg_confidence': round(results_df['confidence'].mean(), 2) if len(results_df) > 0 else 0
        }
        
        return jsonify({'results': results, 'stats': stats})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.connection:
            db.close()

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Flask...")
    print("📡 Interface disponible sur: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)