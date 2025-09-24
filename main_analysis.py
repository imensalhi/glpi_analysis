# main_analysis.py
from glpi_database import GLPIDatabase, explore_glpi_structure, get_text_data_sample

def main():
    # Initialiser la connexion
    db = GLPIDatabase('config.ini')
    
    if db.connect():
        # Tester la connexion
        db.test_connection()
        
        # Explorer la structure
        explore_glpi_structure(db)
        
        # Récupérer un échantillon
        print("\n📋 Échantillon de données texte :")
        sample = get_text_data_sample(db, 10)
        
        # Afficher les données pour analyse
        for idx, row in sample.iterrows():
            print(f"\n--- Ticket #{row['id']} ---")
            print(f"Titre: {row['title']}")
            if row['description']:
                print(f"Description: {str(row['description'])[:200]}...")
            else:
                print(f"Description: [VIDE]")
            print(f"Catégorie: {row['category_name']}")
            print(f"Date: {row['date']}")
            print(f"Statut: {row['status']}")
        
        # Analyser l'encodage et le format
        analyze_text_characteristics(sample)
        
        # Fermer la connexion
        db.close()
        
        return sample
    else:
        print("❌ Impossible de se connecter à la base")
        return None

def analyze_text_characteristics(sample_data):
    """Analyser les caractéristiques du texte"""
    print("\n🔍 ANALYSE DES CARACTÉRISTIQUES DU TEXTE")
    print("=" * 50)
    
    # Vérifier l'encodage
    arabic_chars = set('ابتثجحخدذرزسشصضطظعغفقكلمنهوي')
    
    for idx, row in sample_data.iterrows():
        title = str(row['title']) if row['title'] else ""
        description = str(row['description']) if row['description'] else ""
        
        # Détecter l'arabe
        title_arabic_chars = [char for char in title if char in arabic_chars]
        desc_arabic_chars = [char for char in description if char in arabic_chars]
        
        # Vérifier le format HTML
        is_html = '<' in description and '>' in description
        
        print(f"\n📌 Ticket #{row['id']}:")
        print(f"   Titre: {len(title)} caractères, {len(title_arabic_chars)} caractères arabes")
        print(f"   Description: {len(description)} caractères, {len(desc_arabic_chars)} caractères arabes")
        print(f"   Contient du HTML: {'OUI' if is_html else 'NON'}")

if __name__ == "__main__":
    sample_data = main()
