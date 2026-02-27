from models.reservation import Reservation
from models.creneau import Creneau
from models.groupe import Groupe
from database import BaseDeDonnees

class PlanningService:
    def __init__(self, db: BaseDeDonnees):
        self._db = db

    def afficher_planning_journalier(self, date):

        sql = """
        SELECT c.id_creneau, c.heure_debut, c.heure_fin, g.nom_groupe, g.responsable, g.type_evenement
        FROM creneaux c
        LEFT JOIN reservations r ON c.id_creneau = r.id_creneau AND r.date_reservation=%s
        LEFT JOIN groupes g ON r.id_groupe = g.id_groupe
        """

        self._db.curseur.execute(sql, (date,))
        return self._db.curseur.fetchall()

    def reserver_creneau(self, session_utilisateur, id_creneau, id_groupe, date_reservation):
        if session_utilisateur is None:
            print("Veuillez vous connecter.")
            return False
        
        if session_utilisateur.role not in ['ADMIN', 'GESTIONNAIRE']:
            print("Permission refusée.")
            return False
        
        try:
            # Vérifier si déjà réservé
            self._db.curseur.execute(
                "SELECT * FROM reservations WHERE date_reservation=%s AND id_creneau=%s",
                (date_reservation, id_creneau)
            )

            if self._db.curseur.fetchone():
                print("Ce créneau est déjà réservé !")
                return False
            
            # Insérer réservation
            self._db.curseur.execute(
                "INSERT INTO reservations (date_reservation, id_creneau, id_groupe) VALUES (%s,%s,%s)",
                (date_reservation, id_creneau, id_groupe)
            )

            self._db.commit()
            print("Réservation réussie !")
            return True
        
        except Exception as e:
            print("Erreur lors de la réservation :", e)
            return False
        
