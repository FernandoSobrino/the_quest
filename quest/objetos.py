import os

import pygame as pg
from pygame.sprite import Sprite

from . import ANCHO_P, ALTO_P, TIEMPO_LASER_JUGADOR


class Nave(Sprite):
    margen_lateral = 20
    velocidad = 5

    def __init__(self):
        super().__init__
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

       


