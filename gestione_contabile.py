import traceback

try:
    from datetime import datetime
    import os
    from tabulate import tabulate
    import csv
    from collections import defaultdict

    FILE_DATI = os.path.join(os.path.expanduser("~"), "gestione_contabile.csv")

    # Se il file non esiste, crealo con intestazione
    if not os.path.exists(FILE_DATI):
        with open(FILE_DATI, mode="w", newline="", encoding="utf-8") as file:
            file.write("Data,Entrata,Uscita,Causale\n")

    data_corrente = datetime.now().strftime("%Y-%m-%d")

    # INSERIMENTO DATI
    entrata = input("ENTRATE\nImporto entrata (€):  ").strip()
    uscita = input("USCITE\nImporto uscita (€):  ").strip()
    causale = input("Causale:  ").strip()

    with open(FILE_DATI, mode="a", newline="", encoding="utf-8") as file:
        file.write(f"{data_corrente},{entrata},{uscita},{causale}\n")

    # CALCOLO RESOCONTI
    totali_mensili = defaultdict(lambda: [0.0, 0.0])  # [entrate, uscite]
    anno_corrente = datetime.now().year

    with open(FILE_DATI, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for riga in reader:
            data = riga["Data"]
            if not data.startswith(str(anno_corrente)):
                continue
            mese = data[:7]
            e = float(riga["Entrata"]) if riga["Entrata"] else 0.0
            u = float(riga["Uscita"]) if riga["Uscita"] else 0.0
            totali_mensili[mese][0] += e
            totali_mensili[mese][1] += u

    print("\nRESOCONTO MENSILE:")
    tabella = []
    for mese, valori in sorted(totali_mensili.items()):
        tabella.append([mese, f"{valori[0]:.2f} €", f"{valori[1]:.2f} €"])
    print(tabulate(tabella, headers=["Mese", "Entrate", "Uscite"], tablefmt="grid"))

    print("\nRESOCONTO ANNUALE:")
    entrate_tot = sum(v[0] for v in totali_mensili.values())
    uscite_tot = sum(v[1] for v in totali_mensili.values())
    print(tabulate([["Totale", f"{entrate_tot:.2f} €", f"{uscite_tot:.2f} €"]],
                   headers=["Anno", "Entrate", "Uscite"], tablefmt="grid"))

except Exception:
    with open("errore_log.txt", "w", encoding="utf-8") as log:
        log.write(traceback.format_exc())
