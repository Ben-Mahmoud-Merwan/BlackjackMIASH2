import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# --- DÉCLARATION DES VARIABLES GLOBALES (Pour éviter les erreurs Mypy) ---
dict_images = {}
img_dos = None
btn_imgs = {}
paquet = []
main_joueur = []
main_croupier = []

# --- 1. LOGIQUE DE JEU ---
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

# --- 2. CHARGEMENT DES IMAGES ---
def charger_ressources():
    global dict_images, img_dos, btn_imgs
    
    try:
        img_brute = Image.open("cartes.png")
        img_b = Image.open("button d'action.png")
    except FileNotFoundError:
        print("Erreur : Les fichiers images sont introuvables !")
        return

    h_unitaire = img_brute.height // 53
    taille_affichage = (100, 150)
    
    img_dos = ImageTk.PhotoImage(img_brute.crop((0, 0, 110, 170)).resize(taille_affichage))
    
    noms = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    for i, nom in enumerate(noms):
        y = i * h_unitaire + 170
        coupe = img_brute.crop((0, y, img_brute.width, y + h_unitaire))
        dict_images[nom] = ImageTk.PhotoImage(coupe.resize(taille_affichage))

    btn_imgs["deal"] = ImageTk.PhotoImage(img_b.crop((0, 0, 70, 70)))
    btn_imgs["hit"] = ImageTk.PhotoImage(img_b.crop((280, 0, 350, 70)))
    btn_imgs["stand"] = ImageTk.PhotoImage(img_b.crop((350, 0, 420, 70)))

# --- 3. FONCTIONS DE L'INTERFACE ---
def rafraichir_ecran(final=False):
    canvas.delete("all")
    for i, carte in enumerate(main_joueur):
        canvas.create_image(50 + i*110, 300, image=dict_images[carte], anchor="nw")
    for i, carte in enumerate(main_croupier):
        img = dict_images[carte] if (i == 0 or final) else img_dos
        canvas.create_image(50 + i*110, 50, image=img, anchor="nw")
    canvas.create_text(50, 470, text=f"Votre score: {calculer_score(main_joueur)}", fill="white", anchor="w", font=("Arial", 16, "bold"))

def jouer_hit():
    main_joueur.append(paquet.pop())
    rafraichir_ecran()
    if calculer_score(main_joueur) > 21:
        messagebox.showinfo("Résultat", "Vous avez brûlé !")
        relancer()

def jouer_stand():
    while calculer_score(main_croupier) < 17:
        main_croupier.append(paquet.pop())
    rafraichir_ecran(final=True)
    messagebox.showinfo("Résultat", "Fin de manche")
    relancer()

def relancer():
    global paquet, main_joueur, main_croupier
    paquet = list(paquet_base)
    random.shuffle(paquet)
    main_joueur = [paquet.pop(), paquet.pop()]
    main_croupier = [paquet.pop(), paquet.pop()]
    rafraichir_ecran()

# --- 4. LANCEMENT ---
root = tk.Tk()
root.title("Blackjack Final")
root.geometry("600x620")

charger_ressources() # On charge les images avant de créer les boutons

canvas = tk.Canvas(root, bg="#2E8B57", width=600, height=500)
canvas.pack()

cadre_boutons = tk.Frame(root)
cadre_boutons.pack(pady=10)

# On utilise les clés du dictionnaire btn_imgs
tk.Button(cadre_boutons, image=btn_imgs["deal"], command=relancer, borderwidth=0).grid(row=0, column=0, padx=10)
tk.Button(cadre_boutons, image=btn_imgs["hit"], command=jouer_hit, borderwidth=0).grid(row=0, column=1, padx=10)
tk.Button(cadre_boutons, image=btn_imgs["stand"], command=jouer_stand, borderwidth=0).grid(row=0, column=2, padx=10)

relancer()
root.mainloop()