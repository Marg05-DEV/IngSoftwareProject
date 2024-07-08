import os
import pickle

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile

from fpdf import FPDF, Align, YPos, XPos


class GestoreRegistroAnagrafe:
    @staticmethod
    def ricercaUnitaImmobiliareByInterno(interno):
        nome_file = 'Dati/UnitaImmobiliari.pickle'
        print("dentro la ricerca")
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = dict(pickle.load(f))
                for unitaImmobiliare in unitaImmobiliari.values():
                    if unitaImmobiliare.interno == interno:
                        return unitaImmobiliare
                return None
        else:
            return None

    @staticmethod
    def ordinaUnitaImmobiliariByScala(list_unitaImmobiliari, isDecrescente=False):
        print("----------------------------------------------")
        for item in list_unitaImmobiliari:
            print(item.getInfoUnitaImmobiliare())

        print("----------------------------------------------")
        list_unitaImmobiliari.sort(key=lambda immobile: immobile.interno)
        for item in list_unitaImmobiliari:
            print(item.getInfoUnitaImmobiliare())

        print("----------------------------------------------")
        list_unitaImmobiliari.sort(key=lambda immobile: immobile.scala)
        for item in list_unitaImmobiliari:
            print(item.getInfoUnitaImmobiliare())

        print("----------------------------------------------")
        list_unitaImmobiliari.sort(key=lambda immobile: immobile.tipoUnitaImmobiliare)
        for item in list_unitaImmobiliari:
            print(item.getInfoUnitaImmobiliare())

    @staticmethod
    def ordinaUnitaImmobiliariByInterno(list_unitaImmobiliari, isDecrescente=False):
        print("----------------------------------------------")
        list_unitaImmobiliari.sort(key=lambda immobile: immobile.scala)
        for item in list_unitaImmobiliari:
            print(item.getInfoUnitaImmobiliare())

        print("----------------------------------------------")
        list_unitaImmobiliari.sort(key=lambda immobile: immobile.interno)
        for item in list_unitaImmobiliari:
            print(item.getInfoUnitaImmobiliare())

        print("----------------------------------------------")
        list_unitaImmobiliari.sort(key=lambda immobile: immobile.tipoUnitaImmobiliare)
        for item in list_unitaImmobiliari:
            print(item.getInfoUnitaImmobiliare())

    @staticmethod
    def ordinaUnitaImmobiliariByNominativoProprietario(list_unitaImmobiliari, isDecrescente):
        proprietari_unita_immobiliari = []
        senza_proprietario = []
        senza_condomini = []
        print('inizio ordinamento proprietario')
        for item in list_unitaImmobiliari:
            print("------------------------------------------------------------------------------------------")
            print(item.getInfoUnitaImmobiliare())
            proprietario_cf = [key for key, value in item.condomini.items() if value == 'Proprietario']
            print(proprietario_cf)
            if len(proprietario_cf) < 1:
                print("no prop")
                if len(item.condomini) < 1:
                    print("nessun condomino")
                    senza_condomini.append(item)
                else:
                    print("nessun propriestario")
                    senza_proprietario.append(item)
            else:
                print("si prop")
                proprietario = Condomino.ricercaCondominoByCF(proprietario_cf[0])
                proprietari_unita_immobiliari.append([item.codice, proprietario.cognome.upper(), proprietario.nome.upper()])

        print("fine aver scorso unita")
        print(senza_proprietario)
        print(senza_condomini)
        print(proprietari_unita_immobiliari)
        if len(senza_proprietario) > 0:
            GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByScala(senza_proprietario)
        if len(senza_condomini) > 0:
            GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByScala(senza_condomini)
        print("ordinati lo schifo")
        proprietari_unita_immobiliari.sort(reverse=isDecrescente, key=lambda row: row[2])
        proprietari_unita_immobiliari.sort(reverse=isDecrescente, key=lambda row: row[1])
        print(senza_proprietario)
        print(senza_condomini)
        print(proprietari_unita_immobiliari)

        sorted_unitaImmobiliari = []
        for proprietario in proprietari_unita_immobiliari:
            for unitaImmobiliare in list_unitaImmobiliari:
                if unitaImmobiliare.codice == proprietario[0]:
                    sorted_unitaImmobiliari.append(unitaImmobiliare)
                    break

        for item in senza_proprietario:
            sorted_unitaImmobiliari.append(item)
        for item in senza_condomini:
            sorted_unitaImmobiliari.append(item)

        for i in range(len(list_unitaImmobiliari)):
            list_unitaImmobiliari[i] = sorted_unitaImmobiliari[i]

    @staticmethod
    def ricercaCondominoByNome(nome):
        nome_file = 'Dati/Condomini.pickle'
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                condomini = pickle.load(f)
                for condomino in condomini.values():
                    if condomino.nome == nome:
                        return condomino
                return None
        else:
            return None

    @staticmethod
    def ordinaCondominoByNominativo(list_condomini, isDecrescente):
        sorted_nominativo = []
        for condomino in list_condomini:
            sorted_nominativo.append((condomino.cognome + " " + condomino.nome).upper())
        sorted_nominativo.sort(reverse=isDecrescente)
        sorted_condomini = []
        for nominativo in sorted_nominativo:
            for condomino in list_condomini:
                if (condomino.cognome + " " + condomino.nome).upper() == nominativo:
                    sorted_condomini.append(condomino)
                    break
        for i in range(len(list_condomini)):
            list_condomini[i] = sorted_condomini[i]

    @staticmethod
    def generaPDFRegistroAnagrafeCondominiale(immobile):
        def print_anagrafica(pdf, condomino):
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Nome:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, condomino.nome, new_x=XPos.END)

            pdf.set_x(pdf.w / 2)
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Cognome:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, condomino.cognome, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Nato il:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, condomino.dataDiNascita.strftime("%m/%d/%Y"), new_x=XPos.END)

            pdf.set_x(pdf.w / 3)
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Città:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, condomino.luogoDiNascita, new_x=XPos.END)

            pdf.set_x((2 * pdf.w) / 3)
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Provincia:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, condomino.provinciaDiNascita, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Residenza:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, condomino.residenza, new_x=XPos.END)

            pdf.set_x((3 * pdf.w) / 5)
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Telefono:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, condomino.telefono, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Codice Fiscale:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, condomino.codiceFiscale, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "Registro Anagrafe Condominiale", align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)
        pdf.cell(0, 10, "dell'immobile:", align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)
        pdf.cell(0, 10, immobile.denominazione, align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)

        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(immobile)
        print("unita_immobiliari prese", unitaImmobiliari)
        for unitaImmobiliare in unitaImmobiliari.values():
            print("---------------------- ", unitaImmobiliare, "-------------------------")

            proprietario = None
            proprietari = [Condomino.ricercaCondominoByCF(cf) for cf in unitaImmobiliare.condomini.keys() if unitaImmobiliare.condomini[cf] == 'Proprietario']
            if len(proprietari) > 0:
                proprietario = proprietari[0]
            comproprietari = [Condomino.ricercaCondominoByCF(cf) for cf in unitaImmobiliare.condomini.keys() if unitaImmobiliare.condomini[cf] == 'Coproprietario']
            inquilini = [Condomino.ricercaCondominoByCF(cf) for cf in unitaImmobiliare.condomini.keys() if unitaImmobiliare.condomini[cf] == 'Inquilino']

            print("PROPRIETARIO")
            if proprietari:
                print(proprietario.getDatiAnagraficiCondomino())

            print("\nCOMPROPRIETARI")
            for comproprietario in comproprietari:
                print(comproprietario.getDatiAnagraficiCondomino())

            print("\nINQUILINI")
            for inquilino in inquilini:
                print(inquilino.getDatiAnagraficiCondomino())

            pdf.add_page()
            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, "DATI ANAGRAFICI PROPRIETARIO UNITÀ IMMOBILIARE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if proprietari:
                print_anagrafica(pdf, proprietario)
            else:
                pdf.set_font("helvetica", "I", 14)
                pdf.cell(0, 10, "Nessun proprietario presente", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            print("fine anagrafica")

            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Tipo di unità immobiliare:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)

            if unitaImmobiliare.tipoUnitaImmobiliare == "Appartamento":
                pdf.cell(0, 10, unitaImmobiliare.tipoUnitaImmobiliare, new_x=XPos.END)

                pdf.set_x(pdf.w / 2)
                pdf.set_font("helvetica", "B", 12)
                pdf.cell(0, 10, "Scala:", new_x=XPos.END)
                pdf.set_font("helvetica", "", 12)
                pdf.cell(0, 10, str(unitaImmobiliare.scala), new_x=XPos.END)

                pdf.set_x((3 * pdf.w) / 4)
                pdf.set_font("helvetica", "B", 12)
                pdf.cell(0, 10, "Interno:", new_x=XPos.END)
                pdf.set_font("helvetica", "", 12)
                pdf.cell(0, 10, str(unitaImmobiliare.interno), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                pdf.cell(0, 10, unitaImmobiliare.tipoUnitaImmobiliare, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_font("helvetica", "B", 13)
            pdf.cell(0, 10, "Dati Catastali:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Foglio:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, str(unitaImmobiliare.foglio), new_x=XPos.END)

            pdf.set_x(pdf.w / 6)
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Particella:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, str(unitaImmobiliare.particella), new_x=XPos.END)

            pdf.set_x((2 * pdf.w) / 6)
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Subalterno:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, str(unitaImmobiliare.subalterno), new_x=XPos.END)

            pdf.set_x((3 * pdf.w) / 6)
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "ZC:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, str(unitaImmobiliare.ZC), new_x=XPos.END)

            pdf.set_x((5 * pdf.w) / 8)
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Classe:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, str(unitaImmobiliare.classe), new_x=XPos.END)

            pdf.set_x((6 * pdf.w) / 8)
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, "Categoria:", new_x=XPos.END)
            pdf.set_font("helvetica", "", 12)
            pdf.cell(0, 10, str(unitaImmobiliare.categoria), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_line_width(0.3)
            pdf.set_draw_color(r=0, g=0, b=0)
            pdf.line(pdf.x, pdf.y, pdf.x + pdf.epw, pdf.y)

            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, "DATI ANAGRAFICI EVENTUALE COMPROPRIETARIO UNITÀ IMMOBILIARE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if comproprietari:
                print_anagrafica(pdf, comproprietari[0])
                if len(comproprietari) > 1:
                    pdf.set_font("helvetica", "B", 12)
                    pdf.cell(0, 10, "Altri comproprietari:", new_x=XPos.END)
                    indent_x = pdf.x
                    for i in range(1, len(comproprietari)):
                        pdf.set_font("helvetica", "B", 10)
                        pdf.cell(0, 10, "Nome:", new_x=XPos.END)
                        pdf.set_font("helvetica", "", 10)
                        pdf.cell(0, 10, comproprietari[i].nome, new_x=XPos.END)

                        pdf.set_x(indent_x + ((pdf.w - indent_x) / 3))
                        pdf.set_font("helvetica", "B", 10)
                        pdf.cell(0, 10, "Cognome:", new_x=XPos.END)
                        pdf.set_font("helvetica", "", 10)
                        pdf.cell(0, 10, comproprietari[i].cognome, new_x=XPos.END)

                        pdf.set_x(indent_x + (2 * (pdf.w - indent_x) / 3))
                        pdf.set_font("helvetica", "B", 10)
                        pdf.cell(0, 10, "CF:", new_x=XPos.END)
                        pdf.set_font("helvetica", "", 10)
                        pdf.cell(0, 10, comproprietari[i].codiceFiscale, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

                        if not i == (len(comproprietari) - 1):
                            pdf.set_x(indent_x)
            else:
                pdf.set_font("helvetica", "I", 14)
                pdf.cell(0, 10, "Nessun comproprietario presente", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.line(pdf.x, pdf.y, pdf.x + pdf.epw, pdf.y)

            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, "DATI ANAGRAFICI INQUILINO (SE PRESENTE)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if inquilini:
                print_anagrafica(pdf, inquilini[0])
                if len(inquilini) > 1:
                    pdf.set_font("helvetica", "B", 12)
                    pdf.cell(0, 10, "Altri inquilini:", new_x=XPos.END)
                    indent_x = pdf.x
                    for i in range(1, len(inquilini)):
                        pdf.set_font("helvetica", "B", 10)
                        pdf.cell(0, 10, "Nome:", new_x=XPos.END)
                        pdf.set_font("helvetica", "", 10)
                        pdf.cell(0, 10, inquilini[i].nome, new_x=XPos.END)

                        pdf.set_x(indent_x + ((pdf.w - indent_x) / 3))
                        pdf.set_font("helvetica", "B", 10)
                        pdf.cell(0, 10, "Cognome:", new_x=XPos.END)
                        pdf.set_font("helvetica", "", 10)
                        pdf.cell(0, 10, inquilini[i].cognome, new_x=XPos.END)

                        pdf.set_x(indent_x + (2 * (pdf.w - indent_x) / 3))
                        pdf.set_font("helvetica", "B", 10)
                        pdf.cell(0, 10, "CF:", new_x=XPos.END)
                        pdf.set_font("helvetica", "", 10)
                        pdf.cell(0, 10, inquilini[i].codiceFiscale, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

                        if not i == (len(inquilini) - 1):
                            pdf.set_x(indent_x)
            else:
                pdf.set_font("helvetica", "I", 14)
                pdf.cell(0, 10, "Nessun inquilino presente", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        return pdf



