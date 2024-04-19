class Fornitore:

    def __init__(self):
        self.cittaSede = ""
        self.denominazione = ""
        self.indirizzoSede = ""
        self.partitaIva = ""
        self.tipoProfessione = ""
    def aggiungiFornitore(self , cittaSede, denominazione, indirizzoSede, partitaIva, tipoProfessione):
        self.cittaSede = cittaSede
        self.denominazione = denominazione
        self.indirizzoSede = indirizzoSede
        self.partitaIva = partitaIva
        self.tipoProfessione = tipoProfessione

    def getFornitore(self):
        return {
            "cittaSede": self.cittaSede,
            "denominazione": self.denominazione,
            "indirizzoSede": self.indirizzoSede,
            "partitaIva": self.partitaIva,
            "tipoProfessione": self.tipoProfessione
        }
