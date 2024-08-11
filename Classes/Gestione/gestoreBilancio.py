from fpdf import FPDF, Align, XPos, YPos

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class GestoreBilancio:

    @staticmethod
    def visualizzaProspettiEsercizio(bilancio):
        def printSpesePreventivate(pdf, bilancio):
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(0, 10, "Spese preventivate", align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)

            with pdf.table(width=pdf.epw, col_widths=(75, 25), text_align=("LEFT", "RIGHT")) as table:

                heading = table.row()
                heading.cell("DESCRIZIONE TIPOLOGIA DI SPESA", align=Align.C)
                heading.cell("PREVENTIVO ANALITICO", align=Align.C)

                totale_preventivato = 0.0
                for tabella_millesimale in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileById(bilancio.immobile)).values():

                    pdf.set_font("helvetica", "BI", 9)
                    tabella_millesimale_row = table.row()
                    tabella_millesimale_row.cell(f"{tabella_millesimale.nome} - {tabella_millesimale.descrizione}", align=Align.C)
                    tabella_millesimale_row.cell("%.2f" % sum(list(bilancio.spesePreventivate[tabella_millesimale.codice].values())))
                    pdf.set_font("helvetica", "", 9)
                    for cod_tipo_spesa in tabella_millesimale.tipologieSpesa:
                        tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(cod_tipo_spesa)
                        row = table.row()
                        row.cell("> " + tipo_spesa.descrizione)
                        row.cell("%.2f" % bilancio.spesePreventivate[tabella_millesimale.codice][cod_tipo_spesa])
                        totale_preventivato += bilancio.spesePreventivate[tabella_millesimale.codice][cod_tipo_spesa]

                pdf.set_font("helvetica", "B", 9)
                totale_row = table.row()
                totale_row.cell("TOTALE")
                totale_row.cell("%.2f" % totale_preventivato)

        def printSpeseConsuntivate(pdf, bilancio):
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(0, 10, "Spese consuntivate", align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)

            with pdf.table(width=pdf.epw, col_widths=(55, 15, 15, 15), text_align=("LEFT", "RIGHT", "RIGHT", "RIGHT")) as table:
                heading = table.row()
                heading.cell("DESCRIZIONE TIPOLOGIA DI SPESA", align=Align.C)
                heading.cell("CONSUNTIVO ANALITICO", align=Align.C)
                heading.cell("PREVENTIVO ANALITICO", align=Align.C)
                heading.cell("RISPARMIO o DEFICIT(-)", align=Align.C)

                totale_preventivato = 0.0
                totale_consuntivato = 0.0
                totale_risparmio = 0.0
                for tabella_millesimale in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileById(bilancio.immobile)).values():

                    pdf.set_font("helvetica", "BI", 9)
                    tabella_millesimale_row = table.row()
                    tabella_millesimale_row.cell(f"{tabella_millesimale.nome} - {tabella_millesimale.descrizione}", align=Align.C)
                    tabella_millesimale_row.cell("%.2f" % sum(list(bilancio.speseConsuntivate[tabella_millesimale.codice].values())))
                    tabella_millesimale_row.cell("%.2f" % sum(list(bilancio.spesePreventivate[tabella_millesimale.codice].values())))
                    tabella_millesimale_row.cell("%.2f" % (sum(list(bilancio.speseConsuntivate[tabella_millesimale.codice].values())) - sum(list(bilancio.spesePreventivate[tabella_millesimale.codice].values()))))
                    pdf.set_font("helvetica", "", 9)
                    for cod_tipo_spesa in tabella_millesimale.tipologieSpesa:
                        tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(cod_tipo_spesa)
                        row = table.row()
                        row.cell("> " + tipo_spesa.descrizione)
                        row.cell("%.2f" % bilancio.speseConsuntivate[tabella_millesimale.codice][cod_tipo_spesa])
                        row.cell("%.2f" % bilancio.spesePreventivate[tabella_millesimale.codice][cod_tipo_spesa])
                        row.cell("%.2f" % (bilancio.speseConsuntivate[tabella_millesimale.codice][cod_tipo_spesa] - bilancio.spesePreventivate[tabella_millesimale.codice][cod_tipo_spesa]))
                        totale_consuntivato += bilancio.speseConsuntivate[tabella_millesimale.codice][cod_tipo_spesa]
                        totale_preventivato += bilancio.spesePreventivate[tabella_millesimale.codice][cod_tipo_spesa]
                        totale_risparmio += bilancio.speseConsuntivate[tabella_millesimale.codice][cod_tipo_spesa] - bilancio.spesePreventivate[tabella_millesimale.codice][cod_tipo_spesa]
                pdf.set_font("helvetica", "B", 9)
                totale_row = table.row()
                totale_row.cell("TOTALE")
                totale_row.cell("%.2f" % totale_consuntivato)
                totale_row.cell("%.2f" % totale_preventivato)
                totale_row.cell("%.2f" % totale_risparmio)

        def printRipartizioneConsuntivo(pdf, bilancio):
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(0, 10, "Ripartizione spese consuntivate", align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)
            tabelle_millesimali_immobile = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileById(bilancio.immobile)).values())

            column_width = [1] * len(tabelle_millesimali_immobile) + [3] + [1] * len(tabelle_millesimali_immobile) + [2] * 4
            totale_consuntivo = 0.0
            print(column_width)
            with pdf.table(width=pdf.epw, num_heading_rows=2) as table:
                pdf.set_font("helvetica", "", 7)

                heading_top = table.row()

                heading_top.cell("MILLESIMI", colspan=len(tabelle_millesimali_immobile))
                heading_top.cell("QUOTE", colspan=len(tabelle_millesimali_immobile))

                heading = table.row()
                for tabella in tabelle_millesimali_immobile:
                    heading.cell(tabella.nome.upper())

                heading.cell("UNITÀ IMMOBILIARE", rowspan=2)

                for tabella in tabelle_millesimali_immobile:
                    heading.cell(tabella.nome.upper())

                heading.cell("TOTALE CONSUNTIVO", rowspan=2)
                heading.cell("CONGUAGLIO ANNO PRECEDENTE", rowspan=2)
                heading.cell("TOTALE VERSATO", rowspan=2)
                heading.cell("CONGUAGLIO ANNO ATTUALE", rowspan=2)

                pdf.set_font("helvetica", "", 9)
                for unita_immobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(bilancio.immobile)).values():
                    unita_row = table.row()
                    for tabella in tabelle_millesimali_immobile:
                        unita_row.cell("%.2f" % tabella.millesimi[unita_immobiliare.codice])

                    pdf.set_font("helvetica", "BI", 9)
                    if unita_immobiliare.tipoUnitaImmobiliare == "Appartamento":
                        proprietario = Condomino.ricercaCondominoByCF([item for item in unita_immobiliare.condomini.keys() if unita_immobiliare.condomini[item] == "Proprietario"][0])
                        unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} Scala {unita_immobiliare.scala} Int.{unita_immobiliare.interno} di\n{proprietario.cognome} {proprietario.nome}")
                    else:
                        proprietario = Condomino.ricercaCondominoByCF([item for item in unita_immobiliare.condomini.keys() if unita_immobiliare.condomini[item] == "Proprietario"][0])
                        unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} di\n{proprietario.cognome} {proprietario.nome}")

                    pdf.set_font("helvetica", "", 9)
                    totale_cons_unita = 0.0
                    print("prova", unita_immobiliare.getInfoUnitaImmobiliare())
                    for tabella in tabelle_millesimali_immobile:
                        print("--prova")
                        unita_row.cell("%.2f" % bilancio.ripartizioneSpeseConsuntivate[tabella.codice][unita_immobiliare.codice])
                        print("--prova")
                        totale_cons_unita += bilancio.ripartizioneSpeseConsuntivate[tabella.codice][unita_immobiliare.codice]
                    totale_consuntivo += totale_cons_unita

                    print("prova")
                    unita_row.cell("%.2f" % totale_cons_unita)
                    print("prova")
                    unita_row.cell("%.2f" % bilancio.conguaglioPrecedente[unita_immobiliare.codice])
                    print("prova")
                    unita_row.cell("%.2f" % bilancio.rateVersate[unita_immobiliare.codice])
                    print("prova")
                    unita_row.cell("%.2f" % bilancio.ripartizioneConguaglio[unita_immobiliare.codice])
                    print("provaa")

                pdf.set_font("helvetica", "", 9)
                print("fine for unita")
                totale_row = table.row()

                for tabella in tabelle_millesimali_immobile:
                    totale_row.cell("%.2f" % sum(list(tabella.millesimi.values())))

                totale_row.cell("TOTALE")

                for tabella in tabelle_millesimali_immobile:
                    totale_row.cell("%.2f" % sum(list(bilancio.ripartizioneSpeseConsuntivate[tabella.codice].values())))

                totale_row.cell("%.2f" % totale_consuntivo)
                totale_row.cell("%.2f" % sum(list(bilancio.conguaglioPrecedente.values())))
                totale_row.cell("%.2f" % sum(list(bilancio.rateVersate.values())))
                totale_row.cell("%.2f" % sum(list(bilancio.ripartizioneConguaglio.values())))
                print("fine rip cons")

        def printRipartizionePreventivo(pdf, bilancio):
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(0, 10, "Ripartizione spese preventivate", align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)

        print("dentro visProspetti")
        pdf = FPDF()
        bilancio = Bilancio.ricercaBilancioByCodice(bilancio.codice)
        pdf.add_page()
        print("dentro visProspetti")
        printSpesePreventivate(pdf, bilancio)

        pdf.add_page()
        print("dentro visProspetti")
        printSpeseConsuntivate(pdf, bilancio)

        pdf.add_page("L")
        print("dentro visProspetti")
        printRipartizioneConsuntivo(pdf, bilancio)
        printRipartizioneConsuntivo()
        print("fatto")

        pdf.add_page("L")
        print("dentro visProspetti")
        printRipartizionePreventivo(pdf, bilancio)

        return pdf
