import random
import tkinter as tk
from tkinter import messagebox

# --- 1. LOGIQUE DU JEU ---
# On crée le paquet de cartes (Bûches = 10 pts, As = 1 ou 11) [cite: 9]
paquet_base = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4

def calculer_score(main):
    score = 0
    as_possede = 0
    for carte in main:
        if carte in ["J", "Q", "K"]: score += 10 # Les bûches valent 10 [cite: 9]
        elif carte == "A":
            score += 11 # L'As vaut 11 par défaut [cite: 9]
            as_possede += 1
        else: score += int(carte)
    
    # Si on dépasse 21, l'As passe de 11 à 1 point [cite: 9]
    while score > 21 and as_possede > 0:
        score -= 10
        as_possede -= 1
    return score

# --- 2. ACTIONS DU JEU ---
def piocher_joueur():
    main_joueur.append(paquet.pop()) # Le joueur tire ("Hit") [cite: 22]
    update_interface()
    if calculer_score(main_joueur) > 21: # Si le joueur "brûle" [cite: 6]
        fin_de_partie("Dommage ! Vous avez dépassé 21.")

def rester_joueur():
    # Le croupier joue selon la règle : tire à 16, reste à 17 [cite: 30, 31]
    while calculer_score(main_croupier) < 17:
        main_croupier.append(paquet.pop())
    
    # Comparaison des scores pour déterminer le vainqueur [cite: 6]
    s_j = calculer_score(main_joueur)
    s_c = calculer_score(main_croupier)
    
    if s_c > 21: fin_de_partie("Gagné ! Le croupier a dépassé 21.")
    elif s_j > s_c: fin_de_partie(f"Gagné ! {s_j} contre {s_c}")
    elif s_j < s_c: fin_de_partie(f"Perdu ! Le croupier a {s_c}")
    else: fin_de_partie("Égalité !")

# --- 3. INTERFACE GRAPHIQUE ---
def update_interface():
    # On affiche les cartes sous forme de texte simple
    label_joueur.config(text=f"Vos cartes : {main_joueur}\nScore : {calculer_score(main_joueur)}")
    label_croupier.config(text=f"Croupier : {main_croupier[0]}, ?")

def nouvelle_partie():
    global paquet, main_joueur, main_croupier
    paquet = list(paquet_base)
    random.shuffle(paquet)
    # Distribution initiale : 2 cartes chacun [cite: 13, 14, 15]
    main_joueur = [paquet.pop(), paquet.pop()]
    main_croupier = [paquet.pop(), paquet.pop()]
    btn_hit.config(state="normal")
    btn_stand.config(state="normal")
    update_interface()

def fin_de_partie(message):
    btn_hit.config(state="disabled")
    btn_stand.config(state="disabled")
    label_croupier.config(text=f"Croupier : {main_croupier}\nScore : {calculer_score(main_croupier)}")
    messagebox.showinfo("Résultat", message)

# Fenêtre principale
root = tk.Tk()
root.title("Blackjack Simplifié")
root.geometry("400x400")
root.configure(bg="#2E8B57") # Vert tapis 

# Zones de texte
label_croupier = tk.Label(root, text="", font=("Arial", 14), bg="#2E8B57", fg="white")
label_croupier.pack(pady=30)

label_joueur = tk.Label(root, text="", font=("Arial", 14), bg="#2E8B57", fg="white")
label_joueur.pack(pady=30)

# Boutons
btn_hit = tk.Button(root, text="Tirer (Hit)", command=piocher_joueur, width=15)
btn_hit.pack(pady=5)

btn_stand = tk.Button(root, text="Rester (Stand)", command=rester_joueur, width=15)
btn_stand.pack(pady=5)

btn_rejouer = tk.Button(root, text="Nouvelle Partie", command=nouvelle_partie, width=15)
btn_rejouer.pack(pady=20)

nouvelle_partie()
root.mainloop()