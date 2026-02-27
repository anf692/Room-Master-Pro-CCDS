from models.reservation import Reservation
from models.creneau import Creneau
from models.groupe import Groupe
from database import BaseDeDonnees
from datetime import datetime

class PlanningService:
    def __init__(self, db: BaseDeDonnees):
        self._db = db

    # Conversion timedelta -> HH:MM
    def _format_heure(self, td):
        total_seconds = int(td.total_seconds())
        heures = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{heures:02d}:{minutes:02d}"

    # Convertit date française jj/mm/aaaa -> YYYY-MM-DD
    def _format_date_mysql(self, date_fr):
        try:
            date_obj = datetime.strptime(date_fr, "%d/%m/%Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Format de date invalide ! Utilisez jj/mm/aaaa")


    def afficher_planning_journalier(self, date_fr):
        date_mysql = self._format_date_mysql(date_fr)

        sql = """
        SELECT c.id_creneau, c.heure_debut, c.heure_fin, g.nom_groupe, g.responsable, g.type_evenement
        FROM creneaux c
        LEFT JOIN reservations r ON c.id_creneau = r.id_creneau AND r.date_reservation=%s
        LEFT JOIN groupes g ON r.id_groupe = g.id_groupe
        ORDER BY c.id_creneau
        """

        self._db.curseur.execute(sql, (date_mysql,))
        resultats = self._db.curseur.fetchall()

        # Format lisible
        planning = []
        for ligne in resultats:
            planning.append({
                "id_creneau": ligne['id_creneau'],
                "heure_debut": self._format_heure(ligne['heure_debut']),
                "heure_fin": self._format_heure(ligne['heure_fin']),
                "nom_groupe": ligne['nom_groupe'] or "[LIBRE]",
                "responsable": ligne['responsable'] or "-",
                "type_evenement": ligne['type_evenement'] or "-"
            })
        return planning


    def ajouter_groupe(self, session_utilisateur, nom_groupe, responsable, type_evenement):
        if session_utilisateur is None:
            print("Veuillez vous connecter.")
            return False

        if session_utilisateur.role not in ['ADMIN', 'GESTIONNAIRE']:
            print("Permission refusée.")
            return False

        try:
            # Vérifier si le groupe existe déjà
            self._db.curseur.execute(
                "SELECT * FROM groupes WHERE nom_groupe = %s",
                (nom_groupe,)
            )

            if self._db.curseur.fetchone():
                print("Ce groupe existe déjà.")
                return False

            # Insertion
            self._db.curseur.execute(
                "INSERT INTO groupes (nom_groupe, responsable, type_evenement) VALUES (%s, %s, %s)",
                (nom_groupe, responsable, type_evenement)
            )

            self._db.commit()
            print("Groupe ajouté avec succès !")
            return True

        except Exception as e:
            print("Erreur lors de l'ajout du groupe :", e)
            return False


    def reserver_creneau(self, session_utilisateur, id_creneau, id_groupe, date_fr):
        if session_utilisateur is None:
            print("Veuillez vous connecter.")
            return False
        
        if session_utilisateur.role not in ['ADMIN', 'GESTIONNAIRE']:
            print("Permission refusée.")
            return False

        try:
            date_mysql = self._format_date_mysql(date_fr)

            # Vérifier si déjà réservé
            self._db.curseur.execute(
                "SELECT * FROM reservations WHERE date_reservation=%s AND id_creneau=%s",
                (date_mysql, id_creneau)
            )

            if self._db.curseur.fetchone():
                print("Ce créneau est déjà réservé !")
                return False

            # Insérer réservation
            self._db.curseur.execute(
                "INSERT INTO reservations (date_reservation, id_creneau, id_groupe) VALUES (%s,%s,%s)",
                (date_mysql, id_creneau, id_groupe)
            )

            self._db.commit()
            print("Réservation réussie !")
            return True

        except Exception as e:
            print("Erreur lors de la réservation :", e)
            return False
        
