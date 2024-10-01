import os
import subprocess

class GestorePDF:

    def creaPDF(self, nomefile):
        pass

    def visualizzaPDF(self, nomefile):#ricerca il pdf e lo apre a schermo con il visualizzatore pdf predefinito del pc
        directory = 'Dati/'+nomefile

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".pdf") and nomefile.lower in file.lower():
                    file_path = os.path.join(root, file)
                    subprocess.Popen(["xdg-open", file_path])
                    return

        return "PDF non trovato"

    def visualizzaListaPDF(self):
        file_pdf = [file for file in os.listdir('../Dati') if file.lower().endswith(".pdf")]

        if not file_pdf:
            print("Non ci sono File nella Directory")
            return

        file_pdf.sort()  #ordina in oldine alfabetico la lista dei PDF
