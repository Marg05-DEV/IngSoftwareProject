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
                for tabella_millesimale in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(
                        Immobile.ricercaImmobileById(bilancio.immobile)).values():

                    pdf.set_font("helvetica", "BI", 9)
                    tabella_millesimale_row = table.row()
                    tabella_millesimale_row.cell(f"{tabella_millesimale.nome} - {tabella_millesimale.descrizione}",
                                                 align=Align.C)
                    tabella_millesimale_row.cell(
                        "%.2f" % sum(list(bilancio.spesePreventivate[tabella_millesimale.codice].values())))
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

            with pdf.table(width=pdf.epw, col_widths=(55, 15, 15, 15),
                           text_align=("LEFT", "RIGHT", "RIGHT", "RIGHT")) as table:
                heading = table.row()
                heading.cell("DESCRIZIONE TIPOLOGIA DI SPESA", align=Align.C)
                heading.cell("CONSUNTIVO ANALITICO", align=Align.C)
                heading.cell("PREVENTIVO ANALITICO", align=Align.C)
                heading.cell("RISPARMIO o DEFICIT(-)", align=Align.C)

                totale_preventivato = 0.0
                totale_consuntivato = 0.0
                totale_risparmio = 0.0
                for tabella_millesimale in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(
                        Immobile.ricercaImmobileById(bilancio.immobile)).values():

                    pdf.set_font("helvetica", "BI", 9)
                    tabella_millesimale_row = table.row()
                    tabella_millesimale_row.cell(f"{tabella_millesimale.nome} - {tabella_millesimale.descrizione}",
                                                 align=Align.C)
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
                        row.cell("%.2f" % (bilancio.speseConsuntivate[tabella_millesimale.codice][cod_tipo_spesa] -
                                           bilancio.spesePreventivate[tabella_millesimale.codice][cod_tipo_spesa]))
                        totale_consuntivato += bilancio.speseConsuntivate[tabella_millesimale.codice][cod_tipo_spesa]
                        totale_preventivato += bilancio.spesePreventivate[tabella_millesimale.codice][cod_tipo_spesa]
                        totale_risparmio += bilancio.speseConsuntivate[tabella_millesimale.codice][cod_tipo_spesa] - \
                                            bilancio.spesePreventivate[tabella_millesimale.codice][cod_tipo_spesa]
                pdf.set_font("helvetica", "B", 9)
                totale_row = table.row()
                totale_row.cell("TOTALE")
                totale_row.cell("%.2f" % totale_consuntivato)
                totale_row.cell("%.2f" % totale_preventivato)
                totale_row.cell("%.2f" % totale_risparmio)

        def printRipartizioneConsuntivo(pdf, bilancio):
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(0, 10, "Ripartizione spese consuntivate", align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)
            tabelle_millesimali_immobile = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(
                Immobile.ricercaImmobileById(bilancio.immobile)).values())

            column_width = [1] * len(tabelle_millesimali_immobile) + [4] + [1] * len(tabelle_millesimali_immobile) + [
                2] * 4
            column_alignment = ["CENTER"] * len(tabelle_millesimali_immobile) + ["LEFT"] + ["RIGHT"] * len(
                tabelle_millesimali_immobile) + ["RIGHT"] * 4
            totale_consuntivo = 0.0

            with pdf.table(width=pdf.epw, num_heading_rows=2, col_widths=tuple(column_width),
                           text_align=tuple(column_alignment)) as table:
                pdf.set_font("helvetica", "B", 7)

                heading_top = table.row()

                heading_top.cell("MILLESIMI", align=Align.C, colspan=len(tabelle_millesimali_immobile))
                heading_top.cell("UNITÀ IMMOBILIARE", align=Align.C, rowspan=2)
                heading_top.cell("QUOTE", align=Align.C, colspan=len(tabelle_millesimali_immobile))

                heading_top.cell("TOTALE CONSUNTIVO", align=Align.C, rowspan=2)
                heading_top.cell("CONGUAGLIO ANNO PRECEDENTE", align=Align.C, rowspan=2)
                heading_top.cell("TOTALE VERSATO", align=Align.C, rowspan=2)
                heading_top.cell("CONGUAGLIO ANNO ATTUALE", align=Align.C, rowspan=2)

                heading = table.row()
                for tabella in tabelle_millesimali_immobile:
                    heading.cell(tabella.nome.upper(), align=Align.C)

                for tabella in tabelle_millesimali_immobile:
                    heading.cell(tabella.nome.upper(), align=Align.C)

                pdf.set_font("helvetica", "", 8)
                for unita_immobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(bilancio.immobile)).values():
                    unita_row = table.row()
                    for tabella in tabelle_millesimali_immobile:
                        unita_row.cell("%.2f" % tabella.millesimi[unita_immobiliare.codice])

                    pdf.set_font("helvetica", "BI", 7)

                    proprietario = [item for item in unita_immobiliare.condomini.keys() if unita_immobiliare.condomini[item] == "Proprietario"]
                    if unita_immobiliare.tipoUnitaImmobiliare == "Appartamento":
                        if unita_immobiliare.condomini:
                            if proprietario:
                                proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                                unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} Sc. {unita_immobiliare.scala} Int.{unita_immobiliare.interno} di {proprietario.cognome} {proprietario.nome}")
                            else:
                                unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} Sc. {unita_immobiliare.scala} Int.{unita_immobiliare.interno} di Nessun Proprietario")
                        else:
                            unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} Sc. {unita_immobiliare.scala} Int.{unita_immobiliare.interno} con Nessun Condomino")
                    else:
                        if unita_immobiliare.condomini:
                            if proprietario:
                                proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                                unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}")
                            else:
                                unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} di Nessun Proprietario")
                        else:
                            unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} con Nessun Condomino")

                    pdf.set_font("helvetica", "", 8)
                    totale_cons_unita = 0.0

                    for tabella in tabelle_millesimali_immobile:
                        unita_row.cell("%.2f" % bilancio.ripartizioneSpeseConsuntivate[tabella.codice][unita_immobiliare.codice])
                        totale_cons_unita += bilancio.ripartizioneSpeseConsuntivate[tabella.codice][
                            unita_immobiliare.codice]

                    totale_consuntivo += totale_cons_unita

                    unita_row.cell("%.2f" % totale_cons_unita)
                    unita_row.cell("%.2f" % bilancio.conguaglioPrecedente[unita_immobiliare.codice])
                    unita_row.cell("%.2f" % bilancio.rateVersate[unita_immobiliare.codice])
                    unita_row.cell("%.2f" % bilancio.ripartizioneConguaglio[unita_immobiliare.codice])

                pdf.set_font("helvetica", "I", 8)
                totale_row = table.row()

                for tabella in tabelle_millesimali_immobile:
                    totale_row.cell("%.2f" % sum(list(tabella.millesimi.values())))

                pdf.set_font("helvetica", "BI", 9)
                totale_row.cell("TOTALE")

                pdf.set_font("helvetica", "I", 8)

                for tabella in tabelle_millesimali_immobile:
                    totale_row.cell("%.2f" % sum(list(bilancio.ripartizioneSpeseConsuntivate[tabella.codice].values())))

                totale_row.cell("%.2f" % totale_consuntivo)
                totale_row.cell("%.2f" % sum(list(bilancio.conguaglioPrecedente.values())))
                totale_row.cell("%.2f" % sum(list(bilancio.rateVersate.values())))
                totale_row.cell("%.2f" % sum(list(bilancio.ripartizioneConguaglio.values())))

        def printRipartizionePreventivo(pdf, bilancio):
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(0, 10, "Ripartizione spese preventivate", align=Align.C, new_x=XPos.LEFT, new_y=YPos.NEXT)

            tabelle_millesimali_immobile = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileById(bilancio.immobile)).values())

            column_width = [1] * len(tabelle_millesimali_immobile) + [4] + [1] * len(tabelle_millesimali_immobile) + [
                2] * 3 + [1.5] * bilancio.numeroRate
            column_alignment = ["CENTER"] * len(tabelle_millesimali_immobile) + ["LEFT"] + ["RIGHT"] * len(
                tabelle_millesimali_immobile) + ["RIGHT"] * 3 + ["RIGHT"] * bilancio.numeroRate
            totale_preventivo = 0.0
            totale_rate = [0.0] * bilancio.numeroRate
            with pdf.table(width=pdf.epw, num_heading_rows=2, col_widths=tuple(column_width),
                           text_align=tuple(column_alignment)) as table:
                pdf.set_font("helvetica", "B", 7)

                heading_top = table.row()

                heading_top.cell("MILLESIMI", align=Align.C, colspan=len(tabelle_millesimali_immobile))
                heading_top.cell("UNITÀ IMMOBILIARE", align=Align.C, rowspan=2)
                heading_top.cell("QUOTE", align=Align.C, colspan=len(tabelle_millesimali_immobile))

                heading_top.cell("TOTALE PREVENTIVO", align=Align.C, rowspan=2)
                heading_top.cell("CONGUAGLIO ANNO ATTUALE", align=Align.C, rowspan=2)
                heading_top.cell("TOTALE DA VERSARE", align=Align.C, rowspan=2)

                for i in range(bilancio.numeroRate):
                    heading_top.cell(f"{i + 1}a RATA", align=Align.C)

                heading = table.row()
                for tabella in tabelle_millesimali_immobile:
                    heading.cell(tabella.nome.upper(), align=Align.C)

                for tabella in tabelle_millesimali_immobile:
                    heading.cell(tabella.nome.upper(), align=Align.C)

                pdf.set_font("helvetica", "B", 6)
                for i in range(bilancio.numeroRate):
                    heading.cell(f"SCADE IL {bilancio.scadenzaRate[i].strftime('%d/%m/%Y')}", align=Align.C)

                pdf.set_font("helvetica", "", 7)
                for unita_immobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(bilancio.immobile)).values():
                    unita_row = table.row()

                    for tabella in tabelle_millesimali_immobile:
                        unita_row.cell("%.2f" % tabella.millesimi[unita_immobiliare.codice])

                    pdf.set_font("helvetica", "BI", 8)

                    proprietario = [item for item in unita_immobiliare.condomini.keys() if
                                    unita_immobiliare.condomini[item] == "Proprietario"]
                    if unita_immobiliare.tipoUnitaImmobiliare == "Appartamento":
                        if unita_immobiliare.condomini:
                            if proprietario:
                                proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                                unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} Sc. {unita_immobiliare.scala} Int.{unita_immobiliare.interno} di {proprietario.cognome} {proprietario.nome}")
                            else:
                                unita_row.cell(
                                    f"{unita_immobiliare.tipoUnitaImmobiliare} Sc. {unita_immobiliare.scala} Int.{unita_immobiliare.interno} di Nessun Proprietario")
                        else:
                            unita_row.cell(
                                f"{unita_immobiliare.tipoUnitaImmobiliare} Sc. {unita_immobiliare.scala} Int.{unita_immobiliare.interno} con Nessun Condomino")
                    else:
                        if unita_immobiliare.condomini:
                            if proprietario:
                                proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                                unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}")
                            else:
                                unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} di Nessun Proprietario")
                        else:
                            unita_row.cell(f"{unita_immobiliare.tipoUnitaImmobiliare} con Nessun Condomino")

                    pdf.set_font("helvetica", "", 7)
                    totale_prev_unita = 0.0

                    for tabella in tabelle_millesimali_immobile:
                        unita_row.cell("%.2f" % bilancio.ripartizioneSpesePreventivate[tabella.codice][unita_immobiliare.codice])
                        totale_prev_unita += bilancio.ripartizioneSpesePreventivate[tabella.codice][unita_immobiliare.codice]

                    totale_preventivo += totale_prev_unita

                    unita_row.cell("%.2f" % totale_prev_unita)
                    unita_row.cell("%.2f" % bilancio.ripartizioneConguaglio[unita_immobiliare.codice])
                    unita_row.cell("%.2f" % bilancio.importiDaVersare[unita_immobiliare.codice])

                    i = 0
                    for rata in bilancio.ratePreventivate[unita_immobiliare.codice]:
                        unita_row.cell("%.2f" % rata)
                        totale_rate[i] += rata
                        i += 1

                pdf.set_font("helvetica", "I", 7)
                totale_row = table.row()

                for tabella in tabelle_millesimali_immobile:
                    totale_row.cell("%.2f" % sum(list(tabella.millesimi.values())))

                pdf.set_font("helvetica", "BI", 8)
                totale_row.cell("TOTALE")

                pdf.set_font("helvetica", "I", 7)

                for tabella in tabelle_millesimali_immobile:
                    totale_row.cell("%.2f" % sum(list(bilancio.ripartizioneSpesePreventivate[tabella.codice].values())))

                totale_row.cell("%.2f" % totale_preventivo)
                totale_row.cell("%.2f" % sum(list(bilancio.ripartizioneConguaglio.values())))
                totale_row.cell("%.2f" % sum(list(bilancio.importiDaVersare.values())))

                for i in range(bilancio.numeroRate):
                    totale_row.cell("%.2f" % totale_rate[i])

        pdf = FPDF()
        bilancio = Bilancio.ricercaBilancioByCodice(bilancio.codice)
        pdf.add_page()
        printSpesePreventivate(pdf, bilancio)

        pdf.add_page()
        printSpeseConsuntivate(pdf, bilancio)

        pdf.add_page("L")
        printRipartizioneConsuntivo(pdf, bilancio)

        pdf.add_page("L")
        printRipartizionePreventivo(pdf, bilancio)

        return pdf
