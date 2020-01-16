#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Implémentation objet du jeu Asteroids.
# Copyright (C) 2020 - Jérôme Kirman
# Ce programme est un logiciel libre ; voir les fichiers README.md et LICENSE.

# Modules requis
from math import cos, sin, pi
import random
import sys

import pygame
from pygame.locals import *

# Taille de l'écran
XMAX = 800
YMAX = 600

# Ressources graphiques
IMG_ASTEROIDE = pygame.image.load("asteroid.png")
IMG_VAISSEAU = pygame.image.load("ship.png")
IMG_LASER = pygame.image.load("lazor.png")

# Conversion radians/degrés
def rad2deg(a):
	return - 180 * a / pi - 90

# Roll The Dice !
def rtd(x):
	return random.randint(0,x)

# Le vaisseau du joueur
class Vaisseau(pygame.sprite.Sprite):
	# Propriétés statiques
	vang = pi/30
	accel = 0.2

	def __init__(self):
		# Données du jeu
		self.x , self.y  = XMAX/2, YMAX/2 # Position
		self.vx, self.vy = 0, 0           # Vitesse
		self.angle = 0                    # Rotation
		self.tirs = []                    # Lasers tirés
		# Données du sprite
		super().__init__()

		self.update()

	# Mise à jour (à chaque image)
	def update(self):
		# Mise à jour de la position (avec boucle aux bords de l'écran)
		self.x = (self.x + self.vx) % XMAX
		self.y = (self.y + self.vy) % YMAX

		# Recalcul de l'image et du masque pour les collisions
		self.image = pygame.transform.rotate(IMG_VAISSEAU, rad2deg(self.angle))
		self.rect = (int(self.x), int(self.y), self.image.get_width(), self.image.get_height())
		self.mask = pygame.mask.from_surface(self.image)

	# Commandes du vaisseau
	def tourner(self, direction):
		self.angle += direction * self.vang

	def accelerer(self):
		self.vx += self.accel * cos(self.angle)
		self.vy += self.accel * sin(self.angle)

	def ralentir(self):
		self.vx -= self.accel * cos(self.angle)
		self.vy -= self.accel * sin(self.angle)

	def tirer(self):
		self.tirs.append(Laser(self))

# Les tirs du joueur
class Laser(pygame.sprite.Sprite):
	vitesse = 20

	def __init__(self, tireur):
		# Jeu
		self.x, self.y = tireur.x, tireur.y        # Position
		self.vx = self.vitesse * cos(tireur.angle) # Vitesse horizontale
		self.vy = self.vitesse * sin(tireur.angle) # Vitesse verticale

		# Sprite
		super().__init__()
		self.image = pygame.transform.rotate(IMG_LASER, rad2deg(tireur.angle))
		self.update()
		self.mask = pygame.mask.from_surface(self.image)

	# Mise à jour (à chaque image)
	def update(self):
		self.x += self.vx
		self.y += self.vy
		self.rect = (int(self.x), int(self.y), self.image.get_width(), self.image.get_height())

# Les astéroïdes hostiles
class Asteroide(pygame.sprite.Sprite):
	def __init__(self):
		# Jeu
		self.x, self.y = 0, 0                     # Position
		self.vx, self.vy = rtd(20)-10, rtd(20)-10 # Vitesse
		self.angle = 0                            # Rotation initiale
		self.va = pi / 15                         # Vitesse angulaire
		# Sprite
		super().__init__()
		self.update()

	# Mise à jour (à chaque image)
	def update(self):
		# Déplacement (avec boucle aux bords de l'écran) et rotation
		self.x = (self.x + self.vx) % XMAX
		self.y = (self.y + self.vy) % YMAX
		self.angle = (self.angle + self.va) % (2*pi)

		# Recalcul de l'image et du masque pour les collisions
		self.image = pygame.transform.rotate(IMG_ASTEROIDE, rad2deg(self.angle))
		self.rect = (int(self.x), int(self.y), self.image.get_width(), self.image.get_height())
		self.mask = pygame.mask.from_surface(self.image)

# Quitter le jeu
def quit():
	pygame.quit()
	sys.exit()

# Fonction principale
def main():
	# Création du joueur et des menaces
	joueur = Vaisseau()
	asteroides = [Asteroide(), Asteroide(), Asteroide()]

	# Couleur du fond
	black = pygame.Color(0,0,0)

	# Fenêtre du jeu
	fenetre = pygame.display.set_mode((XMAX,YMAX))
	# Horloge limitant les IPS
	horloge = pygame.time.Clock()

	# Boucle principale
	while (True):
		# Traitement des évènements (clavier)
		for e in pygame.event.get():
			pass

		# CONTRÔLES
		#  ECHAP          quitter
		#  GAUCHE/DROITE  rotation gauche/droite
		#  HAUT/BAS       accélérer/ralentir
		#  SPACE          tirer
		appui = pygame.key.get_pressed()
		if appui[K_ESCAPE]:
			quit()
		if appui[K_LEFT]:
			joueur.tourner(-1)
		if appui[K_RIGHT]:
			joueur.tourner(+1)
		if appui[K_UP]:
			joueur.accelerer()
		if appui[K_DOWN]:
			joueur.ralentir()
		if appui[K_SPACE]:
			joueur.tirer()
		
		# PHYSIQUE
		joueur.update()

		for a in asteroides:
			a.update()

		for t in joueur.tirs:
			t.update()

		# Destruction des objets
		asteroides_detruits = []
		lasers_perdus = []
		for t in joueur.tirs:
			for a in asteroides:
				if pygame.sprite.collide_mask(a,t) != None:
					# Collision astéroïde/laser
					asteroides_detruits.append(a)
					lasers_perdus.append(t)
			if (t.x < 0 or t.x > XMAX
			 or t.y < 0 or t.y > YMAX):
				# Sortie de l'écran d'un laser
				lasers_perdus.append(t)

		# Suppression des objets détruits
		for a in asteroides_detruits:
			asteroides.remove(a)
		for t in lasers_perdus:
			joueur.tirs.remove(t)

		# Défaite si collision avec un astéroïde
		for a in asteroides:
			if pygame.sprite.collide_mask(a,joueur) != None:
				print ("Game over !")
				quit()

		# Victoire s'il n'y a plus d'astétoïdes
		if not asteroides:
			print ("Victoire !")
			quit()

		# DESSIN
		# Nettoyage de la fenêtre
		fenetre.fill(black)

		# Tracé du joueur
		fenetre.blit(joueur.image, joueur.rect)

		# Tracé des lasers
		for t in joueur.tirs:
			fenetre.blit(t.image, t.rect)

		# Tracé des astéroïdes
		for a in asteroides:
			fenetre.blit(a.image, a.rect)

		# Mise à jour de l'écran
		pygame.display.update()
		# Attente pour atteindre 30 IPS
		horloge.tick(30)


# Initialisation du module PyGame
pygame.init()

# Lancement du jeu
main()
