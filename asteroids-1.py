#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Implémentation du jeu Asteroids : ajout du vaisseau.
# Copyright (C) 2020-2021 - Jérôme Kirman (Palais de la Découverte)
# Ce programme est un logiciel libre ; voir les fichiers README.md et LICENSE.

# Modules requis
import sys

import pygame
from pygame.locals import *

# Taille de la fenêtre
XMAX, YMAX = 800, 600

# Ressources graphiques
charger = pygame.image.load
IMG_VAISSEAU = charger("ship.png")

# Objets du jeu
class Vaisseau():
	x, y = XMAX/2, YMAX/2 # Position actuelle

	img = IMG_VAISSEAU    # Image
	rect = (x, y, 20, 20) # Emplacement

# Corps du jeu
pygame.init()

# Création du joueur
joueur = Vaisseau()

# Fenêtre du jeu
fenetre = pygame.display.set_mode((XMAX,YMAX))
# Horloge limitant les IPS
horloge = pygame.time.Clock()

# Boucle principale
while (True):
	# CONTRÔLES
	pygame.event.get()
	appui = pygame.key.get_pressed()
	if appui[K_ESCAPE]:
		sys.exit()

	# DESSIN
	fenetre.fill(pygame.Color(0,0,10))

	fenetre.blit(joueur.img, joueur.rect)

	# Mise à jour de l'écran
	pygame.display.update()

	# Attente pour atteindre 30 IPS
	horloge.tick(30)
