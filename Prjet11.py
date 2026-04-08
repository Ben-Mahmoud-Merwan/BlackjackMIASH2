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


# exemple
joueur, croupier = tirage_blackjack()
print("Joueur :", joueur)
print("Croupier :", [croupier[0], "??"])  # une cachée






import random

paquet = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4

def valeur_main(main):
    total = 0
    as_count = 0

    for carte in main:
        if carte in ["J", "Q", "K"]:
            total += 10
        elif carte == "A":
            total += 11
            as_count += 1
        else:
            total += int(carte)

    while total > 21 and as_count:
        total -= 10
        as_count -= 1

    return total

def tirer():
    return random.choice(paquet)

def blackjack():
    joueur = [tirer(), tirer()]
    croupier = [tirer(), tirer()]

    print("Ta main :", joueur, "=", valeur_main(joueur))
    print("Carte visible croupier :", croupier[0])

    # tour joueur
    while valeur_main(joueur) < 21:
        choix = input("hit ou stand ? ")

        if choix == "hit":
            joueur.append(tirer())
            print("Ta main :", joueur, "=", valeur_main(joueur))
        else:
            break

    if valeur_main(joueur) > 21:
        print("Tu brûles, perdu")
        return

    # tour croupier (tire à 16 reste à 17)
    while valeur_main(croupier) < 17:
        croupier.append(tirer())

    print("Main croupier :", croupier, "=", valeur_main(croupier))

    # résultat
    if valeur_main(croupier) > 21:
        print("Croupier brûle, gagné")
    elif valeur_main(joueur) > valeur_main(croupier):
        print("Gagné")
    elif valeur_main(joueur) < valeur_main(croupier):
        print("Perdu")
    else:
        print("Égalité")

# lancer le jeu
blackjack()