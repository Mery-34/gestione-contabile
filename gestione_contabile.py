import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv
import os

FILE_DATI = os.path.join(os.path.expanduser("~"), "gestione_contabile.csv")

def inizializza_file():
    if not os.path.exists(FILE_DATI):
        with open(FILE_DATI, mode="w", newline="", encoding="utf-8") as file:
            file.write("Data,Entrata,Uscita,Causale\n")

def carica_dati():
    entrate, uscite = [], []
    tot_mese_e, tot_mese_u = 0, 0
    tot_anno_e, tot_anno_u = 0, 0
    filtro = filtro_var.get()
    oggi = datetime.now()

    if not os.path.exists(FILE_DATI):
        return entrate, uscite, (0, 0), (0, 0)

    with open(FILE_DATI, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = row["Data"]
            e = float(row["Entrata"]) if row["Entrata"] else 0
            u = float(row["Uscita"]) if row["Uscita"] else 0
            causale = row["Causale"]

            if filtro == "Giorno" and data == oggi.strftime("%Y-%m-%d"):
                if e: entrate.append((data, e, causale))
                if u: uscite.append((data, u, causale))
            if filtro == "Mese" and data[:7] == oggi.strftime("%Y-%m"):
                if e:
                    entrate.append((data, e, causale))
                    tot_mese_e += e
                if u:
                    uscite.append((data, u, causale))
                    tot_mese_u += u
            if filtro == "Anno" and data[:4] == oggi.strftime("%Y"):
                if e: tot_anno_e += e
                if u: tot_anno_u += u

    return entrate, uscite, (tot_mese_e, tot_mese_u), (tot_anno_e, tot_anno_u)

def aggiorna_tabelle():
    entrate, uscite, tot_mese, tot_anno = carica_dati()

    tab_entrate.delete(*tab_entrate.get_children())
    tab_uscite.delete(*tab_uscite.get_children())

    for data, val, causale in entrate:
        tab_entrate.insert("", "end", values=(val, causale, data))
    for data, val, causale in uscite:
        tab_uscite.insert("", "end", values=(val, causale, data))

    tab_res_mese.delete(*tab_res_mese.get_children())
    tab_res_mese.insert("", "end", values=("Entrate", f"{tot_mese[0]:.2f} €"))
    tab_res_mese.insert("", "end", values=("Uscite", f"{tot_mese[1]:.2f} €"))

    tab_res_anno.delete(*tab_res_anno.get_children())
    tab_res_anno.insert("", "end", values=("Entrate", f"{tot_anno[0]:.2f} €"))
    tab_res_anno.insert("", "end", values=("Uscite", f"{tot_anno[1]:.2f} €"))

def nuova_salva_dati():
    with open(FILE_DATI, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if entrata_importo.get().strip():
            writer.writerow([
                entrata_data.get(),
                entrata_importo.get().strip(),
                "",
                entrata_causale.get().strip()
            ])
            entrata_importo.set("")
            entrata_causale.set("")
            entrata_data.set(datetime.now().strftime("%Y-%m-%d"))

        if uscita_importo.get().strip():
            writer.writerow([
                uscita_data.get(),
                "",
                uscita_importo.get().strip(),
                uscita_causale.get().strip()
            ])
            uscita_importo.set("")
            uscita_causale.set("")
            uscita_data.set(datetime.now().strftime("%Y-%m-%d"))

    aggiorna_tabelle()

# --- Interfaccia ---
inizializza_file()
root = tk.Tk()
root.title("Gestione Contabile")
root.geometry("900x800")
root.configure(bg="white")

font_label = ("Arial", 12, "bold")
font_entry = ("Arial", 12)

# --- SEZIONE 1: Inserimento Dati ---
frame_input = tk.LabelFrame(root, text="Inserimento Dati", bg="white", font=font_label, padx=10, pady=10)
frame_input.pack(padx=20, pady=10, fill="x")

frame_entrata = tk.Frame(frame_input, bg="white")
frame_uscita = tk.Frame(frame_input, bg="white")

entrata_importo = tk.StringVar()
entrata_causale = tk.StringVar()
entrata_data = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

uscita_importo = tk.StringVar()
uscita_causale = tk.StringVar()
uscita_data = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

tk.Label(frame_entrata, text="Entrata (€):", bg="white", font=font_label).grid(row=0, column=0, sticky="e", pady=5)
tk.Entry(frame_entrata, textvariable=entrata_importo, font=font_entry).grid(row=0, column=1)

tk.Label(frame_entrata, text="Causale:", bg="white", font=font_label).grid(row=1, column=0, sticky="e", pady=5)
tk.Entry(frame_entrata, textvariable=entrata_causale, font=font_entry).grid(row=1, column=1)

tk.Label(frame_entrata, text="Data:", bg="white", font=font_label).grid(row=2, column=0, sticky="e", pady=5)
tk.Entry(frame_entrata, textvariable=entrata_data, font=font_entry).grid(row=2, column=1)

tk.Label(frame_uscita, text="Uscita (€):", bg="white", font=font_label).grid(row=0, column=0, sticky="e", pady=5)
tk.Entry(frame_uscita, textvariable=uscita_importo, font=font_entry).grid(row=0, column=1)

tk.Label(frame_uscita, text="Causale:", bg="white", font=font_label).grid(row=1, column=0, sticky="e", pady=5)
tk.Entry(frame_uscita, textvariable=uscita_causale, font=font_entry).grid(row=1, column=1)

tk.Label(frame_uscita, text="Data:", bg="white", font=font_label).grid(row=2, column=0, sticky="e", pady=5)
tk.Entry(frame_uscita, textvariable=uscita_data, font=font_entry).grid(row=2, column=1)

frame_entrata.pack(side="left", padx=40)
frame_uscita.pack(side="left", padx=40)

tk.Button(frame_input, text="Aggiungi Movimento", bg="#a8e6a1", font=font_label, command=nuova_salva_dati).pack(pady=10)

# --- SEZIONE 2: Filtro ---
frame_filtro = tk.LabelFrame(root, text="Filtro Visualizzazione", bg="white", font=font_label, padx=10, pady=10)
frame_filtro.pack(padx=20, pady=10, fill="x")

filtro_var = tk.StringVar(value="Mese")
tk.Label(frame_filtro, text="Visualizza per:", bg="white", font=font_label).pack(side="left", padx=5)
ttk.Combobox(frame_filtro, textvariable=filtro_var, values=["Giorno", "Mese", "Anno"], font=font_entry, width=10).pack(side="left")
tk.Button(frame_filtro, text="Visualizza", bg="#add8e6", font=font_label, command=aggiorna_tabelle).pack(side="left", padx=10)

# --- SEZIONE 3: Tabelle Entrate/Uscite ---
frame_tabelle = tk.Frame(root, bg="white")
frame_tabelle.pack(padx=20, pady=10, fill="both", expand=True)

tk.Label(frame_tabelle, text="Entrate", bg="white", font=font_label).pack()
tab_entrate = ttk.Treeview(frame_tabelle, columns=("Importo", "Causale", "Data"), show="headings", height=6)
for col in ("Importo", "Causale", "Data"):
    tab_entrate.heading(col, text=col)
    tab_entrate.column(col, anchor="center", width=200)
tab_entrate.pack(pady=5, fill="x")

tk.Label(frame_tabelle, text="Uscite", bg="white", font=font_label).pack(pady=(20, 0))
tab_uscite = ttk.Treeview(frame_tabelle, columns=("Importo", "Causale", "Data"), show="headings", height=6)
for col in ("Importo", "Causale", "Data"):
    tab_uscite.heading(col, text=col)
    tab_uscite.column(col, anchor="center", width=200)
tab_uscite.pack(pady=5, fill="x")

# --- SEZIONE 4: Tabelle Resoconto Mensile e Annuale ---
frame_resoconti = tk.Frame(root, bg="white")
frame_resoconti.pack(padx=20, pady=10, fill="x")

tk.Label(frame_resoconti, text="Resoconto Mensile", bg="white", font=font_label).pack()
tab_res_mese = ttk.Treeview(frame_resoconti, columns=("Tipo", "Totale €"), show="headings", height=2)
tab_res_mese.heading("Tipo", text="Tipo")
tab_res_mese.heading("Totale €", text="Totale €")
tab_res_mese.column("Tipo", anchor="center", width=200)
tab_res_mese.column("Totale €", anchor="center", width=200)
tab_res_mese.pack(pady=5)

tk.Label(frame_resoconti, text="Resoconto Annuale", bg="white", font=font_label).pack(pady=(20, 0))
tab_res_anno = ttk.Treeview(frame_resoconti, columns=("Tipo", "Totale €"), show="headings", height=2)
tab_res_anno.heading("Tipo", text="Tipo")
tab_res_anno.heading("Totale €", text="Totale €")
tab_res_anno.column("Tipo", anchor="center", width=200)
tab_res_anno.column("Totale €", anchor="center", width=200)
tab_res_anno.pack(pady=5)

aggiorna_tabelle()
root.mainloop()
