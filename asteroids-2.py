#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Implémentation du jeu Asteroids : rotation du vaisseau.
# Copyright (C) 2020-2021 - Jérôme Kirman (Palais de la Découverte)
# Ce programme est un logiciel libre ; voir les fichiers README.md et LICENSE.

# Modules requis
from math import pi
import sys

import pygame
from pygame.locals import *

# Taille de la fenêtre
XMAX, YMAX = 800, 600

# Ressources graphiques
charger = pygame.image.load
IMG_VAISSEAU = charger("ship.png")

# Fonctions utiles
tourner = pygame.transform.rotate

# Conversion radians/degrés
def rad2deg(a):
	return - 180 * a / pi - 90

# Objets du jeu
class Vaisseau():
	VANG = pi/20          # Vitesse de rotation

	x, y = XMAX/2, YMAX/2 # Position actuelle
	angle = 0             # Rotation actuelle

	img = IMG_VAISSEAU    # Image
	rect = (x, y, 20, 20) # Emplacement

	def maj_vaisseau(j):
		# Recalcul de l'image
		j.img = tourner(IMG_VAISSEAU, rad2deg(j.angle))
		tx, ty = j.img.get_size()
		j.rect = (int(j.x), int(j.y), tx, ty)

	# Commandes du vaisseau
	def tourner(j, direction):
		j.angle += direction * j.VANG

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
	if appui[K_LEFT]:
		joueur.tourner(-1)
	if appui[K_RIGHT]:
		joueur.tourner(+1)

	# PHYSIQUE
	joueur.maj_vaisseau()

	# DESSIN
	fenetre.fill(pygame.Color(0,0,10))

	fenetre.blit(joueur.img, joueur.rect)

	# Mise à jour de l'écran
	pygame.display.update()

	# Attente pour atteindre 30 IPS
	horloge.tick(30)
