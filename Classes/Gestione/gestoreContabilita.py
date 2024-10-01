import os
import pickle

from fpdf import FPDF, Align, XPos, YPos

from Classes.Contabilita.rata import Rata
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.fornitore import Fornitore
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class GestoreContabilita:
    def visualizzaSaldoCassa(self):
        saldo_cassa_contanti = 0.0
        saldo_cassa_A_B = 0.0
        if os.path.isfile("Dati/Rata.pickle"):
            with open("Dati/Rate.pickle", 'rb') as f:
                rate = pickle.load(f)
                for rata in rate.values():
                    if rata.tipoPagamento == "Contanti":
                        saldo_cassa_contanti += rata.importo
                    if rata.tipoPagamento == "Assegno Bancario":
                        saldo_cassa_A_B += rata.importo
                return {saldo_cassa_contanti,
                        saldo_cassa_A_B}

    def visualizzaStatoPatrimonialeSpese(self, immobile):
        if os.path.isfile("Dati/Spesa.pickle"):
            with open("Dati/Spesa.pickle", 'rb') as f:
                spese = pickle.load(f)
                for spesa in spese.values():
                    if spesa.pagata != True and spesa.immobile == immobile:
                        return "Spesa " + spesa.codice + " non pagata dell'immobile selezionato "

    def visualizzaStatoPatrimonialeRate(self):
        if os.path.isfile("Dati/Rate.pickle"):
            with open("Dati/Rate.pickle", 'rb') as f:
                rate = pickle.load(f)
                for rata in rate.values():
                    if rata.pagata != True:
                        return "Rata " + rata.codice + " non versata dell'immobile selezionato "

    @staticmethod
    def generaRicevuta(rata):

        def print_dati_rata():
            pdf.set_font("helvetica", "", 11)
            pdf.cell(0, 12, "Immobile: " + Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(rata.unitaImmobiliare).immobile).denominazione, new_x=XPos.END)
            pdf.set_x(2 * pdf.w / 3)
            pdf.cell(0, 12, "Data: " + rata.dataPagamento.strftime("%d/%m/%Y"), new_x=XPos.START, new_y=YPos.NEXT)
            pdf.set_x(2 * pdf.w / 3)
            pdf.cell(0, 12, "Ricevuta n. " + str(rata.numeroRicevuta), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 12, f"Si riceve dal Sig. {rata.versante} la somma di euro {'%.2f' % rata.importo}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 12, "per riscossione " + rata.descrizione, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_x(3 * pdf.w / 5)
            pdf.cell(0, 12, "L'AMMINISTRATORE", new_x=XPos.RMARGIN, new_y=YPos.NEXT)

        pdf = FPDF('portrait', 'mm', 'A5')
        pdf.add_page()
        pdf.set_font("helvetica", "", 11)

        pdf.cell(0, pdf.eph/2 - 10, "", 1, new_x=XPos.START)
        print_dati_rata()
        pdf.set_y(pdf.eph/2 - 10)
        pdf.set_font("helvetica", "", 7)
        pdf.cell(0, 10, str(rata.codice), align='R', new_x=XPos.LMARGIN)

        pdf.set_y(pdf.h/2 - 10)
        pdf.cell(0, 0.1, "", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_y(pdf.h / 2 -10 + ((pdf.h - pdf.eph -20)/2))
        pdf.cell(0, pdf.eph/2 - 10, "", 1, new_x=XPos.START)
        print_dati_rata()
        pdf.set_y(pdf.eph - 10)
        pdf.set_font("helvetica", "", 7)
        pdf.cell(0, 10, str(rata.codice), align='R', new_x=XPos.LMARGIN)

        return pdf

