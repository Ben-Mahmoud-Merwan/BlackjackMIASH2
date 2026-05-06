import random # Importation du module random pour mélanger le paquet et choisir les couleurs aléatoirement
import tkinter as tk # Importation de tkinter pour créer la fenêtre et l'interface graphique
from PIL import Image, ImageTk # Importation de PIL pour ouvrir, découper et redimensionner les images de cartes
 
 
# --- CODE DE BASE ---
 
# On crée le paquet de base avec les 13 valeurs répétées 4 fois (une fois par couleur : trèfle, carreau, cœur, pique)
paquet_base = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4
 
 
def calculer_score(main): # Fonction qui calcule le score total d'une main de cartes passée en paramètre
    score = 0 # Initialisation du score à 0
    as_possede = 0 # Compteur d'As dans la main (leur valeur peut changer entre 11 et 1)
    for carte in main: # On parcourt chaque carte de la main
        if carte in ["J", "Q", "K"]: score += 10 # Valet, Dame et Roi valent tous 10 points
        elif carte == "A": # Si c'est un As :
            score += 11 # On lui attribue d'abord la valeur maximale de 11
            as_possede += 1 # On note qu'on possède un As de plus
        else: score += int(carte) # Pour les cartes numériques (2 à 10), on convertit le texte en nombre et on l'ajoute
    while score > 21 and as_possede > 0: # Tant qu'on dépasse 21 ET qu'on a encore des As comptés à 11 :
        score -= 10 # On repasse cet As de 11 à 1 (soit -10 au score)
        as_possede -= 1 # On retire cet As du compteur d'As valant encore 11
    return score # On retourne le score final calculé
 
 
# --- INTERFACE GRAPHIQUE ---
 
def charger_images(): # Fonction qui ouvre les fichiers image et découpe chaque bouton et chaque carte
    global img_cartes, img_bouton_hit, img_bouton_stand, img_bouton_deal, img_dos_carte # Ces variables sont déclarées globales pour que Python ne les efface pas de la mémoire (risque de disparition des images sinon)
 
    # --- Chargement des boutons ---
    image_boutons = Image.open("button d'action.png") # Ouverture de l'image contenant tous les boutons bleus sur une seule image de 700x210 pixels
    img_bouton_deal  = ImageTk.PhotoImage(image_boutons.crop((  0, 0,  70, 70))) # Découpe du bouton DEAL : colonne 0, chaque bouton fait 70x70 pixels
    img_bouton_hit   = ImageTk.PhotoImage(image_boutons.crop((280, 0, 350, 70))) # Découpe du bouton HIT : colonne 4 (4 x 70 = 280 pixels depuis la gauche)
    img_bouton_stand = ImageTk.PhotoImage(image_boutons.crop((350, 0, 420, 70))) # Découpe du bouton STAND : colonne 5 (5 x 70 = 350 pixels depuis la gauche)
 
    # --- Chargement des cartes ---
    image = Image.open("cartes.png") # Ouverture de la grande image contenant les 53 cartes empilées verticalement (dos + 52 cartes)
    carte_hauteur = image.height // 53 # Calcul de la hauteur d'une seule carte : hauteur totale divisée par 53 cartes (~150 pixels)
    TAILLE = (143, 221) # Taille d'affichage finale choisie pour chaque carte (proportions réelles d'une carte à jouer)
 
    img_dos_carte = ImageTk.PhotoImage( # Création de l'image du dos de carte :
        image.crop((0, 0, 110, 170)).resize(TAILLE, Image.Resampling.LANCZOS) # On découpe la première zone (le dos) et on la redimensionne à la taille finale
    )
 
    # Chargement des 52 cartes organisées en 4 couleurs de 13 valeurs :
    # Indices 0→12 = Trèfle | 13→25 = Carreau | 26→38 = Cœur | 39→51 = Pique
    rangs = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] # Liste des 13 valeurs dans l'ordre du fichier image
    img_cartes = {} # Dictionnaire qui associera chaque tuple (valeur, couleur_idx) à son image tkinter
    for couleur_idx in range(4): # On parcourt les 4 couleurs (0=Trèfle, 1=Carreau, 2=Cœur, 3=Pique)
        for i, valeur in enumerate(rangs): # On parcourt les 13 valeurs avec leur position (i) dans la couleur
            y1 = (couleur_idx * 13 + i) * carte_hauteur + 170 # Calcul du bord haut de la carte dans le fichier : on saute le dos (170px) puis on compte les cartes précédentes
            y2 = y1 + carte_hauteur # Calcul du bord bas de la carte
            img_cartes[(valeur, couleur_idx)] = ImageTk.PhotoImage( # On stocke l'image dans le dictionnaire avec le tuple comme clé
                image.crop((0, y1, image.width, y2)).resize(TAILLE, Image.Resampling.LANCZOS) # Découpage puis redimensionnement à la taille finale
            )
 
 
