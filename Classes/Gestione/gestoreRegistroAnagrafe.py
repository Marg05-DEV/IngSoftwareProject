import os
import pickle

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile

from fpdf import FPDF

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
        for item in list_unitaImmobiliari:
            proprietario_cf = [key for key, value in item.condomini.items() if value == 'Proprietario']
            print(proprietario_cf)
            if len(proprietario_cf) < 1:
                if len(item.condomini < 1):
                    senza_condomini.append(item.codice)
                else:
                    senza_proprietario.append(item.codice)

            proprietario = Condomino.ricercaCondominoByCF(proprietario_cf[0])
            proprietari_unita_immobiliari.append([item.codice, proprietario.cognome, proprietario.nome])
        GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByScala(senza_proprietario)
        GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByScala(senza_condomini)
        proprietari_unita_immobiliari.sort(key=lambda row: row[2])
        proprietari_unita_immobiliari.sort(key=lambda row: row[1])
        print(senza_proprietario)
        print(senza_condomini)
        print(proprietari_unita_immobiliari)
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
    def generaPDFRegistroAnagrafeCondominiale(self):
        pdf = FPDF()

