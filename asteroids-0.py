#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Implémentation du jeu Asteroids : version initiale (fenêtre pyGame).
# Copyright (C) 2020-2021 - Jérôme Kirman (Palais de la Découverte)
# Ce programme est un logiciel libre ; voir les fichiers README.md et LICENSE.

# Modules requis
import sys

import pygame
from pygame.locals import *

# Taille de la fenêtre
XMAX, YMAX = 800, 600

# Corps du jeu
pygame.init()

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

	# Mise à jour de l'écran
	pygame.display.update()

	# Attente pour atteindre 30 IPS
	horloge.tick(30)
