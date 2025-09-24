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
            {"title": "PC hang problem", "content": "chwaya chwaya el pc yhang, ma3andich 3lach. aide moi stp.", "category": "tunisian_latin"},

            # Anglais avec Codes Techniques Avancés (5 tickets)
            {"title": "Docker container keeps crashing", "content": "Hey team, our main app container (nginx:1.21.6-alpine) keeps crashing with exit code 137. Memory limit set to 2GB but it's hitting OOM killer. Logs show memory spike around 18:30 UTC. Need urgent fix before tomorrow's deployment!", "category": "english_tech"},
            {"title": "MySQL 8.0.32 replication lag", "content": "Good morning, experiencing significant replication lag on MySQL 8.0.32 slave server. Current lag: 47 seconds. Master shows high IO_THREAD utilization. Binary log size: 2.3GB. Performance degrading since yesterday. Please investigate.", "category": "english_tech"},
            {"title": "Firewall rule blocking port 8443", "content": "pfSense 2.6.0 is blocking HTTPS traffic on port 8443 despite rule allowing it. Source: 192.168.1.0/24, Destination: any. Rule works for port 443 but not 8443. Checked logs - packets getting dropped. Need urgent resolution.", "category": "english_tech"},
            {"title": "BGP session down with AS65001", "content": "BGP peering session with AS65001 (10.0.0.1) went down at 14:32 EST. Last known state: Established. Current state: Active. No recent config changes. ISP reports no issues on their end. Route table shows 0 prefixes received. Help needed!", "category": "english_tech"},
            {"title": "VMware vSphere 7.0 U3 host disconnected", "content": "VMware host esxi-prod-01 (192.168.10.15) showing as disconnected in vCenter 7.0 U3. VMs still running but can't manage them. SSL certificate renewed last week. Tried reconnect - fails with error \"Host certificate verification failed\". Please check.", "category": "english_tech"},

            # Arabe Tunisien avec Codes Techniques (5 tickets)
            {"title": "خطأ في Apache 2.4.54", "content": "أهلا، عندي مشكلة في Apache 2.4.54 على Ubuntu 22.04. الخطأ \"SSL_ERROR_RX_RECORD_TOO_LONG\" يظهر كل مرة. حاولت أغير الإعدادات في ssl.conf بس ما نجحتش. محتاج مساعدة عاجلة.", "category": "arabic_tech"},
            {"title": "بطء في PostgreSQL 14.7", "content": "السلام عليكم، قاعدة البيانات PostgreSQL 14.7 بطيئة جداً. الاستعلامات تاخد أكثر من 30 ثانية. حجم الجدول الرئيسي 2.5 مليون سجل. هل محتاجة تحسين؟ شكراً.", "category": "arabic_tech"},
            {"title": "مشكلة في Router Mikrotik RB4011", "content": "مرحبا، الراوتر Mikrotik RB4011 فيه مشكلة. Port 5 ما يشتغلش، LED ما يضويش. حاولت reset بس نفس المشكلة. هل هي مشكلة Hardware؟", "category": "arabic_tech"},
            {"title": "خطأ في Windows Server 2022", "content": "أهلا وسهلا، Windows Server 2022 يعطي Event ID 4625 كثير في Security Log. محاولات دخول فاشلة من IP 203.45.67.89. هل هذا هجوم؟ محتاجة نحجب هذا IP.", "category": "arabic_tech"},
            {"title": "مشكلة في Backup Veeam B&R 12", "content": "كيف الحال؟ نظام النسخ الاحتياطي Veeam Backup & Replication 12 يعطي خطأ \"Snapshot creation failed\" للآلة الافتراضية SQL-PROD-01. حجم البيانات 850 جيجا. محتاج حل سريع.", "category": "arabic_tech"},

            # Arabe Style Facebook avec Codes Techniques (5 tickets)
            {"title": "mochkla fel Office 365 E3", "content": "kifkm l team! 3andi problème fel Office 365 E3 license... kol marra n7awel na7el Outlook y3tini error code 0x80040116... 7awlt restart w update ama nefs l7ala... aidouni plz!", "category": "tunisian_latin_tech"},
            {"title": "Node.js v18.14 ma yemchich", "content": "salem! Node.js version 18.14.0 ma yemchi 3al Ubuntu 20.04... y3tini \"EACCES permission denied\" meta n7awel n3amel npm install... 7awlt sudo ama ma n7ebch na3melha heka... des idées?", "category": "tunisian_latin_tech"},
            {"title": "Switch HP ProCurve 2530 problem", "content": "ahla, switch HP ProCurve 2530-24G ports 15 w 16 ma ye5dmuch... LED orange dayma... 7awelt reboot ama ma n9arech... est-ce que hardware failure? need help urgent!", "category": "tunisian_latin_tech"},
            {"title": "MySQL 8.0 slow queries", "content": "bonsoir team! MySQL 8.0.28 3ammel slow queries barch... kol query t5od more than 15 seconds... database size 4.2 GB... lezem optimization walla server upgrade? urgent plz!", "category": "tunisian_latin_tech"},
            {"title": "pfSense 2.7 firewall logs error", "content": "salam! pfSense 2.7.0 3am yekteb errors fel logs barch... \"kernel: pid 1234: blocked by rule 999\"... heka normal walla fi hacking attempt? chneya n3amel? 7atta f documentation ma l9itch 7aja w7da...", "category": "tunisian_latin_tech"},

            # Tickets Mixtes Complexes (2-4 langues + codes) (10 tickets)
            {"title": "URGENT: Exchange 2019 + Outlook مشكلة كبيرة!", "content": "Hello team!! J'ai un problème énorme... Exchange 2019 CU12 refuse les connexions من الصباح and my entire équipe can't access emails! Error code 0x80040115 يظهر constantly. C'est très urgent car we have meeting with clients at 3 PM و محتاجين الإيميلات! Please fix ASAP!! Merci bcp", "category": "mixed"},
            {"title": "Docker + Kubernetes cluster down - عاجل جداً!!", "content": "team urgent!!! notre cluster Kubernetes v1.26.3 est complètement down! Les pods في حالة CrashLoopBackOff و ما نجمناش نعملهم restart... Docker Engine v23.0.1 shows errors في اللوجات: \"failed to start container runtime\"... Business impact critique!! Need senior engineer NOW!", "category": "mixed"},
            {"title": "Adobe CC 2023 مع مشاكل الطابعة Canon", "content": "salut les gars... Adobe Creative Cloud 2023 يعطيني خطأ غريب when I try to print من Photoshop vers Canon imageRUNNER C3226i... ça dit \"PostScript error\" و الطابعة تطبع صفحات فاضية!! J'ai deadline demain for client presentation... help needed!! Also, InDesign crashes avec error E404 randomly", "category": "mixed"},
            {"title": "SQL Server 2022 replication فشل + backup issues", "content": "Dear IT support, notre SQL Server 2022 replication vers DR site completely failed last night. Error log shows: \"The process could not connect to Subscriber\"... واضح إنو في مشكلة network ama ping يشتغل normal! Also backup job failed with error code B304... هذا يعني إنو ما عندناش backup منذ 48 hours!! This is critical risk للشركة.", "category": "mixed"},
            {"title": "React 18.2 + Node.js deployment مشكلة", "content": "hey everyone! deploying React 18.2.0 application على Node.js v19.8.1 server بس في خطأ strange... كل marra build ينتهي successfully ama when users access site shows \"Cannot GET /\" error... nginx logs تقول 502 Bad Gateway w backend service runs على port 3000... tried pm2 restart ama nefs l mochkla!", "category": "mixed"},
            {"title": "Multi-site VPN failure - Cisco ASA + pfSense", "content": "Urgent situation!! Our main VPN tunnel between headquarters (Cisco ASA 5516-X firmware 9.16.4) and branch office (pfSense 2.6.0) est complètement down depuis ce matin! Site-to-site traffic blocked و الموظفين can't access shared resources... IPSec Phase 1 successful but Phase 2 fails with error \"No proposal chosen\"... tried rebooting both firewalls بس المشكلة باقية...", "category": "mixed"},
            {"title": "VMware vSphere 8.0 + Windows Server 2022 بلوة كبيرة", "content": "salam team... عندي disaster scenario! VMware vSphere 8.0 host crashed w restart loop... Windows Server 2022 domain controller VM won't boot يعطي \"CRITICAL_PROCESS_DIED\" BSOD! Users can't login للشبكة w Exchange services down... tried booting من snapshot ama corrupted!! قاعدة البيانات also affected... This affects 200+ users!!", "category": "mixed"},
            {"title": "Fortinet FortiGate + مشاكل bandwidth + WiFi issues", "content": "kifkom team? Multiple issues today!! Fortinet FortiGate 200E firmware 7.2.3 shows bandwidth utilization 95% constantly but actual traffic monitoring tools show only 30%... suspicious!! Also WiFi infrastructure (Ubiquiti UniFi 6 Enterprise) dropping connections randomly... users complain \"internet bati2 kol dqiqa\"... tried channel optimization ama المشكلة persist!", "category": "mixed"},
            {"title": "Critical: Microsoft 365 + on-premises integration failure", "content": "Dear IT Support Team, We are experiencing a critical system failure affecting our hybrid Microsoft 365 environment. Azure AD Connect v2.0.88.0 synchronization has stopped working, resulting في عدم تحديث user accounts للسحابة. On-premises Active Directory (Windows Server 2022) functions normally, but cloud services show authentication errors.", "category": "mixed"},
            {"title": "DISASTER: Oracle DB 19c + backup corruption + network chaos!!", "content": "MAYDAY MAYDAY!! Complete system meltdown! Oracle Database 19c crashed with ORA-00600 error و automatic recovery failed! Backup validation shows corruption في الـ RMAN files... وهذا means ما عندناش clean backup منذ last week!! Also network infrastructure going crazy - switches (Cisco C9300 series) randomly rebooting, fiber connections unstable!!", "category": "mixed"}
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