def piocher_carte(): # Fonction qui tire une carte du paquet et lui attribue une couleur d'affichage aléatoire
    valeur = paquet.pop() # On retire la dernière carte du paquet mélangé (et on la supprime du paquet)
    couleur_idx = random.randint(0, 3) # On choisit aléatoirement une couleur parmi les 4 (0=Trèfle, 1=Carreau, 2=Cœur, 3=Pique)
    return (valeur, couleur_idx) # On retourne un tuple contenant la valeur de la carte et l'index de sa couleur d'affichage
 
 
def actualiser_affichage(fin_partie=False): # Fonction qui efface et redessine tout le tapis (scores + cartes) à chaque action du joueur
    canvas.update_idletasks() # Force tkinter à mettre à jour les dimensions réelles du canvas avant qu'on les lise
    W = canvas.winfo_width() # Récupération de la largeur actuelle du canvas en pixels
    H = canvas.winfo_height() # Récupération de la hauteur actuelle du canvas en pixels
    if W < 50 or H < 50: # Si le canvas n'est pas encore affiché (dimensions trop petites) :
        racine.after(50, lambda: actualiser_affichage(fin_partie)) # On réessaie dans 50 millisecondes
        return # On sort de la fonction pour éviter d'afficher sur un canvas vide
 
    canvas.delete("all") # On efface tout ce qui est actuellement dessiné sur le tapis vert
 
    score_j = calculer_score([c[0] for c in main_joueur]) # Calcul du score du joueur : on extrait uniquement la valeur (c[0]) de chaque tuple (valeur, couleur_idx)
    score_c = calculer_score([c[0] for c in main_croupier]) # Idem pour le croupier
 
    # Affichage du score du joueur en bas à gauche du tapis
    canvas.create_text(120, H - 30,
                       text=f"Votre Score : {score_j}",
                       font=("Helvetica", 20, "bold"), fill="white")
 
    if fin_partie: # Si la partie est terminée (le croupier a joué) :
        canvas.create_text(W - 200, 30, # Affichage du vrai score final du croupier en haut à droite
                           text=f"Score Croupier : {score_c}",
                           font=("Helvetica", 20, "bold"), fill="white")
    else: # Si on est encore en cours de partie :
        valeur_visible = calculer_score([main_croupier[0][0]]) # On calcule uniquement le score de la première carte visible du croupier
        canvas.create_text(W - 200, 30, # Affichage du score partiel avec un "?" pour la carte cachée
                           text=f"Score Croupier : {valeur_visible} + ?",
                           font=("Helvetica", 20, "bold"), fill="white")
 
    ESPACEMENT = 153 # Décalage horizontal entre deux cartes : 143px (largeur carte) + 10px de marge
 
    # --- Affichage des cartes du croupier en haut du tapis ---
    nb_c = len(main_croupier) # Nombre de cartes actuelles dans la main du croupier
    offset_c = W // 2 - (nb_c * ESPACEMENT) // 2 # Calcul du point de départ pour centrer le groupe de cartes horizontalement
    for index, carte in enumerate(main_croupier): # On parcourt chaque carte du croupier avec son numéro d'ordre
        px = offset_c + index * ESPACEMENT + 71 # Position horizontale du centre de cette carte (71 = moitié de 143px)
        if index == 1 and not fin_partie: # Si c'est la 2ème carte ET que la partie n'est pas finie :
            canvas.create_image(px, H // 4, image=img_dos_carte) # On affiche le dos de carte (carte cachée)
        else: # Sinon (1ère carte ou fin de partie) :
            canvas.create_image(px, H // 4, image=img_cartes[carte]) # On affiche la vraie face de la carte
 
    # --- Affichage des cartes du joueur en bas du tapis ---
    nb_j = len(main_joueur) # Nombre de cartes actuelles dans la main du joueur
    offset_j = W // 2 - (nb_j * ESPACEMENT) // 2 # Calcul du point de départ pour centrer le groupe de cartes horizontalement
    for index, carte in enumerate(main_joueur): # On parcourt chaque carte du joueur avec son numéro d'ordre
        px = offset_j + index * ESPACEMENT + 71 # Position horizontale du centre de cette carte
        canvas.create_image(px, 3 * H // 4 - 20, image=img_cartes[carte]) # On affiche la carte face visible
 
 
def gerer_fin_de_partie(): # Fonction qui détermine le gagnant et affiche le texte de résultat au centre du tapis
    canvas.update_idletasks() # Force la mise à jour des dimensions du canvas
    W = canvas.winfo_width() # Récupération de la largeur du canvas
    H = canvas.winfo_height() # Récupération de la hauteur du canvas
    cx, cy = W // 2, H // 2 # Calcul du centre exact du tapis pour placer le texte de résultat
 
    score_j = calculer_score([c[0] for c in main_joueur]) # Score final du joueur
    score_c = calculer_score([c[0] for c in main_croupier]) # Score final du croupier
 
    FONT = ("Helvetica", 90, "bold") # Police grande et grasse pour que le résultat soit bien visible
    if score_j > 21: # Règle 1 : le joueur a dépassé 21, il perd automatiquement
        canvas.create_text(cx, cy, text="LOSER",  font=FONT, fill="red") # Texte LOSER en rouge
    elif score_c > 21 or score_j > score_c: # Règle 2 : le croupier dépasse 21 OU le joueur a un meilleur score
        canvas.create_text(cx, cy, text="WINNER", font=FONT, fill="yellow") # Texte WINNER en jaune
    elif score_c <= 21 and score_j < score_c: # Règle 3 : le croupier a un meilleur score sans dépasser 21
        canvas.create_text(cx, cy, text="LOSER",  font=FONT, fill="red") # Texte LOSER en rouge
    else: # Règle 4 : égalité de score
        canvas.create_text(cx, cy, text="DRAW",   font=FONT, fill="gray") # Texte DRAW en gris
 
    bouton_hit.config(state="disabled") # Désactivation du bouton HIT pour empêcher de tirer après la fin de partie
    bouton_stand.config(state="disabled") # Désactivation du bouton STAND après la fin de partie
    bouton_deal.config(state="normal") # Réactivation du bouton DEAL maintenant que la partie est terminée : le joueur peut relancer
 
 
def action_hit(): # Fonction déclenchée quand le joueur appuie sur le bouton HIT (tirer une carte)
    main_joueur.append(piocher_carte()) # On tire une nouvelle carte et on l'ajoute à la main du joueur
    if calculer_score([c[0] for c in main_joueur]) >= 21: # Si le joueur atteint ou dépasse 21 :
        actualiser_affichage(fin_partie=True) # On révèle la carte cachée du croupier
        gerer_fin_de_partie() # On affiche le résultat final
    else: # Si le joueur est encore en dessous de 21 :
        actualiser_affichage(fin_partie=False) # On rafraîchit simplement l'affichage avec la nouvelle carte
 
 
def action_stand(): # Fonction déclenchée quand le joueur appuie sur STAND (rester / ne plus tirer)
    while calculer_score([c[0] for c in main_croupier]) < 17: # Le croupier tire des cartes tant qu'il a moins de 17 (règle du casino)
        main_croupier.append(piocher_carte()) # Le croupier pioche une carte et l'ajoute à sa main
    actualiser_affichage(fin_partie=True) # On révèle la carte cachée du croupier et on affiche son score réel
    gerer_fin_de_partie() # On compare les scores et on affiche le résultat
 
 
def nouvelle_partie(): # Fonction qui réinitialise et lance une nouvelle partie
    global paquet, main_joueur, main_croupier # On déclare ces variables globales pour pouvoir les modifier ici
    bouton_deal.config(state="disabled") # Désactivation du bouton DEAL pendant la partie : on ne peut pas relancer une partie en cours
    bouton_hit.config(state="normal") # Réactivation du bouton HIT (il était désactivé depuis la fin de la partie précédente)
    bouton_stand.config(state="normal") # Réactivation du bouton STAND
    paquet = list(paquet_base) # Copie du paquet de base (pour ne pas modifier l'original)
    random.shuffle(paquet) # Mélange aléatoire du paquet comme au casino
    main_joueur   = [piocher_carte(), piocher_carte()] # Distribution des 2 cartes de départ au joueur
    main_croupier = [piocher_carte(), piocher_carte()] # Distribution des 2 cartes de départ au croupier
    actualiser_affichage(fin_partie=False) # Affichage initial des cartes (avec la 2ème carte du croupier cachée)
 
 
# ── CRÉATION DE LA FENÊTRE ET DE L'INTERFACE ──────────────────────────────────
 
racine = tk.Tk() # Création de la fenêtre principale de l'application
racine.title("Blackjack Python") # Titre affiché dans la barre de la fenêtre
 
try:
    racine.state('zoomed') # Ouverture en mode fenêtré maximisé (plein écran sans cacher la barre des tâches) — fonctionne sur Windows et macOS
except Exception:
    racine.attributes('-zoomed', True) # Même effet sur Linux / systèmes X11
 
# Configuration de la grille de la fenêtre : 2 lignes, 2 colonnes
racine.grid_rowconfigure(0, weight=1) # La ligne 0 (tapis) s'étire pour remplir tout l'espace vertical disponible
racine.grid_rowconfigure(1, weight=0) # La ligne 1 (boutons) garde une hauteur fixe, elle ne s'étire pas
racine.grid_columnconfigure(0, weight=1) # La colonne 0 s'étire horizontalement pour remplir l'espace
racine.grid_columnconfigure(1, weight=0) # La colonne 1 (boutons) garde une largeur fixe
 
canvas = tk.Canvas(racine, bg="#2E8B57") # Création du tapis de jeu vert (couleur casino) sans dimensions fixes : il s'adapte à la fenêtre
canvas.grid(row=0, column=0, columnspan=2, sticky="nsew") # Placement du canvas sur toute la ligne 0 (2 colonnes), il s'étire dans toutes les directions
 
charger_images() # Appel de la fonction qui charge toutes les images en mémoire (doit être fait après la création de la fenêtre)
 
frame_boutons = tk.Frame(racine) # Création d'un conteneur invisible qui regroupe les 3 boutons ensemble
frame_boutons.grid(row=1, column=1, sticky="e", pady=10, padx=20) # Placement en bas à droite de la fenêtre avec des marges
 
bouton_deal  = tk.Button(frame_boutons, image=img_bouton_deal,  command=nouvelle_partie, borderwidth=0) # Bouton DEAL : lance une nouvelle partie au clic
bouton_deal.grid(row=0, column=0, padx=5) # Placement dans la première colonne du conteneur
bouton_deal.config(state="normal") # Le bouton DEAL est actif au tout premier lancement pour permettre de démarrer la première partie
 
bouton_hit   = tk.Button(frame_boutons, image=img_bouton_hit,   command=action_hit,      borderwidth=0) # Bouton HIT : tire une carte au clic
bouton_hit.grid(row=0, column=1, padx=5) # Placement dans la deuxième colonne du conteneur
bouton_hit.config(state="disabled") # Le bouton HIT est désactivé au démarrage : il faut d'abord appuyer sur DEAL pour commencer
 
bouton_stand = tk.Button(frame_boutons, image=img_bouton_stand, command=action_stand,    borderwidth=0) # Bouton STAND : le joueur arrête de tirer et le croupier joue
bouton_stand.grid(row=0, column=2, padx=5) # Placement dans la troisième colonne du conteneur
bouton_stand.config(state="disabled") # Le bouton STAND est désactivé au démarrage : il faut d'abord appuyer sur DEAL pour commencer
 
racine.mainloop() # Démarrage de la boucle principale de tkinter qui maintient la fenêtre ouverte et écoute les événements (clics, touches...)