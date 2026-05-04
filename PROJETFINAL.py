import random
import tkinter as tk
from PIL import Image, ImageTk
 

# Création d'une liste représentant les valeurs d'un jeu de 52 cartes (13 valeurs multipliées par 4 couleurs)
paquet_base = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4
 
# Fonction qui calcule le total des points d'une main (liste de cartes)
def calculer_score(main):
    score = 0
    as_possede = 0
    # On parcourt chaque carte de la main
    for carte in main:
        # Si c'est une figure (Valet, Dame, Roi), ça vaut 10 points
        if carte in ["J", "Q", "K"]: score += 10
        # Si c'est un As, on ajoute 11 par défaut et on retient qu'on a un As
        elif carte == "A":
            score += 11
            as_possede += 1
        # Sinon (cartes de 2 à 10), on convertit le texte en nombre entier et on l'ajoute
        else: score += int(carte)
    # Si le score dépasse 21 et qu'on a un As qui valait 11, on retire 10 (l'As vaut maintenant 1)
    while score > 21 and as_possede > 0:
        score -= 10
        as_possede -= 1
    return score
 
 

 
# Fonction pour découper et préparer toutes les images du jeu
def charger_images():
    # Déclaration des variables globales pour pouvoir les utiliser partout 
    global img_cartes, img_bouton_hit, img_bouton_stand, img_bouton_deal, img_dos_carte
 
    #  Préparation des boutons bleus
    # Ouverture de l'image contenant tous les boutons
    image_boutons = Image.open("button d'action.png")
    # Découpage du bouton "Deal" 
    img_bouton_deal  = ImageTk.PhotoImage(image_boutons.crop((  0, 0,  70, 70)))
    # Découpage du bouton "Hit"
    img_bouton_hit   = ImageTk.PhotoImage(image_boutons.crop((280, 0, 350, 70)))
    # Découpage du bouton "Stand"
    img_bouton_stand = ImageTk.PhotoImage(image_boutons.crop((350, 0, 420, 70)))
 
    # 2. Préparation des cartes
    # Ouverture de l'image contenant toutes les cartes
    image = Image.open("cartes.png")
 
    # Calcul de la hauteur d'une seule carte en fonction de l'image source
    carte_hauteur = image.height // 53
    # Taille finale souhaitée pour les cartes sur l'écran
    TAILLE = (143, 221)
 
    # Découpage de l'image du dos de la carte (première carte en haut à gauche de l'image source)
    img_dos_carte = ImageTk.PhotoImage(
        image.crop((0, 0, 110, 170)).resize(TAILLE, Image.Resampling.LANCZOS))
 
    # Liste des valeurs dans l'ordre de l'image source
    rangs = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    # Création d'un dictionnaire pour stocker l'image de chaque carte
    img_cartes = {}
    # Boucle pour découper l'image de chaque carte en descendant sur l'image source
    for i, valeur in enumerate(rangs):
        y1 = i * carte_hauteur + 170
        y2 = y1 + carte_hauteur
        # On découpe, on redimensionne et on stocke dans le dictionnaire avec la valeur comme clé
        img_cartes[valeur] = ImageTk.PhotoImage(
            image.crop((0, y1, image.width, y2)).resize(TAILLE, Image.Resampling.LANCZOS))
 
