# glpi_data_extractor.py
# Extraction des données
import pandas as pd
import re
import html
from datetime import datetime
# fichier pour Extrait les tickets via SQL nettoie le HTML (ex. supprime balises, décode entités comme &), combine titre + contenu en full_text.
class GLPIDataExtractor:
    def __init__(self, db_connection):
        self.db = db_connection
        
    def extract_tickets_data(self, limit=None):
        """Extraire tous les tickets avec titre et contenu"""
        query = """
        SELECT 
            id,
            name as title,
            content,
            date as created_date,
            status,
            priority
        FROM glpi_tickets 
        WHERE (name IS NOT NULL AND name != '') 
           OR (content IS NOT NULL AND content != '')
        ORDER BY date DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        df = pd.read_sql(query, self.db.engine)
        print(f"{len(df)} tickets extraits")
        
        return df
    
    def clean_html_content(self, text):
        """Nettoyer le contenu HTML"""
        if pd.isna(text) or text == '':
            return ''
            
        # Décoder les entités HTML
        text = html.unescape(text)
        
        # Supprimer les balises HTML
        text = re.sub(r'<[^>]+>', '', text)
        
        # Nettoyer les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def prepare_dataset(self, df):
        """Préparer le dataset pour l'analyse"""
        # Nettoyer le HTML
        df['clean_title'] = df['title'].apply(self.clean_html_content)
        df['clean_content'] = df['content'].apply(self.clean_html_content)
        
        # Combiner titre et contenu
        df['full_text'] = df['clean_title'] + ' ' + df['clean_content']
        df['full_text'] = df['full_text'].str.strip()
        
        # Supprimer les tickets vides
        df = df[df['full_text'] != ''].copy()
        
        print(f" Dataset préparé: {len(df)} tickets valides")
        
        return df