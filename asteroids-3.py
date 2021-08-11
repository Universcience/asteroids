#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Implémentation du jeu Asteroids : déplacement et accélération du vaisseau.
# Copyright (C) 2020-2021 - Jérôme Kirman (Palais de la Découverte)
# Ce programme est un logiciel libre ; voir les fichiers README.md et LICENSE.

# Modules requis
from math import pi, cos, sin
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
	ACCEL = 0.2           # Accélération

	x, y = XMAX/2, YMAX/2 # Position actuelle
	vx, vy = 0, 0         # Vitesse actuelle
	angle = 0             # Rotation actuelle

	img = IMG_VAISSEAU    # Image
	rect = (x, y, 20, 20) # Emplacement

	def maj_vaisseau(j):
		# Recalcul de la position
		j.x = (j.x + j.vx) % XMAX
		j.y = (j.y + j.vy) % YMAX

		# Recalcul de l'image
		j.img = tourner(IMG_VAISSEAU, rad2deg(j.angle))
		tx, ty = j.img.get_size()
		j.rect = (int(j.x), int(j.y), tx, ty)

	# Commandes du vaisseau
	def tourner(j, direction):
		j.angle += direction * j.VANG

	def accelerer(j, direction):
		acc = direction * j.ACCEL
		j.vx += acc * cos(j.angle)
		j.vy += acc * sin(j.angle)

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
	if appui[K_UP]:
		joueur.accelerer(+1)
	if appui[K_DOWN]:
		joueur.ralentir(-1)

	# PHYSIQUE
	joueur.maj_vaisseau()

	# DESSIN
	fenetre.fill(pygame.Color(0,0,10))

	fenetre.blit(joueur.img, joueur.rect)

	# Mise à jour de l'écran
	pygame.display.update()

	# Attente pour atteindre 30 IPS
	horloge.tick(30)
