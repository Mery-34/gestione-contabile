import csv
import os
from datetime import datetime
from tabulate import tabulate

FILE_DATI = "dati_contabili.csv"

def inizializza_file():
    if not os.path.exists(FILE_DATI):
        with open(FILE_DATI, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["data", "tipo", "importo", "causale"])

def inserisci_operazione():
    print("="*40)
    print(" GESTIONE CONTABILE PERSONALE ".center(40, "="))
    print("="*40)
    print("\nInserisci i dati (lascia vuoto se non vuoi compilare una sezione):\n")

    # Entrata
    entrata = input("ENTRATE\nImporto entrata (€):  ").strip()
    causale_entrata = input("Causale entrata:        ").strip()

    # Uscita
    uscita = input("\nUSCITE\nImporto uscita (€):   ").strip()
    causale_uscita = input("Causale uscita:         ").strip()

    # Data
    data_input = input("\nData (gg/mm/aaaa) [Invio per oggi]: ").strip()
    if data_input == "":
        data = datetime.today()
    else:
        try:
            data = datetime.strptime(data_input, "%d/%m/%Y")
        except ValueError:
            print("⚠️  Formato data non valido. Uso la data di oggi.")
            data = datetime.today()

    # Salvataggio
    with open(FILE_DATI, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if entrata:
            try:
                imp = float(entrata.replace(",", "."))
                writer.writerow([data.strftime("%d/%m/%Y"), "Entrata", f"{imp:.2f}", causale_entrata])
            except ValueError:
                print("⚠️  Importo entrata non valido. Scartato.")
        if uscita:
            try:
                imp = float(uscita.replace(",", "."))
                writer.writerow([data.strftime("%d/%m/%Y"), "Uscita", f"{imp:.2f}", causale_uscita])
            except ValueError:
                print("⚠️  Importo uscita non valido. Scartato.")

    print("\nOperazioni salvate!")

def mostra_resoconto_mensile():
    oggi = datetime.today()
    mese_corrente = oggi.strftime("%m")
    anno_corrente = oggi.strftime("%Y")

    entrate = 0
    uscite = 0
    righe = []

    if not os.path.exists(FILE_DATI):
        print("\nNessun dato disponibile.")
        return

    with open(FILE_DATI, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for riga in reader:
            data = datetime.strptime(riga["data"], "%d/%m/%Y")
            if data.strftime("%m") == mese_corrente and data.strftime("%Y") == anno_corrente:
                imp = float(riga["importo"])
                if riga["tipo"] == "Entrata":
                    entrate += imp
                elif riga["tipo"] == "Uscita":
                    uscite += imp
                righe.append([
                    riga["data"],
                    riga["tipo"],
                    f"{imp:.2f} €",
                    riga["causale"]
                ])

    saldo = entrate - uscite
    mese_nome = oggi.strftime("%B").capitalize()

    print("\n" + "="*40)
    print(f" RESOCONTO DI {mese_nome.upper()} {anno_corrente} ".center(40, "="))
    print("="*40)
    print(f"Totale entrate:  {entrate:.2f} €")
    print(f"Totale uscite:   {uscite:.2f} €")
    print(f"Saldo:           {saldo:.2f} €\n")

    if righe:
        print(tabulate(righe, headers=["Data", "Tipo", "Importo", "Causale"], tablefmt="grid"))
    else:
        print("Nessuna operazione registrata per questo mese.")

def mostra_resoconto_annuale():
    oggi = datetime.today()
    anno_corrente = oggi.strftime("%Y")

    entrate = 0
    uscite = 0
    righe = []

    if not os.path.exists(FILE_DATI):
        print("\nNessun dato disponibile.")
        return

    with open(FILE_DATI, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for riga in reader:
            data = datetime.strptime(riga["data"], "%d/%m/%Y")
            if data.strftime("%Y") == anno_corrente:
                imp = float(riga["importo"])
                if riga["tipo"] == "Entrata":
                    entrate += imp
                elif riga["tipo"] == "Uscita":
                    uscite += imp
                righe.append([
                    riga["data"],
                    riga["tipo"],
                    f"{imp:.2f} €",
                    riga["causale"]
                ])

    saldo = entrate - uscite

    print("\n" + "="*40)
    print(f" RESOCONTO ANNUALE {anno_corrente} ".center(40, "="))
    print("="*40)
    print(f"Totale entrate:  {entrate:.2f} €")
    print(f"Totale uscite:   {uscite:.2f} €")
    print(f"Saldo:           {saldo:.2f} €\n")

    if righe:
        print(tabulate(righe, headers=["Data", "Tipo", "Importo", "Causale"], tablefmt="grid"))
    else:
        print("Nessuna operazione registrata per questo anno.")

def main():
    inizializza_file()
    inserisci_operazione()
    mostra_resoconto_mensile()
    mostra_resoconto_annuale()

if __name__ == "__main__":
    main()

