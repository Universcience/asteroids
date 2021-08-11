#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Implémentation du jeu Asteroids : ajout collisions et fin de partie.
# Copyright (C) 2020-2021 - Jérôme Kirman (Palais de la Découverte)
# Ce programme est un logiciel libre ; voir les fichiers README.md et LICENSE.

# Modules requis
from math import pi, cos, sin, sqrt
import sys, random

import pygame
from pygame.locals import *

# Taille de la fenêtre
XMAX, YMAX = 800, 600

# Ressources graphiques
charger = pygame.image.load
IMG_ASTEROIDE = charger("rock.png")
IMG_VAISSEAU = charger("ship.png")

# Fonctions utiles
tourner = pygame.transform.rotate

# Conversion radians/degrés
def rad2deg(a):
	return - 180 * a / pi - 90

def collision(a, b, dist):
	dx = a.x - b.x
	dy = a.y - b.y
	return sqrt(dx**2 + dy**2) < dist

def hasard(x):
	return random.randint(0,x)

def quitter(msg):
	print (msg)
	pygame.quit()
	sys.exit()

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

class Asteroide():
	vang = hasard(20) - 10

	x, y = 0, 0
	vx, vy = 0, 0
	angle = 0

	img = None
	rect = (0, 0, 0, 0)

	def maj_asteroide(a):
		a.x = (a.x + a.vx) % XMAX
		a.y = (a.y + a.vy) % YMAX

		a.angle += a.vang % 360

		a.img = tourner(IMG_ASTEROIDE, a.angle)
		tx, ty = a.img.get_size()
		a.rect = (int(a.x), int(a.y), tx, ty)

# Corps du jeu
pygame.init()

# Création du joueur et des astéroïdes
joueur = Vaisseau()

asteroides = []
for i in range(5):
	a = Asteroide()
	a.vx = hasard(16) - 8
	a.vy = hasard(16) - 8
	asteroides.append(a)

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
		quitter("Quitté le jeu.")
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

	for a in asteroides:
		a.maj_asteroide()

	# Fin de partie ?
	for a in asteroides:
		if collision(joueur, a, 12):
			quitter("Game over !")

	# DESSIN
	fenetre.fill(pygame.Color(0,0,10))

	fenetre.blit(joueur.img, joueur.rect)

	for a in asteroides:
		fenetre.blit(a.img, a.rect)

	# Mise à jour de l'écran
	pygame.display.update()

	# Attente pour atteindre 30 IPS
	horloge.tick(30)
