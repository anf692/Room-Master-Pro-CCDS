class Utilisateur:
    def __init__(self, id_user, nom_complet, email, mot_de_passe, role):
        self._id_user = id_user
        self._nom_complet = nom_complet
        self._email = email
        self._mot_de_passe = mot_de_passe
        self._role = role

    
    @property
    def id_user(self):
        return self._id_user

    @property
    def nom_complet(self):
        return self._nom_complet

    @property
    def email(self):
        return self._email

    @property
    def role(self):
        return self._role