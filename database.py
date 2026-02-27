import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import Error


load_dotenv()

class BaseDeDonnees:
    def __init__(self):

        try:
            self._connexion = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            self._curseur = self._connexion.cursor(dictionary=True)

        except Error as e:
            print("Erreur de connexion à la base :", e)
            self._connexion = None
            self._curseur = None


    @property
    def connexion(self):
        return self._connexion

    @property
    def curseur(self):
        return self._curseur

    def commit(self):
        if self._connexion:
            self._connexion.commit()

    def fermer(self):
        if self._connexion:
            self._curseur.close()
            self._connexion.close()
    
