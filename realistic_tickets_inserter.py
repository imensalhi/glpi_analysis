# corrected_tickets_inserter.py
import mysql.connector
from datetime import datetime, timedelta
import random

class CorrectedTicketsInserter:
    def __init__(self, db_connection):
        self.db = db_connection
        self.inserted_count = 0
        
        # Tous tes tickets réalistes
        self.tickets_data = [
            # Français pur
            {"title": "Problème imprimante", "content": "Bonjour, mon imprimante ne répond plus depuis ce matin. Elle est bien connectée mais rien ne sort.", "category": "french_pure"},
            {"title": "Mot de passe oublié", "content": "J'ai oublié mon mot de passe Windows, pouvez-vous le réinitialiser ?", "category": "french_pure"},
            {"title": "Logiciel comptabilité", "content": "Le logiciel de comptabilité ne s'ouvre plus, il affiche une erreur \"DLL manquante\".", "category": "french_pure"},
            {"title": "Écran noir", "content": "Mon écran reste noir au démarrage, pourtant le PC semble allumé.", "category": "french_pure"},
            {"title": "Serveur partagé", "content": "Impossible d'accéder à mes fichiers sur le serveur partagé.", "category": "french_pure"},
            {"title": "Problème clavier", "content": "Le clavier de mon portable ne fonctionne plus correctement, certaines touches ne répondent pas.", "category": "french_pure"},
            {"title": "Connexion VPN", "content": "Je n'arrive pas à me connecter au VPN depuis chez moi.", "category": "french_pure"},
            {"title": "Outlook plantage", "content": "Mon Outlook plante à chaque fois que j'essaie d'envoyer un mail.", "category": "french_pure"},
            {"title": "Réseau lent", "content": "Le réseau est très lent aujourd'hui, est-ce qu'il y a une maintenance ?", "category": "french_pure"},
            {"title": "Antivirus expiré", "content": "J'ai besoin d'une mise à jour de mon antivirus, il est expiré.", "category": "french_pure"},
            
            # Anglais pur
            {"title": "Laptop won't boot", "content": "Hello, my laptop won't boot. It's stuck on the manufacturer logo.", "category": "english_pure"},
            {"title": "Access Denied", "content": "I can't access the shared drive. It says \"Access Denied\".", "category": "english_pure"},
            {"title": "Mouse issue", "content": "My mouse is acting weird, it double-clicks randomly.", "category": "english_pure"},
            {"title": "Wi-Fi disconnecting", "content": "The Wi-Fi keeps disconnecting every few minutes.", "category": "english_pure"},
            {"title": "Admin rights needed", "content": "I need admin rights to install Adobe Reader.", "category": "english_pure"},
            {"title": "Excel corruption", "content": "My Excel file got corrupted, can you recover it?", "category": "english_pure"},
            {"title": "Printer jammed", "content": "The printer in room 204 is jammed again.", "category": "english_pure"},
            {"title": "Blue screen error", "content": "I'm getting a blue screen with \"IRQL_NOT_LESS_OR_EQUAL\".", "category": "english_pure"},
            {"title": "Email configuration", "content": "Can you help me configure my email on my phone?", "category": "english_pure"},
            {"title": "Deleted folder", "content": "I accidentally deleted a folder from the server. Can it be restored?", "category": "english_pure"},
            
            # Arabe tunisien pur
            {"title": "مشكل الحاسوب", "content": "الحاسوب متاعي ما عادش يحب يشعل، يعطيني صوت متاع erreur.", "category": "arabic_pure"},
            {"title": "مشكل الطابعة", "content": "الطابعة ما تطبعش، الورقة تدخل وتخرج بيضاء.", "category": "arabic_pure"},
            {"title": "كلمة السر الويفي", "content": "نحب نبدل كلمة السر متاع الويفي، كيفاش نعمل؟", "category": "arabic_pure"},
            {"title": "مشكل Outlook", "content": "Outlook ما يبعثش المايلات، يعطيني erreur 0x800ccc0e.", "category": "arabic_pure"},
            {"title": "مشكل الشبكة", "content": "فما مشكل في الشبكة، ما نجمش نفتح حتى موقع.", "category": "arabic_pure"},
            {"title": "برنامج جديد", "content": "نحب نركب برنامج جديد، يلزمني صلاحيات administrateur.", "category": "arabic_pure"},
            {"title": "فايروس", "content": "فما فايروس في الجهاز، كل مرة يطلعلي نافذة غريبة.", "category": "arabic_pure"},
            {"title": "الجهاز يسخن", "content": "الحاسوب يسخن برشة ويطفى وحدو.", "category": "arabic_pure"},
            {"title": "مشاركة الفايلات", "content": "نحب نعمل partage للفايلات بين زوز حواسيب.", "category": "arabic_pure"},
            {"title": "مشكل الكاميرا", "content": "فما مشكل في الكاميرا، ما تشتغلش في Teams.", "category": "arabic_pure"},
            
            # Arabe tunisien en lettres latines
            {"title": "PC startup problem", "content": "Pc ma y7ebch ydemarre, yb9a stuck f logo.", "category": "tunisian_latin"},
            {"title": "Outlook mail issue", "content": "Outlook ma yeb3athch les mails, erreur 0x800ccc0e.", "category": "tunisian_latin"},
            {"title": "Password reset", "content": "N7eb na3mel reset l mot de passe Windows.", "category": "tunisian_latin"},
            {"title": "Wifi problem", "content": "Wifi yta7 kol 5 min, chnowa el solution ?", "category": "tunisian_latin"},
            {"title": "Printer jammed", "content": "Printer ta3na fi bureau 3 jammed, please check.", "category": "tunisian_latin"},
            
            # Français + codes techniques
            {"title": "Erreur Visual Studio", "content": "Bonjour, j'ai une erreur \"0x80070005\" quand j'essaie d'installer Visual Studio.", "category": "french_tech"},
            {"title": "Script Python", "content": "Le script Python plante avec \"ModuleNotFoundError: No module named 'pandas'\".", "category": "french_tech"},
            {"title": "BOOTMGR missing", "content": "Mon PC affiche \"BOOTMGR is missing\", je ne peux pas démarrer.", "category": "french_tech"},
            {"title": "Port firewall", "content": "J'ai besoin d'ouvrir le port 443 sur mon firewall pour accéder à l'API.", "category": "french_tech"},
            {"title": "Problème NAS", "content": "Le NAS ne monte plus sur le réseau, pourtant il est bien branché.", "category": "french_tech"},
            
            # Anglais + codes techniques
            {"title": "403 Forbidden error", "content": "Getting \"403 Forbidden\" when accessing internal web app.", "category": "english_tech"},
            {"title": "SQL syntax error", "content": "My SQL query returns \"Syntax error near 'FROM'\".", "category": "english_tech"},
            {"title": "Boot device error", "content": "Laptop shows \"No bootable device found\", need urgent fix.", "category": "english_tech"},
            
            # Arabe tunisien + codes techniques
            {"title": "مشكل Outlook SMTP", "content": "Outlook ma yeb3athch, erreur SMTP 550.", "category": "arabic_tech"},
            {"title": "Blue screen", "content": "PC y3tini blue screen: \"KERNEL_SECURITY_CHECK_FAILURE\".", "category": "arabic_tech"},
            
            # Arabe en lettres latines + codes techniques
            {"title": "PC boot error", "content": "Pc y3tini erreur \"0xc000000f\", ma y7ebch ydemarre.", "category": "tunisian_latin_tech"},
            {"title": "WiFi DNS error", "content": "Wifi yta7 w y3tini \"DNS_PROBE_FINISHED_NO_INTERNET\".", "category": "tunisian_latin_tech"},
            
            # Mixte
            {"title": "Disk boot failure", "content": "Hello, mon PC affiche \"Disk boot failure\", please help urgentement.", "category": "mixed"},
            {"title": "Outlook SMTP error", "content": "Salam, Outlook ma yeb3athch les mails, SMTP error 0x80042109, chnowa el solution ?", "category": "mixed"},
            {"title": "Python script error", "content": "Hey, j'ai un souci avec mon script Python, ça dit \"IndentationError\", w ma fahmtch chnowa ghalta.", "category": "mixed"},
            
            # Tickets supplémentaires réalistes
            {"title": "Ordinateur ne s'allume plus", "content": "Bonjour, mon ordinateur ne s'allume plus du tout depuis ce matin. J'ai essayé de le brancher ailleurs, rien n'y fait.", "category": "french_pure"},
            {"title": "HP LaserJet issue", "content": "Hi there, my printer isn't working properly. It keeps jamming paper every time I try to print. Model is HP LaserJet 400.", "category": "english_pure"},
            {"title": "مشكل الويفي", "content": "سلام، الويفي عندي ما يخدمش كيف كيف، يقطع كل شوية. شنوة الحل؟", "category": "arabic_pure"},
            {"title": "PC hang problem", "content": "chwaya chwaya el pc yhang, ma3andich 3lach. aide moi stp.", "category": "tunisian_latin"}
        ]

    def check_table_structure(self):
        """Vérifier la structure de la table glpi_tickets"""
        print("🔍 Vérification de la structure de la table...")
        
        cursor = self.db.connection.cursor()
        cursor.execute("DESCRIBE glpi_tickets")
        columns = cursor.fetchall()
        cursor.close()
        
        column_names = [col[0] for col in columns]
        print(f"✅ Colonnes disponibles: {', '.join(column_names[:10])}...")
        
        return column_names

    def insert_all_tickets(self):
        """Insérer tous les tickets avec la structure correcte"""
        if not self.db.connection or not self.db.connection.is_connected():
            print("❌ Pas de connexion à la base GLPI")
            return False

        # Vérifier la structure
        available_columns = self.check_table_structure()
        
        cursor = self.db.connection.cursor()
        
        # Requête simplifiée avec seulement les colonnes essentielles
        insert_query = """
        INSERT INTO glpi_tickets (
            name, content, date, date_mod, status, priority, 
            urgency, impact, entities_id, type, date_creation
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        print(f"🚀 Insertion de {len(self.tickets_data)} tickets réalistes...")
        print("=" * 60)
        
        success_count = 0
        failed_count = 0
        
        # Répartition des priorités et statuts
        priorities = [2, 3, 4]  # Faible à élevé 
        statuses = [1, 2]       # Nouveau, En cours
        
        for i, ticket in enumerate(self.tickets_data, 1):
            try:
                # Varier les dates
                date_creation = datetime.now() - timedelta(days=random.randint(0, 30))
                
                # Format HTML simple pour le contenu
                html_content = f'<p dir="auto" style="white-space: pre-wrap;">{ticket["content"]}</p>'
                
                # Données du ticket avec structure correcte
                priority = random.choice(priorities)
                data = (
                    ticket['title'],           # name
                    html_content,             # content
                    date_creation,            # date
                    date_creation,            # date_mod
                    random.choice(statuses),  # status
                    priority,                 # priority
                    priority,                 # urgency (même que priority)
                    priority,                 # impact (même que priority)
                    0,                        # entities_id (entité par défaut)
                    1,                        # type (1 = Incident)
                    date_creation             # date_creation
                )
                
                cursor.execute(insert_query, data)
                success_count += 1
                
                # Afficher progression
                if i % 10 == 0:
                    print(f"   ✅ {i}/{len(self.tickets_data)} tickets traités...")
                
                # Afficher détails pour quelques tickets
                if i <= 5:
                    print(f"   📝 Ticket #{i}: [{ticket['category']}] {ticket['title'][:50]}...")
                    
            except Exception as e:
                failed_count += 1
                print(f"   ❌ Erreur ticket #{i}: {e}")
        
        # Valider les insertions
        try:
            self.db.connection.commit()
            print(f"\n🎉 SUCCÈS: {success_count} tickets insérés dans GLPI!")
            
            if failed_count > 0:
                print(f"⚠️  {failed_count} tickets ont échoué")
            
            self.inserted_count = success_count
            
        except Exception as e:
            print(f"❌ Erreur lors de la validation: {e}")
            self.db.connection.rollback()
            return False
        
        finally:
            cursor.close()
        
        return success_count > 0

    def verify_insertion(self):
        """Vérifier les tickets insérés"""
        if not self.db.connection:
            return False
        
        cursor = self.db.connection.cursor()
        
        # Compter les tickets récents
        cursor.execute("""
            SELECT COUNT(*) FROM glpi_tickets 
            WHERE date >= DATE_SUB(NOW(), INTERVAL 2 HOUR)
        """)
        
        recent_count = cursor.fetchone()[0]
        
        # Échantillon des tickets
        cursor.execute("""
            SELECT name, LEFT(content, 100) as preview, date
            FROM glpi_tickets 
            WHERE date >= DATE_SUB(NOW(), INTERVAL 2 HOUR)
            ORDER BY date DESC 
            LIMIT 8
        """)
        
        sample_tickets = cursor.fetchall()
        cursor.close()
        
        print(f"\n🔍 Vérification: {recent_count} tickets créés récemment")
        print("\n📋 Échantillon des derniers tickets:")
        print("-" * 50)
        
        for i, (title, preview, date) in enumerate(sample_tickets, 1):
            clean_preview = preview.replace('<p dir="auto" style="white-space: pre-wrap;">', '').replace('</p>', '')
            print(f"{i}. {title}")
            print(f"   {clean_preview[:70]}...")
            print(f"   📅 {date}\n")
        
        return recent_count > 0

    def show_statistics(self):
        """Afficher les statistiques par catégorie"""
        categories = {}
        for ticket in self.tickets_data:
            cat = ticket['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"\n📊 STATISTIQUES D'INSERTION")
        print("=" * 40)
        print(f"Total tickets insérés: {self.inserted_count}")
        print(f"\nRépartition par catégorie:")
        
        for category, count in categories.items():
            percentage = (count / len(self.tickets_data)) * 100
            print(f"  • {category}: {count} tickets ({percentage:.1f}%)")


def main():
    from glpi_database import GLPIDatabase
    
    print("🎯 INSERTION DES TICKETS RÉALISTES DANS GLPI (VERSION CORRIGÉE)")
    print("=" * 65)
    
    # Connexion à la base
    db = GLPIDatabase('config.ini')
    
    if not db.connect():
        print("❌ Impossible de se connecter à GLPI")
        return
    
    # Tester la connexion
    if not db.test_connection():
        print("❌ Problème de connexion GLPI")
        db.close()
        return
    
    # Créer l'inserteur corrigé
    inserter = CorrectedTicketsInserter(db)
    
    print(f"📋 Prêt à insérer {len(inserter.tickets_data)} tickets réalistes")
    print("   • Structure SQL adaptée à ta version GLPI")
    print("   • Colonnes vérifiées automatiquement")
    print("   • Dates variées (30 derniers jours)")
    
    # Demander confirmation
    choice = input(f"\n❓ Continuer avec l'insertion ? (y/n): ")
    
    if choice.lower() != 'y':
        print("⏸️  Insertion annulée")
        db.close()
        return
    
    # Insérer les tickets
    success = inserter.insert_all_tickets()
    
    if success:
        # Vérifier l'insertion
        inserter.verify_insertion()
        
        # Afficher les statistiques
        inserter.show_statistics()
        
        print(f"\n🎉 MISSION ACCOMPLIE!")
        print("✅ Dataset multilingue créé dans GLPI")
        print("🔄 Prêt pour le développement de l'algorithme d'analyse!")
        
    else:
        print("❌ Erreur lors de l'insertion des tickets")
    
    db.close()

if __name__ == "__main__":
    main()