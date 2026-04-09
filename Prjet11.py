#BLACKJACK: 
# Guillaume Garnier, Merwan Ben mahmoud-Branchur, Younes Mahmoudi

import random
cartes_joueur = 0
carte_croupier =0 
val_as = random.randint(1,2)
if val_as == 1:
    print("c'est un as")
    carte1 = int(input("veut tu que l'as valent 1 ou 11?"))
    if carte1 == 1:
        print("Le joueur a 1")
    else: print("Le joueur a choisi 11")

else:
    print("ce , n'est pas un as")
    if val_as==2:
        carte1 = random.randint(2,10)
        print(carte1)



val_as2 = random.randint(1,2)
if val_as2 == 1:
    print("c'est un as")
    carte2 = int(input("veut tu que l'as valent 1 ou 11?"))
    if carte2 == 1:
        print("Le joueur a 1")
    else: 
        print("Le joueur a choisi 11")

else:
    print("ce ,'est pas un as")
    if val_as2==2:
        carte2 = random.randint(2,10)
        print(carte2)

carte_joueur = carte1 + carte2 
print(carte_joueur)


choixJoueur = str(input("Que veut tu faire: Hit, Stand, Double Down, Surrender:"))
carte3 = 0
if choixJoueur == "Surrender":
    print("Le joueur a abandonné, Il a perdu la partie  et recupère la moitié de sa mise")


if choixJoueur == "Hit":
    val_as3= random.randint(1,2)
    if val_as3 == 1: 
        print("C'est un AS")
        carte3 = int(input("veut tu qu'il valent 1 ou 11"))
        if carte3 ==1: 
            print("le joueur a obtenue 1")
        else: 
            print("le joueur a choisi 11")
    else: 
        print("ce n'est pas un As")
        if val_as3== 2: 
            carte3 = random.randint(2,10)
            print(carte3)
    
carte_joueur += carte3
print(carte_joueur)

if carte_joueur <= 21: 
    int(input("Que veut tu faire: Stand, Hit"))
















def tirage_blackjack():
    valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    couleurs = ['♠', '♥', '♦', '♣']
    
    def tirer():
        return random.choice(valeurs) + random.choice(couleurs)
    
    joueur = [tirer(), tirer()]
    croupier = [tirer(), tirer()]
    
    return joueur, croupier

joueur, croupier = tirage_blackjack()
print("Joueur :", joueur)
print("Croupier :", [croupier[0], "??"])  




# On prépare un paquet de cartes
paquet = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4 # x4 pour représenter les 4 couleurs

def calculer_score(main):
    score = 0
    as_possede = 0
    for carte in main:
        if carte in ["J", "Q", "K"]: score += 10
        elif carte == "A":
            score += 11
            as_possede += 1
        else: score += int(carte)
    
    # Si on dépasse 21, l'As vaut 1 au lieu de 11
    while score > 21 and as_possede > 0:
        score -= 10
        as_possede -= 1
    return score

# -TIRAGE INITIALE
random.shuffle(paquet)
main_joueur = [paquet.pop(), paquet.pop()] # pop() supprime la cartes du tirage du jeu de cartes pour eviter de la tirer "50 fois d'affilé"
main_croupier = [paquet.pop(), paquet.pop()]

# -TOUR DU JOUEUR
while True:
    score_j = calculer_score(main_joueur)
    print(f"Votre main : {main_joueur} | Score : {score_j}")
    
    if score_j >= 21:
        break
        
    choix = input("Tapez 'h' pour Hit (tirer) ou 's' pour Stand (rester) : ").lower()
    if choix == 'h':
        main_joueur.append(paquet.pop())
    else:
        break

# - TOUR DU CROUPIER 
score_j = calculer_score(main_joueur)

if score_j <= 21:
    print(f"\nMain du croupier : {main_croupier}")
    while calculer_score(main_croupier) < 17:
        main_croupier.append(paquet.pop())
        print(f"Le croupier tire une carte... Nouvelle main : {main_croupier}")

# - VERDICT 
score_c = calculer_score(main_croupier)
print(f"\nScore Final - Vous: {score_j} | Croupier: {score_c}")

if score_j > 21:
    print("Vous avez dépassé 21... Perdu !")
elif score_c > 21 or score_j > score_c:
    print("Gagné !")
elif score_j < score_c:
    print("Le croupier gagne !")
else:
    print("Égalité !")