class Creneau:
    def __init__(self, id_creneau, heure_debut, heure_fin):
        self._id_creneau = id_creneau
        self._heure_debut = heure_debut
        self._heure_fin = heure_fin

    @property
    def id_creneau(self):
        return self._id_creneau

    @property
    def heure_debut(self):
        return self._heure_debut

    @property
    def heure_fin(self):
        return self._heure_fin