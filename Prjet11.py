#BLACKJACK: 
# Guillaume Garnier, Merwan Ben mahmoud-Branchur, Younes Mahmoudi

import random

# On prépare un paquet de cartes
paquet = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4 # x4 pour représenter les 4 couleurs

def calculer_score(main):
    score = 0
    as_possede = 0 #As present dans la main 
    for carte in main:
        if carte in ["J", "Q", "K"]: score += 10 # valeur du Roi, Reine, Valet
        elif carte == "A":
            score += 11 #valeur de l'As = 11
            as_possede += 1 # As possédé prend +1
        else: score += int(carte) #Si c'est un chiffre (2 à 10), on transforme le txt en nbr entier et on l'ajoute au score.
    
    # Si on dépasse 21, l'As vaut 1 au lieu de 11
    while score > 21 and as_possede > 0: 
        score -= 10 # l'As vaut maintenant 1 dans on soustrait 10 au score 
        as_possede -= 1 #on enleve l'As utilisé 
    return score

# -TIRAGE INITIALE
random.shuffle(paquet) #Shuffle melange le paquet comme au Casino 
main_joueur = [paquet.pop(), paquet.pop()] # pop() supprime la cartes du tirage du jeu de cartes pour eviter de la tirer "50 fois d'affilé"
main_croupier = [paquet.pop(), paquet.pop()]

# -TOUR DU JOUEUR
while True: # boucle infini pour enchainé les tour si on veut 
    score_j = calculer_score(main_joueur)
    print(f"Votre main : {main_joueur} --> Score : {score_j}")
    
    if score_j >= 21: # on a perdu car on depasse 21 
        break
        
    choix = input("Tapez 'h' pour Hit (tirer) ou 's' pour Stand (rester) : ").lower()
    if choix == 'h':
        main_joueur.append(paquet.pop()) #Hit alors on tire une carte et on l'ajoute au score, 
    else:
        break #Stand donc on s'arrete 

# - TOUR DU CROUPIER 
score_j = calculer_score(main_joueur)

if score_j <= 21: # si n'a pas eu 21 directement avec les care de depart il tire 
    print(f"\nMain du croupier : {main_croupier}")
    while calculer_score(main_croupier) < 17: # il tire une carte si il est en dessous de 17 sinon il reste
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