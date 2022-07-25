import os
import random
import pygame as pg
from pygame.sprite import Sprite

from . import ANCHO_P, ALTO_P, TIEMPO_LASER_JUGADOR


class Nave(Sprite):
    margen_lateral = 20
    velocidad = 5

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join(
            "resources", "images", "spaceship.png"))
        self.rect = self.image.get_rect()
        self.rect.centery = ALTO_P/2
        self.rect.x = self.margen_lateral

    def update(self):
        tecla_mov = pg.key.get_pressed()
        if tecla_mov[pg.K_UP]:
            self.rect.y -= self.velocidad
            if self.rect.top < 0:
                self.rect.y = 0
        if tecla_mov[pg.K_DOWN]:
            self.rect.y += self.velocidad
            if self.rect.bottom > ALTO_P:
                self.rect.bottom = ALTO_P


class Asteroide(Sprite):
    def __init__(self):
        super().__init__()
        self.img_aleatoria = random.randrange(3)
        if self.img_aleatoria == 0:
            self.image = pg.transform.scale(
                pg.image.load(os.path.join(
                    "resources", "images", "asteroide.png")).convert(), (100, 100))
            self.radius = 50
        if self.img_aleatoria == 1:
            self.image = pg.transform.scale(
                pg.image.load(os.path.join(
                    "resources", "images", "asteroide.png")).convert(), (50, 50))
            self.radius = 25
        if self.img_aleatoria == 2:
            self.image = pg.transform.scale(
                pg.image.load(os.path.join(
                    "resources", "images", "asteroide.png")).convert(), (25, 25))
            self.radius = 12
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO_P - self.rect.width)
        self.rect.y = random.randrange(ALTO_P - self.rect.height)
        self.rect.x -= self.rect.width
        self.velocidad_x = random.randrange(4, 10)

    def update(self):
        self.rect.x -= self.velocidad_x
        if self.rect.left < 0:
            self.rect.x = random.randrange(ANCHO_P)
            self.rect.x -= self.rect.width

            self.velocidad_x = random.randrange(1, 10)
