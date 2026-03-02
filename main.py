from database import BaseDeDonnees
from services.auth_service import AuthService
from services.planning_service import PlanningService
from services.export_service import ExportService

class Application:
    """Classe principale de l'application de gestion de la salle polyvalente."""

    def __init__(self):
        self.db = BaseDeDonnees()
        self.auth = AuthService(self.db)
        self.planning = PlanningService(self.db)
        self.export = ExportService(self.db)

    def lancer(self):
        """Lance l'application et affiche le menu principal."""
        while True:
            print("\n===== MENU =====")
            
            # Vérifier si un utilisateur est connecté
            if not self.auth.session_utilisateur:
                print("1. S'Inscrire")
                print("2. Se connecter")
                print("0. Quitter")
                
                choix = input("Votre choix : ").strip()
                match choix:
                    case "1":
                        try:
                            while True:
                                nom = input("Nom complet : ").strip()
                                if not nom.isalpha():
                                    print("Le nom doit être composé uniquement de lettres. Veuillez réessayer.")
                                else:
                                    break
                            
                            while True:
                                email = input("Email : ").strip().replace(" ", "")
                                if "@" not in email:
                                    print("email invalide")
                                else:
                                    break

                            while True:
                                mdp = input("Mot de passe : ").strip()
                                if not mdp:
                                    print("Mot de passe invalide")
                                else:
                                    break

                            while True:
                                role = input("Role (ADMIN/GESTIONNAIRE/VISITEUR) : ").strip().upper().replace(" ", "")
                                if not role and role not in ["ADMIN", "GESTIONNAIRE", "VISITEUR"]:
                                    print("role invalide")
                                else:
                                    break

                            self.auth.inscription(nom, email, mdp, role)

                        except Exception as e:
                            print("Erreur lors de l'inscription",e)
                    
                    case "2":
                        try:
                            while True:
                                email = input("Email : ").strip().replace(" ", "")
                                if "@" not in email:
                                    print("email invalide")
                                else:
                                    break
                            while True:
                                mdp = input("Mot de passe : ").strip()
                                if not mdp:
                                    print("Mot de passe invalide")
                                else:
                                    break
                            self.auth.login(email, mdp)
                        except Exception as e:
                            print("Erreur lors de la connexion", e)
                    
                    case "0":
                        print("Au revoir !")
                        self.db.fermer()
                        break
                    
                    case _:
                        print("Choix invalide.")

            else:
                user = self.auth.session_utilisateur
                role = user.role

                print(f"\nConnecté en tant que : {user.nom_complet} ({role})")

                print("1. Voir planning journalier")

                if role in ["ADMIN", "GESTIONNAIRE"]:
                    print("2. Réserver un créneau")
                    print("3. Ajouter un groupe")
                    print("4. Export CSV du planning")
                    print("5. Logout")
                    print("0. Quitter")
                else:  # VISITEUR
                    print("2. Logout")
                    print("0. Quitter")

                choix = input("Votre choix : ").strip()

                try:
                    match choix:

                        case "1":
                            date = input("Date (jj/mm/aaaa) : ").strip().replace(" ", "")
                            planning_jour = self.planning.afficher_planning_journalier(date)

                            if not planning_jour:
                                print("Aucune réservation pour cette date.")
                            else:
                                print("\n===== PLANNING JOURNALIER =====")
                                print(f"{'ID':<4} {'Début':<6} {'Fin':<6} {'Groupe':<20} {'Responsable':<15} {'Type':<12}")
                                print("-" * 75)

                                for ligne in planning_jour:
                                    print(f"{ligne['id_creneau']:<4} "
                                        f"{ligne['heure_debut']:<6} "
                                        f"{ligne['heure_fin']:<6} "
                                        f"{ligne['nom_groupe']:<20} "
                                        f"{ligne['responsable']:<15} "
                                        f"{ligne['type_evenement']:<12}")

                        case "2":
                            self.planning.affichage_creneau()
                            self.planning.affichage_groupe()
                            if role in ["ADMIN", "GESTIONNAIRE"]:
                                try:
                                    while True:
                                        id_creneau = int(input("ID Créneau : ").strip().replace(" ", ""))
                                        if not  id_creneau:
                                            print("ID doit etre un nombre")
                                        else:
                                            break
                                    
                                    while True:
                                        id_groupe = int(input("ID Groupe : ").strip().replace(" ", ""))
                                        if not  id_creneau:
                                            print("ID doit etre un nombre")
                                        else:
                                            break

                                    date = input("Date (jj/mm/aaaa) : ").strip().replace(" ", "")

                                    self.planning.reserver_creneau(
                                        user, id_creneau, id_groupe, date
                                    )
                                except Exception as e:
                                    print("Erreur lors de la reservation", e)

                            else:
                                self.auth.logout()
                                print("Déconnecté.")

                        case "3":
                            if role in ["ADMIN", "GESTIONNAIRE"]:
                                try:
                                    while True:
                                        nom = input("Nom du groupe : ").strip()
                                        if not nom.isalpha():
                                            print("Nom invalide")
                                        else:
                                            break

                                    while True:
                                        responsable = input("Responsable : ").strip()
                                        if not responsable.isalpha():
                                            print("Responsable invalide")
                                        else:
                                            break

                                    while True:
                                        type_evenement = input("Type d'événement (Atelier, Réunion, Conférence, Cours): ").strip().capitalize().replace(" ", "")
                                        if type_evenement not in ["Atelier","Réunion", "Conférence","Cours"]:
                                            print("Type d'evenement invalide")
                                        else:
                                            break

                                    self.planning.ajouter_groupe(
                                        user,
                                        nom,
                                        responsable,
                                        type_evenement
                                    )
                                except Exception as e:
                                    print ("Erreur lors de l'ajout du groupe")
                            else:
                                print("Choix invalide.")

                        case "4":
                            if role in ["ADMIN", "GESTIONNAIRE"]:
                                date = input("Date (jj/mm/aaaa) : ").strip().replace(" ","")
                                self.export.export_planning(date)
                            else:
                                print("Choix invalide.")

                        case "5":
                            if role in ["ADMIN", "GESTIONNAIRE"]:
                                self.auth.logout()
                            else:
                                print("Choix invalide.")

                        case "0":
                            print("Au revoir !")
                            self.db.fermer()
                            break

                        case _:
                            print("Choix invalide.")

                except Exception as e:
                    print("Erreur :", e)


app = Application()
app.lancer()