# Fonction pour redessiner le tapis de jeu (scores et cartes)
def actualiser_affichage(fin_partie=False):
    # Met à jour les dimensions de la fenêtre
    canvas.update_idletasks()
    W = canvas.winfo_width() # Largeur de l'écran
    H = canvas.winfo_height() # Hauteur de l'écran
    
    # Si la fenêtre est trop petite (au lancement), on relance la fonction un peu plus tard
    if W < 50 or H < 50:
        racine.after(50, lambda: actualiser_affichage(fin_partie))
        return
 
    # Efface tout ce qui est actuellement dessiné sur le tapis vert
    canvas.delete("all")
 
    # Calcule les scores actuels du joueur et du croupier
    score_j = calculer_score(main_joueur)
    score_c = calculer_score(main_croupier)
 
    # Dessine le texte du Score du joueur en bas à gauche
    canvas.create_text(120, H - 30,
                       text=f"Votre Score : {score_j}",
                       font=("Helvetica", 20, "bold"), fill="white")
 
    # Gestion de l'affichage du score du croupier
    if fin_partie:
        # Si la partie est finie, on affiche son score total en haut à droite
        canvas.create_text(W - 120, 30,
                           text=f"Score Croupier : {score_c}",
                           font=("Helvetica", 20, "bold"), fill="white")
    else:
        # Sinon, on ne calcule et n'affiche que la valeur de sa première carte (visible)
        valeur_visible = calculer_score([main_croupier[0]])
        canvas.create_text(W - 120, 30,
                           text=f"Score Croupier : {valeur_visible} + ?",
                           font=("Helvetica", 20, "bold"), fill="white")
 
    # Espace en pixels entre chaque carte posée
    ESPACEMENT = 153
 
    # Dessiner les cartes du croupier (rangée du haut)
    nb_c = len(main_croupier)
    # Calcul pour centrer les cartes horizontalement
    offset_c = W // 2 - (nb_c * ESPACEMENT) // 2
    for index, carte in enumerate(main_croupier):

        # Position X de la carte
        px = offset_c + index * ESPACEMENT + 71
        # Si la partie n'est pas finie, on cache la 2ème carte (index 1) avec le dos de carte
        if index == 1 and not fin_partie:
            canvas.create_image(px, H // 4, image=img_dos_carte)
        # Sinon on affiche la face de la carte
        else:
            canvas.create_image(px, H // 4, image=img_cartes[carte])
 
    # Dessiner les cartes du joueur (rangée du bas)
    nb_j = len(main_joueur)
    # Calcul pour centrer les cartes horizontalement
    offset_j = W // 2 - (nb_j * ESPACEMENT) // 2
    for index, carte in enumerate(main_joueur):
        px = offset_j + index * ESPACEMENT + 71
        # On dessine l'image de la carte du joueur
        canvas.create_image(px, 3 * H // 4 - 20, image=img_cartes[carte])
 
# Fonction disant qui a gagné à la fin du tour
def gerer_fin_de_partie():
    # Récupération des dimensions pour centrer le texte de victoire/défaite
    canvas.update_idletasks()
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    cx, cy = W // 2, H // 2
 
    # Calcul des scores finaux
    score_j = calculer_score(main_joueur)
    score_c = calculer_score(main_croupier)
 
    # Police d'écriture pour le grand message central
    FONT = ("Helvetica", 90, "bold")
    
    # Conditions de victoire/défaite :
    # Si le joueur dépasse 21, il perd
    if score_j > 21: 
        canvas.create_text(cx, cy, text="LOSER",  font=FONT, fill="red")
    # Si le croupier dépasse 21 OU que le joueur a un meilleur score, le joueur gagne
    elif score_c > 21 or score_j > score_c:
        canvas.create_text(cx, cy, text="WINNER", font=FONT, fill="yellow")
    # Si le croupier a 21 ou moins ET a un meilleur score que le joueur, le joueur perd
    elif score_c <= 21 and score_j < score_c:
        canvas.create_text(cx, cy, text="LOSER",  font=FONT, fill="red")
    # Sinon, c'est une égalité
    else:
        canvas.create_text(cx, cy, text="DRAW",   font=FONT, fill="gray")
 
    # On désactive les boutons Hit et Stand car la partie est finie
    bouton_hit.config(state="disabled")
    bouton_stand.config(state="disabled")
 
# Action déclenchée quand le joueur clique sur "Hit" (Tirer une carte)
def action_hit():
    # On retire une carte du paquet et on l'ajoute à la main du joueur
    main_joueur.append(paquet.pop())
    # Si le joueur atteint ou dépasse 21 après avoir tiré
    if calculer_score(main_joueur) >= 21:
        # On force la fin de partie (révèle les cartes, affiche résultat)
        actualiser_affichage(fin_partie=True)
        gerer_fin_de_partie()
    else:
        # Sinon on met juste l'affichage à jour
        actualiser_affichage(fin_partie=False)
 
# Action déclenchée quand le joueur clique sur "Stand" (S'arrêter)
def action_stand():
    # Tour du croupier : il tire obligatoirement tant que son score est strictement inférieur à 17
    while calculer_score(main_croupier) < 17:
        main_croupier.append(paquet.pop())
    # Le croupier a fini de tirer, on met à jour l'affichage en mode fin de partie (révèle tout)
    actualiser_affichage(fin_partie=True)
    # On calcule qui a gagné
    gerer_fin_de_partie()
 
# Fonction pour initialiser et lancer une nouvelle partie
def nouvelle_partie():
    # Déclaration des variables globales
    global paquet, main_joueur, main_croupier
    # On réactive les boutons d'action
    bouton_hit.config(state="normal")
    bouton_stand.config(state="normal")
    # On recrée un paquet complet à partir du paquet de base
    paquet = list(paquet_base)
    # On mélange le paquet
    random.shuffle(paquet)
    # On distribue 2 cartes au joueur
    main_joueur   = [paquet.pop(), paquet.pop()]
    # On distribue 2 cartes au croupier
    main_croupier = [paquet.pop(), paquet.pop()]
    # On met à jour l'affichage graphique
    actualiser_affichage(fin_partie=False)
 
 

# Création de la fenêtre principale
racine = tk.Tk()
# Nom de la fenêtre
racine.title("Blackjack Python")
 
# Tentative de mettre la fenêtre en plein écran selon le système d'exploitation (Mac/Windows)
try:
    racine.state('zoomed')
except Exception:
    racine.attributes('-zoomed', True)
 
# Configuration de la grille de la fenêtre pour gérer le placement des éléments
racine.grid_rowconfigure(0, weight=1) # Ligne du tapis (prend tout l'espace)
racine.grid_rowconfigure(1, weight=0) # Ligne des boutons (prend juste l'espace nécessaire)
racine.grid_columnconfigure(0, weight=1)
racine.grid_columnconfigure(1, weight=0)
 
# Création du "Canvas" (la zone de dessin), coloré en vert Casino
canvas = tk.Canvas(racine, bg="#2E8B57")
# Placement du canvas dans la fenêtre
canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")
 
# Exécution de la fonction pour découper les images en mémoire
charger_images()
 
# Création d'une zone (Frame) en bas à droite pour regrouper les boutons
frame_boutons = tk.Frame(racine)
frame_boutons.grid(row=1, column=1, sticky="e", pady=10, padx=20)
 
# Création et placement du bouton "Deal" (Nouvelle Partie) avec son image découpée
bouton_deal  = tk.Button(frame_boutons, image=img_bouton_deal,  command=nouvelle_partie, borderwidth=0)
bouton_deal.grid(row=0, column=0, padx=5)
 
# Création et placement du bouton "Hit" (Tirer) avec son image découpée
bouton_hit   = tk.Button(frame_boutons, image=img_bouton_hit,   command=action_hit,      borderwidth=0)
bouton_hit.grid(row=0, column=1, padx=5)
 
# Création et placement du bouton "Stand" (Rester) avec son image découpée
bouton_stand = tk.Button(frame_boutons, image=img_bouton_stand, command=action_stand,    borderwidth=0)
bouton_stand.grid(row=0, column=2, padx=5)
 
# Au bout de 150 millisecondes après le lancement de l'application, la première partie démarre
racine.after(150, nouvelle_partie)
# Boucle principale qui maintient la fenêtre ouverte et attend les clics de l'utilisateur
racine.mainloop()