class Groupe:
    def __init__(self, id_groupe, nom_groupe, responsable, type_evenement):
        self._id_groupe = id_groupe
        self._nom_groupe = nom_groupe
        self._responsable = responsable
        self._type_evenement = type_evenement

    @property
    def id_groupe(self):
        return self._id_groupe

    @property
    def nom_groupe(self):
        return self._nom_groupe

    @property
    def responsable(self):
        return self._responsable

    @property
    def type_evenement(self):
        return self._type_evenement
    
    