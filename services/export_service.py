import csv

class ExportService:
    def __init__(self, db):
        self._db = db

    def export_planning(self, date, fichier="planning_journalier.csv"):

        sql = """
        SELECT c.heure_debut, c.heure_fin, g.nom_groupe, g.type_evenement, g.responsable
        FROM creneaux c
        LEFT JOIN reservations r ON c.id_creneau = r.id_creneau AND r.date_reservation=%s
        LEFT JOIN groupes g ON r.id_groupe = g.id_groupe
        """
        
        self._db.curseur.execute(sql, (date,))
        resultats = self._db.curseur.fetchall()

        with open(fichier, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Heure Début','Heure Fin','Groupe','Type','Responsable'])
            for ligne in resultats:
                writer.writerow([
                    ligne['heure_debut'],
                    ligne['heure_fin'],
                    ligne['nom_groupe'] if ligne['nom_groupe'] else '[LIBRE]',
                    ligne['type_evenement'] if ligne['type_evenement'] else '',
                    ligne['responsable'] if ligne['responsable'] else ''
                ])
        print(f"Planning exporté dans {fichier}")