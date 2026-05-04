import random
import tkinter as tk
from PIL import Image, ImageTk
 
# -CODE DE BASE -
paquet_base = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4
 
def calculer_score(main):
    score = 0
    as_possede = 0
    for carte in main:
        if carte in ["J", "Q", "K"]: score += 10
        elif carte == "A":
            score += 11
            as_possede += 1
        else: score += int(carte)
    while score > 21 and as_possede > 0:
        score -= 10
        as_possede -= 1
    return score
 
 
# -INTERFACE GRAPHIQUE-
 
def charger_images():
    global img_cartes, img_bouton_hit, img_bouton_stand, img_bouton_deal, img_dos_carte
 
    # 1. Boutons bleus 
    image_boutons = Image.open("button d'action.png")
    img_bouton_deal  = ImageTk.PhotoImage(image_boutons.crop((  0, 0,  70, 70)))
    img_bouton_hit   = ImageTk.PhotoImage(image_boutons.crop((280, 0, 350, 70)))
    img_bouton_stand = ImageTk.PhotoImage(image_boutons.crop((350, 0, 420, 70)))
 
    # 2. Cartes 
    image = Image.open("cartes.png")
 
    carte_hauteur = image.height // 53
    TAILLE = (143, 221)
 
    img_dos_carte = ImageTk.PhotoImage(
        image.crop((0, 0, 110, 170)).resize(TAILLE, Image.Resampling.LANCZOS))
 
    rangs = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    img_cartes = {}
    for i, valeur in enumerate(rangs):
        y1 = i * carte_hauteur + 170
        y2 = y1 + carte_hauteur
        img_cartes[valeur] = ImageTk.PhotoImage(
            image.crop((0, y1, image.width, y2)).resize(TAILLE, Image.Resampling.LANCZOS))
 
 
def actualiser_affichage(fin_partie=False):
    canvas.update_idletasks()
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    if W < 50 or H < 50:
        racine.after(50, lambda: actualiser_affichage(fin_partie))
        return
 
    canvas.delete("all")
 
    score_j = calculer_score(main_joueur)
    score_c = calculer_score(main_croupier)
 
    # Score joueur — bas gauche
    canvas.create_text(120, H - 30,
                       text=f"Votre Score : {score_j}",
                       font=("Helvetica", 20, "bold"), fill="white")
 
    # Score croupier — haut droite
    if fin_partie:
        canvas.create_text(W - 120, 30,
                           text=f"Score Croupier : {score_c}",
                           font=("Helvetica", 20, "bold"), fill="white")
    else:
        valeur_visible = calculer_score([main_croupier[0]])
        canvas.create_text(W - 120, 30,
                           text=f"Score Croupier : {valeur_visible} + ?",
                           font=("Helvetica", 20, "bold"), fill="white")
 
    ESPACEMENT = 153
 
    # Cartes du croupier — rangée haute
    nb_c = len(main_croupier)
    offset_c = W // 2 - (nb_c * ESPACEMENT) // 2
    for index, carte in enumerate(main_croupier):
        px = offset_c + index * ESPACEMENT + 71
        if index == 1 and not fin_partie:
            canvas.create_image(px, H // 4, image=img_dos_carte)
        else:
            canvas.create_image(px, H // 4, image=img_cartes[carte])
 
    # Cartes du joueur — rangée basse
    nb_j = len(main_joueur)
    offset_j = W // 2 - (nb_j * ESPACEMENT) // 2
    for index, carte in enumerate(main_joueur):
        px = offset_j + index * ESPACEMENT + 71
        canvas.create_image(px, 3 * H // 4 - 20, image=img_cartes[carte])
 
 
def gerer_fin_de_partie():
    canvas.update_idletasks()
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    cx, cy = W // 2, H // 2
 
    score_j = calculer_score(main_joueur)
    score_c = calculer_score(main_croupier)
 
    FONT = ("Helvetica", 90, "bold")
    if score_j > 21: 
        canvas.create_text(cx, cy, text="LOSER",  font=FONT, fill="red")
    elif score_c > 21 or score_j > score_c:
        canvas.create_text(cx, cy, text="WINNER", font=FONT, fill="yellow")
    elif score_c <= 21 and score_j < score_c:
        canvas.create_text(cx, cy, text="LOSER",  font=FONT, fill="red")
    else:
        canvas.create_text(cx, cy, text="DRAW",   font=FONT, fill="gray")
 
    bouton_hit.config(state="disabled")
    bouton_stand.config(state="disabled")
 
 
def action_hit():
    main_joueur.append(paquet.pop())
    if calculer_score(main_joueur) >= 21:
        actualiser_affichage(fin_partie=True)
        gerer_fin_de_partie()
    else:
        actualiser_affichage(fin_partie=False)
 
 
def action_stand():
    while calculer_score(main_croupier) < 17:
        main_croupier.append(paquet.pop())
    actualiser_affichage(fin_partie=True)
    gerer_fin_de_partie()
 
 
def nouvelle_partie():
    global paquet, main_joueur, main_croupier
    bouton_hit.config(state="normal")
    bouton_stand.config(state="normal")
    paquet = list(paquet_base)
    random.shuffle(paquet)
    main_joueur   = [paquet.pop(), paquet.pop()]
    main_croupier = [paquet.pop(), paquet.pop()]
    actualiser_affichage(fin_partie=False)
 
 
# ── CRÉATION DE L'INTERFACE ────────────────────────────────────────────────────
racine = tk.Tk()
racine.title("Blackjack Python")
 
try:
    racine.state('zoomed')
except Exception:
    racine.attributes('-zoomed', True)
 
racine.grid_rowconfigure(0, weight=1)
racine.grid_rowconfigure(1, weight=0)
racine.grid_columnconfigure(0, weight=1)
racine.grid_columnconfigure(1, weight=0)
 
canvas = tk.Canvas(racine, bg="#2E8B57")
canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")
 
charger_images()
 
frame_boutons = tk.Frame(racine)
frame_boutons.grid(row=1, column=1, sticky="e", pady=10, padx=20)
 
bouton_deal  = tk.Button(frame_boutons, image=img_bouton_deal,  command=nouvelle_partie, borderwidth=0)
bouton_deal.grid(row=0, column=0, padx=5)
 
bouton_hit   = tk.Button(frame_boutons, image=img_bouton_hit,   command=action_hit,      borderwidth=0)
bouton_hit.grid(row=0, column=1, padx=5)
 
bouton_stand = tk.Button(frame_boutons, image=img_bouton_stand, command=action_stand,    borderwidth=0)
bouton_stand.grid(row=0, column=2, padx=5)
 
racine.after(150, nouvelle_partie)
racine.mainloop()
 