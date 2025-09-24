import streamlit as st
import pandas as pd
import time
import mysql.connector
import json  # Ajout du module json
import warnings
from glpi_database import GLPIDatabase
from glpi_data_extractor import GLPIDataExtractor
from text_cleaner import TextCleaner
from language_dictionaries import LanguageDictionaries
from arabic_detector import ArabicDetector
from language_classifier import LanguageClassifier

# Supprimer le warning pyarrow
warnings.filterwarnings("ignore", category=FutureWarning, module="pyarrow")

# CSS pour un style chic et moderne
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f4f8;
        color: #333;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stSelectbox, .stTextInput, .stTextArea {
        border-radius: 8px;
    }
    .block-container {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2E7D32;
    }
    .stTable {
        background-color: #ffffff;
        border-collapse: collapse;
        width: 100%;
    }
    .stTable th, .stTable td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .stTable th {
        background-color: #4CAF50;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Fonction pour extraire les tickets
@st.cache_data(ttl=10)
def get_tickets():
    db = GLPIDatabase('config.ini')
    if not db.connect():
        st.error("❌ Erreur de connexion à la base GLPI")
        return pd.DataFrame()
    
    extractor = GLPIDataExtractor(db)
    df = extractor.extract_tickets_data()
    df = extractor.prepare_dataset(df)
    db.close()
    return df

# Initialiser l'analyseur
@st.cache_resource
def get_classifier():
    text_cleaner = TextCleaner()
    dictionaries = LanguageDictionaries()
    arabic_detector = ArabicDetector()
    return LanguageClassifier(dictionaries.dictionaries, arabic_detector, text_cleaner)

# Fonction pour ajouter un ticket
def add_ticket(title, content):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # À adapter via config.ini
            database="glpi_db"
        )
        cursor = conn.cursor()
        query = "INSERT INTO glpi_tickets (name, content, date, users_id_recipient, status) VALUES (%s, %s, NOW(), %s, %s)"
        cursor.execute(query, (title, content, 1, 1))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("✅ Nouveau ticket ajouté !")
    except Exception as e:
        st.error(f"❌ Erreur lors de l'ajout: {e}")

# Fonction pour grouper les mots
def group_words_by_language(word_details):
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
        if lang in groups:
            groups[lang].append(detail['word'])
    return groups

# Interface Principale
st.title("🎯 Analyse Linguistique des Tickets GLPI")
st.markdown("Sélectionnez un ticket pour voir l'analyse détaillée ou ajoutez un nouveau ticket. L'app se rafraîchit toutes les 10s !")

# Polling pour temps réel
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 10:
    with st.spinner("🔄 Rafraîchissement des tickets..."):
        st.session_state.last_refresh = time.time()
        st.experimental_rerun()

# Ajouter un Ticket
with st.expander("➕ Ajouter un Nouveau Ticket"):
    new_title = st.text_input("Titre du ticket")
    new_content = st.text_area("Contenu du ticket")
    if st.button("Ajouter"):
        if new_title and new_content:
            add_ticket(new_title, new_content)
            st.experimental_rerun()
        else:
            st.warning("Veuillez remplir le titre et le contenu.")

# Récupérer les tickets
df_tickets = get_tickets()

if df_tickets.empty:
    st.warning("Aucun ticket trouvé dans la base GLPI. Ajoutez-en un ci-dessus !")
else:
    # Sélection des Tickets
    ticket_options = [f"#{row['id']} - {row['clean_title'][:50]}..." for _, row in df_tickets.iterrows()]
    selected_ticket = st.selectbox("Choisissez un ticket :", ticket_options)
    
    if selected_ticket:
        ticket_id = int(selected_ticket.split(" - ")[0][1:])
        ticket_row = df_tickets[df_tickets['id'] == ticket_id].iloc[0]
        
        # Analyser le ticket
        classifier = get_classifier()
        analysis = classifier.analyze_text(ticket_row['full_text'])
        grouped_words = group_words_by_language(analysis['word_details'])
        
        # Détails du Ticket
        st.subheader("📋 Détails du Ticket")
        st.write(f"**Titre :** {ticket_row['clean_title']}")
        st.write(f"**Texte Complet :** {ticket_row['full_text']}")
        st.write(f"**Total Mots :** {analysis['total_words']}")
        st.write(f"**Confiance :** {classifier.calculate_confidence(analysis)}%")
        
        # Stats en Table
        st.subheader("📊 Statistiques par Langue/Catégorie")
        stats_data = {
            'Langue/Catégorie': ['Français', 'Anglais', 'Arabe (Script)', 'Tunisien Latin', 'Codes Techniques', 'Inconnus'],
            'Nombre de Mots': [
                analysis['french'],
                analysis['english'],
                analysis['arabic_script'],
                analysis['tunisian_latin'],
                analysis['tech_codes'],
                analysis['unknown']
            ],
            'Pourcentage (%)': [
                round(analysis['french'] / analysis['total_words'] * 100, 1) if analysis['total_words'] > 0 else 0,
                round(analysis['english'] / analysis['total_words'] * 100, 1) if analysis['total_words'] > 0 else 0,
                round(analysis['arabic_script'] / analysis['total_words'] * 100, 1) if analysis['total_words'] > 0 else 0,
                round(analysis['tunisian_latin'] / analysis['total_words'] * 100, 1) if analysis['total_words'] > 0 else 0,
                round(analysis['tech_codes'] / analysis['total_words'] * 100, 1) if analysis['total_words'] > 0 else 0,
                round(analysis['unknown'] / analysis['total_words'] * 100, 1) if analysis['total_words'] > 0 else 0
            ]
        }
        stats_df = pd.DataFrame(stats_data)
        st.table(stats_df)
        
        # Mots Classifiés en Table
        st.subheader("🔍 Mots Classifiés")
        try:
            word_data = [{'Mot': detail['word'], 'Catégorie': detail['language'].capitalize()} for detail in analysis['word_details']]
            word_df = pd.DataFrame(word_data)
            if not word_df.empty:
                st.table(word_df)
            else:
                st.info("Aucun mot à afficher.")
        except Exception as e:
            st.error(f"❌ Erreur lors de l'affichage des mots: {e}")
        
        # Codes Techniques
        if analysis['extracted_tech_codes']:
            st.subheader("💻 Codes Techniques Extraits")
            st.json(analysis['extracted_tech_codes'])
        
        # Bouton pour Exporter l'Analyse
        st.subheader("📥 Exporter l'Analyse")
        analysis_data = {
            'ticket_id': ticket_id,
            'title': ticket_row['clean_title'],
            'full_text': ticket_row['full_text'],
            **analysis
        }
        analysis_df = pd.DataFrame([analysis_data])
        try:
            analysis_df['grouped_words'] = analysis_df['word_details'].apply(lambda x: json.dumps(group_words_by_language(x)))
        except Exception as e:
            st.error(f"❌ Erreur lors de la sérialisation JSON: {e}")
            analysis_df['grouped_words'] = None
        csv = analysis_df.to_csv(index=False)
        st.download_button(
            label="Télécharger l'analyse en CSV",
            data=csv,
            file_name=f"ticket_{ticket_id}_analysis.csv",
            mime="text/csv"
        )

# Pied de Page
st.markdown("---")
st.info("App rafraîchie automatiquement toutes les 10s pour détecter les nouveaux tickets. Ajoutez-en un dans GLPI ou ci-dessus !")