class Reservation:
    def __init__(self, id_reservation, date_reservation, creneau, groupe):
        self._id_reservation = id_reservation
        self._date_reservation = date_reservation
        self._creneau = creneau 
        self._groupe = groupe  

    @property
    def id_reservation(self):
        return self._id_reservation

    @property
    def date_reservation(self):
        return self._date_reservation

    @property
    def creneau(self):
        return self._creneau

    @property
    def groupe(self):
        return self._groupe
    
    