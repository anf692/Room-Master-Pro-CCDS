# services/auth_service.py
import bcrypt
from models.utilisateur import Utilisateur
from database import BaseDeDonnees

class AuthService:
    def __init__(self, db: BaseDeDonnees):
        self._db = db
        self._session_utilisateur = None

    @property
    def session_utilisateur(self):
        return self._session_utilisateur

    def inscription(self, nom_complet, email, mot_de_passe, role):
        hash_pwd = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
        try:
            self._db.curseur.execute(
                "INSERT INTO utilisateurs (nom_complet, email, mot_de_passe, role) VALUES (%s,%s,%s,%s)",
                (nom_complet, email, hash_pwd.decode('utf-8'), role)
            )
            self._db.commit()
            print("Inscription réussie !")

        except Exception as e:
            print("Erreur inscription :", e)

    def login(self, email, mot_de_passe):
        self._db.curseur.execute(
            "SELECT * FROM utilisateurs WHERE email=%s",
            (email,)
        )

        result = self._db.curseur.fetchone()

        if result and bcrypt.checkpw(mot_de_passe.encode('utf-8'), result['mot_de_passe'].encode('utf-8')):
            self._session_utilisateur = Utilisateur(
                result['id_user'],
                result['nom_complet'],
                result['email'],
                result['mot_de_passe'],
                result['role']
            )
            print(f"Connecté en tant que {self._session_utilisateur.nom_complet} ({self._session_utilisateur.role})")
            return True
        
        print("Email ou mot de passe incorrect.")
        return False

    def logout(self):
        self._session_utilisateur = None
        print("Déconnecté.")
        