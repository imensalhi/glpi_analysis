import mysql.connector
from datetime import datetime, timedelta
import random

class CorrectedTicketsInserter:
    def __init__(self, db_connection):
        self.db = db_connection
        self.inserted_count = 0
        
        # Tickets non utilisés, respectant la répartition demandée
        self.tickets_data = [
            # Français pur (12 tickets)
            {"title": "Problème imprimante bureau", "content": "Bonjour, l'imprimante du service RH ne fonctionne plus depuis ce matin. Quand j'essaie d'imprimer, elle fait du bruit mais rien ne sort. Pouvez-vous venir voir s'il vous plaît ? C'est urgent car j'ai des contrats à imprimer pour demain. Merci !", "category": "french_pure"},
            {"title": "URGENT - Ecran noir", "content": "écran noir depuis 10min!!!! help!!!", "category": "french_pure"},
            {"title": "Demande d'installation logiciel", "content": "Bonjour Monsieur, j'aurais besoin que vous installiez le logiciel de comptabilité sur mon ordinateur. Ma collègue m'a dit qu'il fallait faire une demande ici. Je ne suis pas très douée avec l'informatique, donc si vous pouviez passer quand vous avez un moment, ce serait parfait. Bonne journée.", "category": "french_pure"},
            {"title": "pb wifi", "content": "salut, le wifi marche pas sur mon portable, ça dit \"connecté mais pas d'internet\" c'est chiant... tu peux check stp ?", "category": "french_pure"},
            {"title": "Accès dossiers patients bloqué", "content": "Bonjour, je ne parviens plus à accéder aux dossiers patients depuis hier soir. Le système me demande constamment mon mot de passe mais refuse de me connecter. C'est très problématique car j'ai des consultations ce matin. Pourriez-vous résoudre cela rapidement ? Cordialement.", "category": "french_pure"},
            {"title": "Problème sauvegarde présentation", "content": "Hello ! Petit souci... ma présentation PowerPoint ne se sauvegarde plus, ça me dit \"erreur d'écriture\" à chaque fois :( J'ai peur de perdre tout mon travail ! Au secours !", "category": "french_pure"},
            {"title": "Serveur mail en panne", "content": "Mesdames, Messieurs, le serveur de messagerie semble être défaillant. Aucun de mes collaborateurs ne reçoit ses emails depuis 2 heures. Cela impacte notre activité commerciale. Merci de traiter cette demande en priorité absolue.", "category": "french_pure"},
            {"title": "Ordinateur très lent", "content": "Bonjour, mon PC rame énormément depuis la semaine dernière. Il met 5 minutes juste pour ouvrir Excel... c'est pas normal non ? Est-ce que vous pourriez l'optimiser ? Merci d'avance", "category": "french_pure"},
            {"title": "Clavier qui déconne", "content": "yo, mon clavier fait n'importe quoi... il écrit des lettres bizarres quand j'appuie sur certaines touches. genre quand je tape \"a\" ça fait \"à\" et des trucs comme ça... c'est relou", "category": "french_pure"},
            {"title": "Formation logiciel demandée", "content": "Bonjour, suite à notre conversation téléphonique, je confirme ma demande de formation sur le nouveau logiciel de gestion. Pourriez-vous organiser une session pour mon équipe de 5 personnes la semaine prochaine ? Nous sommes disponibles mardi et jeudi après-midi. Très cordialement.", "category": "french_pure"},
            {"title": "Imprimante clignote rouge", "content": "Bonjour, J’ai un souci avec mon imprimante. Elle clignote rouge et je n’arrive plus à imprimer depuis hier matin. Merci de vérifier.", "category": "french_pure"},
            {"title": "PC lent après mise à jour", "content": "Salut le support, Depuis la dernière mise à jour, mon PC est super lent. Il freeze même sur Word. C’est pas normal.", "category": "french_pure"},
            
            # Anglais pur (12 tickets)
            {"title": "Laptop won't start", "content": "Hi team, my laptop doesn't boot anymore. When I press the power button, I just get a black screen with a blinking cursor. I have an important client meeting at 2 PM and really need my files. Can someone help ASAP? Thanks!", "category": "english_pure"},
            {"title": "password reset plz", "content": "hey... forgot my password again 😅 can u reset it? thx!", "category": "english_pure"},
            {"title": "Email synchronization issue", "content": "Good morning, I'm experiencing synchronization problems with my Outlook. Emails from yesterday evening are not showing up, and I can't send new messages. This is affecting my customer communications. Could you please investigate? Best regards.", "category": "english_pure"},
            {"title": "Printer paper jam HELP!", "content": "OMG the printer is completely jammed!!! I tried everything but the paper is stuck really bad. I have 50 flyers to print for the meeting in 1 hour!!! EMERGENCY!!!", "category": "english_pure"},
            {"title": "Security concerns about data access", "content": "I've noticed unusual activity in our system logs. Multiple failed login attempts on my account from unknown IP addresses. Please review our security protocols and ensure our data is protected. This requires immediate attention from your senior technician.", "category": "english_pure"},
            {"title": "Software installation request", "content": "Hi there! Could you please install Adobe Creative Suite on my workstation? I need it for creating training materials. Also, do I need any special permissions? Let me know when would be a good time for you to come by. Thanks a bunch! 😊", "category": "english_pure"},
            {"title": "Spreadsheet crashes constantly", "content": "Every time I open our main budget file, Excel crashes after 2-3 minutes. It's a large file with lots of formulas... maybe that's the issue? I'm losing productivity here. Can you take a look?", "category": "english_pure"},
            {"title": "phone system not working", "content": "the phones r down!!! customers calling but we cant answer... this is really bad 4 business... fix plzzzz", "category": "english_pure"},
            {"title": "Projector connectivity issues", "content": "Dear IT Support, I am unable to connect my laptop to the projector in Conference Room B. I have tried multiple cables and settings without success. I have a presentation scheduled for tomorrow morning. Your prompt assistance would be greatly appreciated. Sincerely, Prof. Williams.", "category": "english_pure"},
            {"title": "Website upload problems", "content": "Hey guys, I can't upload images to our website. It keeps saying \"file too large\" even for small JPEGs. Is there a size limit I don't know about? Need to update the homepage today!", "category": "english_pure"},
            {"title": "SharePoint access issue", "content": "Hi, I'm not able to access the SharePoint drive. It says \"Permission Denied\". Please check my user rights.", "category": "english_pure"},
            {"title": "Keyboard stopped working", "content": "Hello IT, My keyboard stopped working randomly. Tried different USB ports already.", "category": "english_pure"},
            
            # Arabe tunisien pur (12 tickets)
            {"title": "مشكلة في الطابعة", "content": "أهلا، الطابعة ما تخدمش من الصباح. كل مرة نحاول نطبع، تعمل صوت برك وما يخرجش حتى ورقة. نحتاج نطبع فواتير اليوم. ممكن تجو تشوفو؟ مشكورين.", "category": "arabic_pure"},
            {"title": "نسيت كلمة المرور", "content": "السلام عليكم، نسيت كلمة المرور متاعي وما نجمش ندخل للنظام. شنوا نعمل؟ عندي شغل مهم لازم نكملو اليوم. بارك الله فيكم.", "category": "arabic_pure"},
            {"title": "الشبكة بطيئة برشا", "content": "مرحبا، الإنترنت بطيء برشا اليوم. ما نجمش نحمل الملفات الكبار. هل في مشكلة في الخادم؟ نستنى ردكم.", "category": "arabic_pure"},
            {"title": "طلب تثبيت برنامج جديد", "content": "أهلا وسهلا، نحب نثبت برنامج إدارة المشاريع الجديد على جهازي. قالولي لازم نعمل طلب هنا. متى تنجمو تجو؟ شكرا جزيلا.", "category": "arabic_pure"},
            {"title": "الكمبيوتر يطفي وحدو", "content": "كيفكم؟ جهاز الكمبيوتر متاعي يطفي وحدو بلا سبب. صار هكا ثلاث مرات اليوم. شنوا المشكلة في رايكم؟", "category": "arabic_pure"},
            {"title": "ماعادش يخدملي الورد", "content": "سلام، ماعادش يخدملي الورد على البيسي. كل مرة نحاول نحلّه يخرجلي خطأ.", "category": "arabic_pure"},
            {"title": "البريد الالكتروني ما توصلنيش", "content": "المشكل في البريد الالكتروني، الميساجات ما توصلنيش، وجربت نبدل البراوزر نفس المشكل.", "category": "arabic_pure"},
            {"title": "النمبر تاعي مسكر", "content": "سلااام، النمبر تاعي مسكر، كي يكليني حد يقوله \"le numéro n'est pas attribué\".", "category": "arabic_pure"},
            {"title": "الويندوز يطلب activation", "content": "برجاء التدخّل، الويندوز يطلب activation، وكي نعمل activate ما ينجّمش يتصل بالسرفور.", "category": "arabic_pure"},
            {"title": "اللوجيسيال متاع المحاسبة يوقف", "content": "هاو المشكل، اللوجيسيال متاع المحاسبة يوقف فجأة، ديما في نفس البلاصة.", "category": "arabic_pure"},
            {"title": "مشكل الويفي", "content": "سلام، الويفي عندي ما يخدمش كيف كيف، يقطع كل شوية. شنوة الحل؟", "category": "arabic_pure"},
            {"title": "التليفون الداخلي ما يرنّش", "content": "يا جماعة، التليفون الداخلي ما يرنّش، لازم نصلحو بسرعة.", "category": "arabic_pure"},
            
            # Arabe tunisien en lettres latines (7 tickets)
            {"title": "mochkla fel imprimante", "content": "ahla, l'imprimante ma t5ademch mel sb7... kol marra n7awel netba3 taamel sout w ma y5rojch 7atta warqa. n7taj netba3 des documents importants lyoum. momken tjou tchoufou? merci bcp!", "category": "tunisian_latin"},
            {"title": "internet bati2", "content": "salem, l'internet bati2 bch la yemchi... ma nejemch na3mel download w7atta... fel facebook yemchi ama fel email ma yemchich... chneya l mochkla?", "category": "tunisian_latin"},
            {"title": "password forgot", "content": "salut! nesit mot de passe mtee w ma nejemch ned5el lel système... 3andi travail important lezem n5alaso lyoum... aidouni barcha allah y5alik!", "category": "tunisian_latin"},
            {"title": "ordi tres lent", "content": "kifek? l'ordinateur bech yemchi b bt2... y5od 10 minutes juste bech ya7el Excel... heka mech normal... momken t3amelou maintenance?", "category": "tunisian_latin"},
            {"title": "email ma yetb3atch", "content": "bonsoir, l'email ma yetb3atch... kol marra nekteb message w neclicki \"envoyer\" ya3tini erreur... urgent car 3andi rdv demain w lezem neb3ath documents!", "category": "tunisian_latin"},
            {"title": "y'a un bruit bizarre dans le PC", "content": "salam, 3andi laptop jdid w fama bruit ghal3ed s3ir mel we7ed yetla3 mel PC, ye5i yji menou? c'est un Dell Inspiron. merciii", "category": "tunisian_latin"},
            {"title": "3andek chwaya temps?", "content": "la souris wireless se déconnecte toute seule toutes les 5 minutes, faut que je retire la pile et remettre. chépa pk. c'est une Logitech M185. merci pour l'aide.", "category": "tunisian_latin"},
            
            # Français avec codes techniques (6 tickets)
            {"title": "Erreur SQL Server 2019", "content": "Bonjour, je rencontre l'erreur E401 sur SQL Server 2019 depuis la mise à jour vers la version 15.0.4298. Le service s'arrête de manière aléatoire. Logs disponibles sur \\server\\logs\\sql_errors_20241215.txt. Besoin d'assistance technique urgente.", "category": "french_tech"},
            {"title": "IIS 10.0 ne démarre pas", "content": "Salut l'équipe ! Problème avec IIS 10.0 sur Windows Server 2022. Code d'erreur W3SVC_FAILED_TO_START après installation du patch KB5022842. J'ai essayé le restart du service mais rien n'y fait. Des idées ?", "category": "french_tech"},
            {"title": "BSOD avec erreur 0x0000007B", "content": "hello, BSOD récurrent avec code erreur 0x0000007B sur les postes Dell OptiPlex 7090. Ça started après le déploiement du driver v12.3.45 pour les cartes graphiques Intel UHD 630. Rollback nécessaire ?", "category": "french_tech"},
            {"title": "Exchange 2016 CU23 - problème calendrier", "content": "Bonjour, après migration vers Exchange 2016 CU23, les utilisateurs rapportent des dysfonctionnements du calendrier. Event ID 9646 dans les logs. Impact sur 250 utilisateurs. Priorité haute SVP.", "category": "french_tech"},
            {"title": "VLAN 192 inaccessible", "content": "Team, le VLAN 192 (10.1.192.0/24) n'est plus accessible depuis le switch Cisco C9300-48T firmware 16.12.05. Ping timeout sur la gateway 10.1.192.1. Config backup disponible si besoin de rollback.", "category": "french_tech"},
            {"title": "Excel Crash fichier spécifique", "content": "Bonjour, Excel 365 plante systématiquement à l'ouverture du fichier Rapport_Financier_Q4.xlsx. Le fichier fait 120 Mo. Message d'erreur : Excel a rencontré un problème et doit fermer. Avez-vous une solution ?", "category": "french_tech"},
            
            # Anglais avec codes techniques (3 tickets)
            {"title": "NullReferenceException in C# app", "content": "Hi, I’m getting NullReferenceException in the C# app. Seems like a missing dependency.", "category": "english_tech"},
            {"title": "Docker container unreachable", "content": "Hello IT, I deployed a container with Docker, but the service is unreachable on port 8080.", "category": "english_tech"},
            {"title": "Auth service logs issue", "content": "Hi support, Can you check the logs for auth.service on srv-prod03? Users can't authenticate.", "category": "english_tech"},
            
            # Arabe tunisien avec codes techniques (2 tickets)
            {"title": "لازم نبدّل الDNS", "content": "سلام، لازم نبدّل الDNS في الrouteur، خاطر الinternet توحل.", "category": "arabic_tech"},
            {"title": "البورت 443 مسكّر", "content": "يا IT, البورت 443 مسكّر في الـ firewall، نحب نعمل remote desktop.", "category": "arabic_tech"},
            
            # Arabe en lettres latines avec codes techniques (2 tickets)
            {"title": "probleme de login intranet", "content": "salam, kan 7attit login/mot de passe mte3i f l intranet w ki nej3ed nokhrej erreur \"authentification failed\" alors que c'est correct. ken fama problème cote serveur? merci.", "category": "tunisian_latin_tech"},
            {"title": "backup failure Veeam", "content": "slt, backup automatique ma ykounch active, erreur: Failed to preprocess target VM. check please le job \"Nightly-Backup\".", "category": "tunisian_latin_tech"},
            
            # Mixte (4 tickets)
            {"title": "VPN TLS handshake failed", "content": "Hello, j’ai un souci avec le VPN, ça connecte puis ça coupe. Le log dit : TLS handshake failed. Plz help!", "category": "mixed"},
            {"title": "Excel crash urgent", "content": "Salem, i can't open Excel, ça crash direct ! Maybe it's related to last update? chnoa solution?", "category": "mixed"},
            {"title": "Outlook IMAP config", "content": "Hi, besh nestaamel Outlook fi tel tounsi, ma na3refch chnowa les paramètres IMAP exacts.", "category": "mixed"},
            {"title": "SAP crash erreur 500", "content": "Bonjour IT, el système de paie crash mta3 SAP ne répond pas. Error: 500 Internal Server Error.", "category": "mixed"}
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