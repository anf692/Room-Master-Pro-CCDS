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
                        nom = input("Nom complet : ").strip()
                        email = input("Email : ").strip()
                        mdp = input("Mot de passe : ").strip()
                        role = input("Role (ADMIN/GESTIONNAIRE/VISITEUR) : ").strip().upper()
                        self.auth.inscription(nom, email, mdp, role)
                    
                    case "2":
                        email = input("Email : ").strip()
                        mdp = input("Mot de passe : ").strip()
                        self.auth.login(email, mdp)
                    
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
                            date = input("Date (jj/mm/aaaa) : ").strip()
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
                            if role in ["ADMIN", "GESTIONNAIRE"]:
                                id_creneau = int(input("ID Créneau : ").strip())
                                id_groupe = int(input("ID Groupe : ").strip())
                                date = input("Date (jj/mm/aaaa) : ").strip()

                                self.planning.reserver_creneau(
                                    user, id_creneau, id_groupe, date
                                )
                            else:
                                self.auth.logout()
                                print("Déconnecté.")

                        case "3":
                            if role in ["ADMIN", "GESTIONNAIRE"]:
                                nom = input("Nom du groupe : ").strip()
                                responsable = input("Responsable : ").strip()
                                type_evenement = input("Type d'événement : ").strip()

                                self.planning.ajouter_groupe(
                                    user,
                                    nom,
                                    responsable,
                                    type_evenement
                                )
                            else:
                                print("Choix invalide.")

                        case "4":
                            if role in ["ADMIN", "GESTIONNAIRE"]:
                                date = input("Date (jj/mm/aaaa) : ").strip()
                                self.export.export_planning(date)
                            else:
                                print("Choix invalide.")

                        case "5":
                            if role in ["ADMIN", "GESTIONNAIRE"]:
                                self.auth.logout()
                                print("Déconnecté.")
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