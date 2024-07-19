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
    def visualizzaCreditoCondomino(self):
        pass

    def visualizzaDebitoFornitore(self):
        pass

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
            pdf.cell(0, 10, "Immobile: " + Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(rata.unitaImmobiliare).immobile).denominazione, new_x=XPos.END)
            pdf.set_x(3 * pdf.w / 4)
            pdf.cell(0, 10, "Data: " + rata.dataPagamento.strftime("%d/%m/%Y"), new_x=XPos.START, new_y=YPos.NEXT)
            pdf.cell(0, 10, "Ricevuta n. " + str(rata.numeroRicevuta), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            print("i")
            pdf.cell(0, 10, "Si riceve dal Sig. " + rata.versante + " la somma di € " + '%.2f' % rata.importo + "", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            print("iii")
            pdf.cell(0, 10, "per riscossione " + rata.descrizione, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            print("iiii")

        pdf = FPDF(format='A5')
        pdf.add_page()
        pdf.set_font("helvetica", "", 13)

        print_dati_rata()
        """
        pdf.set_line_width(0.3)
        pdf.set_draw_color(r=0, g=0, b=0)
        pdf.line(pdf.x, pdf.eph/2, pdf.x + pdf.epw, pdf.eph/2)

        print_dati_rata()
        """
        return pdf

