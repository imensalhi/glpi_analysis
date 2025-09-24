import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import configparser
#fichier pour la Préparation de la Connexion DB
class GLPIDatabase:
    def __init__(self, config_file='config.ini'):
        # Charger la configuration
        config = configparser.ConfigParser()
        config.read(config_file)
        
        self.host = config['mysql']['host']
        self.database = config['mysql']['database'] 
        self.user = config['mysql']['user']
        self.password = config['mysql']['password']
        
        self.connection = None
        self.engine = None
    
    def connect(self):
        """Établir la connexion MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                charset='utf8mb4'  # Important pour l'arabe
            )
            
            # Moteur SQLAlchemy pour pandas
            self.engine = create_engine(
                f'mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}?charset=utf8mb4'
            )
            
            print("✅ Connexion à la base GLPI établie")
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ Erreur de connexion : {err}")
            return False
    
    def test_connection(self):
        """Tester la connexion"""
        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM glpi_tickets")
            count = cursor.fetchone()[0]
            print(f"📊 Nombre total de tickets : {count}")
            cursor.close()
            return True
        return False
    
    def close(self):
        """Fermer la connexion"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔒 Connexion fermée")

def explore_glpi_structure(db):
    """Explorer la structure des tables GLPI"""
    
    # Lister toutes les tables
    tables_query = "SHOW TABLES LIKE 'glpi_%'"
    tables = pd.read_sql(tables_query, db.engine)
    print(f"📋 Nombre de tables GLPI : {len(tables)}")
    
    # Analyser la table glpi_tickets
    print("\n🎫 Structure de glpi_tickets :")
    tickets_structure = pd.read_sql("DESCRIBE glpi_tickets", db.engine)
    print(tickets_structure.head(10))  # Afficher les 10 premières colonnes
    
    # Échantillon de données
    print("\n📝 Échantillon de tickets :")
    sample_tickets = pd.read_sql("""
        SELECT id, name, content, status, date, priority 
        FROM glpi_tickets 
        ORDER BY date DESC 
        LIMIT 5
    """, db.engine)
    print(sample_tickets)
    
    # Analyser les champs texte
    print("\n📊 Statistiques des champs texte :")
    text_stats = pd.read_sql("""
        SELECT 
            COUNT(*) as total_tickets,
            COUNT(name) as tickets_with_title,
            COUNT(content) as tickets_with_content,
            AVG(CHAR_LENGTH(name)) as avg_title_length,
            AVG(CHAR_LENGTH(content)) as avg_content_length
        FROM glpi_tickets
        WHERE name IS NOT NULL OR content IS NOT NULL
    """, db.engine)
    print(text_stats)

def get_text_data_sample(db, limit=10):
    """Récupérer un échantillon de données texte"""
    
    query = """
    SELECT
        t.id,
        t.name as title,
        t.content as description,
        t.date,
        t.status,
        e.name as entity_name,
        c.name as category_name
    FROM glpi_tickets t
    LEFT JOIN glpi_entities e ON t.entities_id = e.id
    LEFT JOIN glpi_itilcategories c ON t.itilcategories_id = c.id
    WHERE (t.name IS NOT NULL AND t.name != '') 
       OR (t.content IS NOT NULL AND t.content != '')
    ORDER BY t.date DESC
    LIMIT %s
    """
    
    return pd.read_sql(query, db.engine, params=(limit,))
