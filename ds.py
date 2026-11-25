import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

root = tk.Tk()
root.title("ParkVision Pro")
root.geometry("1280x720")
root.configure(bg="#0F172A")

cap = 50
presents = 18
in_cnt = 42
out_cnt = 24

rows = [
    ("123 تونس 4567", "08:15:25", "10:30:17", "Terminé"),
    ("456 تونس 7890", "09:00:12", "-", "En cours"),
    ("789 تونس 0123", "09:20:45", "09:55:30", "Terminé"),
    ("321 تونس 6543", "09:45:10", "-", "En cours"),
]

# Barre du haut
top = tk.Frame(root, bg="#1E293B", height=55)
top.pack(fill="x")
tk.Label(top, text="PARKVISION PRO", bg="#1E293B", fg="#3B82F6", font=("Arial", 14, "bold")).pack(side="left", padx=20, pady=12)
clk = tk.Label(top, text="", bg="#1E293B", fg="#F8FAFC", font=("Consolas", 11))
clk.pack(side="right", padx=20)

# Conteneur 3 colonnes
main = tk.Frame(root, bg="#0F172A")
main.pack(fill="both", expand=True, padx=15, pady=15)
main.columnconfigure(0, weight=2)
main.columnconfigure(1, weight=4)
main.columnconfigure(2, weight=4)
main.rowconfigure(0, weight=1)

# Colonne 1 : KPI + Contrôles
c1 = tk.Frame(main, bg="#1E293B", padx=14, pady=14)
c1.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

lbl_free = tk.Label(c1, text="", bg="#1E293B", fg="#10B981", font=("Arial", 18, "bold"))
lbl_free.pack(anchor="w")

prog = ttk.Progressbar(c1, maximum=cap, value=presents)
prog.pack(fill="x", pady=8)

lbl_io = tk.Label(c1, text="", bg="#1E293B", fg="#94A3B8", font=("Arial", 10, "bold"))
lbl_io.pack(anchor="w", pady=(0, 15))

tk.Label(c1, text="Plaque :", bg="#1E293B", fg="#F8FAFC", font=("Arial", 10)).pack(anchor="w")
plate_var = tk.StringVar(value="123 تونس 4567")
tk.Entry(c1, textvariable=plate_var, bg="#334155", fg="white", font=("Arial", 13, "bold"), justify="center").pack(fill="x", ipady=6, pady=(4, 10))

def refresh_kpi():
    lbl_free.config(text=str(cap - presents) + " places libres")
    prog["value"] = presents
    lbl_io.config(text="Entrées: " + str(in_cnt) + "  |  Sorties: " + str(out_cnt))

def refresh_tree(data):
    for i in tree.get_children():
        tree.delete(i)
    for r in data:
        tree.insert("", "end", values=r)

def scan():
    plate_var.set(str(random.randint(100, 245)) + " تونس " + str(random.randint(1000, 9999)))

def do_in():
    global presents, in_cnt
    p = plate_var.get().strip()
    if not p:
        return
    h = datetime.now().strftime("%H:%M:%S")
    rows.insert(0, (p, h, "-", "En cours"))
    presents += 1
    in_cnt += 1
    refresh_tree(rows)
    refresh_kpi()

def do_out():
    global presents, out_cnt
    p = plate_var.get().strip()
    if not p:
        return
    h = datetime.now().strftime("%H:%M:%S")
    done = False
    for idx, r in enumerate(rows):
        if r[0] == p and r[3] == "En cours":
            rows[idx] = (r[0], r[1], h, "Terminé")
            done = True
            break
    if not done:
        rows.insert(0, (p, "-", h, "Terminé"))
    if presents > 0:
        presents -= 1
    out_cnt += 1
    refresh_tree(rows)
    refresh_kpi()

tk.Button(c1, text="Scanner Plaque", bg="#3B82F6", fg="white", font=("Arial", 10, "bold"), command=scan).pack(fill="x", pady=(0, 12))
tk.Button(c1, text="ENTREE", bg="#10B981", fg="white", font=("Arial", 10, "bold"), command=do_in).pack(fill="x", pady=(0, 6))
tk.Button(c1, text="SORTIE", bg="#EF4444", fg="white", font=("Arial", 10, "bold"), command=do_out).pack(fill="x")
tk.Button(c1, text="Ouvrir Barrière", bg="#334155", fg="#F59E0B", font=("Arial", 9, "bold"), command=lambda: messagebox.showinfo("Barrière", "Barrière ouverte")).pack(fill="x", pady=(16, 0))

# Colonne 2 : 2 Caméras
c2 = tk.Frame(main, bg="#0F172A")
c2.grid(row=0, column=1, sticky="nsew", padx=4)
c2.rowconfigure(0, weight=1)
c2.rowconfigure(1, weight=1)
c2.columnconfigure(0, weight=1)

for idx, (title, col) in enumerate([("CAMERA ENTREE", "#10B981"), ("CAMERA SORTIE", "#3B82F6")]):
    box = tk.Frame(c2, bg="#1E293B", padx=10, pady=10)
    box.grid(row=idx, column=0, sticky="nsew", pady=(0, 4) if idx == 0 else (4, 0))
    tk.Label(box, text=title, bg="#1E293B", fg="#F8FAFC", font=("Arial", 10, "bold")).pack(anchor="w")
    cv = tk.Canvas(box, bg="#090D16", highlightthickness=1, highlightbackground="#334155")
    cv.pack(fill="both", expand=True, pady=(6, 0))
    cv.create_text(180, 90, text="Flux Vidéo (OpenCV / RTSP)", fill="#94A3B8", font=("Arial", 10))

# Colonne 3 : Historique
c3 = tk.Frame(main, bg="#1E293B", padx=12, pady=12)
c3.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
tk.Label(c3, text="HISTORIQUE", bg="#1E293B", fg="#F8FAFC", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 8))

search_var = tk.StringVar()
ent_s = tk.Entry(c3, textvariable=search_var, bg="#334155", fg="white", font=("Arial", 10))
ent_s.pack(fill="x", ipady=5, pady=(0, 8))

tree = ttk.Treeview(c3, columns=("p", "e", "s", "st"), show="headings", height=15)
for col_id, head_txt, w in [("p", "Plaque", 120), ("e", "Entrée", 75), ("s", "Sortie", 75), ("st", "Statut", 80)]:
    tree.heading(col_id, text=head_txt)
    tree.column(col_id, width=w, anchor="center")
tree.pack(fill="both", expand=True)

def filter_rows(event=None):
    q = search_var.get().lower()
    refresh_tree([r for r in rows if q in r[0].lower() or q in r[3].lower()])

ent_s.bind("<KeyRelease>", filter_rows)

def tick():
    clk.config(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    root.after(1000, tick)

refresh_kpi()
refresh_tree(rows)
tick()
root.mainloop()