import csv
from datetime import datetime

class ExportService:
    def __init__(self, db):
        self._db = db

    def format_date_mysql(self, date_fr):
        try:
            return datetime.strptime(date_fr, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Format de date invalide ! Utilisez jj/mm/aaaa")


    def export_planning(self, date_fr, fichier="planning_journalier.csv"):
        # Conversion AVANT requête SQL
        
        date_mysql = self.format_date_mysql(date_fr)

        sql = """
        SELECT c.heure_debut, c.heure_fin, g.nom_groupe, g.type_evenement, g.responsable
        FROM creneaux c
        LEFT JOIN reservations r 
            ON c.id_creneau = r.id_creneau 
            AND r.date_reservation=%s
        LEFT JOIN groupes g 
            ON r.id_groupe = g.id_groupe
        ORDER BY c.id_creneau
        """

        self._db.curseur.execute(sql, (date_mysql,))
        resultats = self._db.curseur.fetchall()

        with open(fichier, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Heure Début','Heure Fin','Groupe','Type','Responsable'])

            for ligne in resultats:
                writer.writerow([
                    ligne['heure_debut'],
                    ligne['heure_fin'],
                    ligne['nom_groupe'] or '[LIBRE]',
                    ligne['type_evenement'] or '',
                    ligne['responsable'] or ''
                ])

        print(f"Planning exporté dans {fichier}")