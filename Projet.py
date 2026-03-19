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
    print("ce ,'est pas un as?")
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


choixJoueur = int(input("Que veut tu faire: Hit, Stand, Double Down, Surrender"))
carte3 = 0
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


#test g








#test Merwan 


          
