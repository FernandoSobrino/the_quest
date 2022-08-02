import os
import random

import pygame as pg
from pygame.sprite import Sprite

from . import ANCHO_P, ALTO_P, FPS


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


class Meteorito(Sprite):
    def __init__(self):
        super().__init__()
        self.w = 128
        self.h = 128
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_P - self.rect.width
        self.rect.y = random.randrange(ALTO_P-self.rect.height)
        if self.rect.bottom == ALTO_P:
            self.rect.y = ALTO_P - 100
        if self.rect.top == 0:
            self.rect.top = 0

        # Almacenar los frames
        self.frames = []
        self.index = 0
        self.how_many = 0
        self.animation_time = FPS // 2

        self.current_time = 0

    def loadFrames(self):

        sprite_sheet = pg.image.load(os.path.join(
            "resources", "images", "asteroids.png"))

        for fila in range(4):
            y = fila * self.h
            for columna in range(8):
                x = columna * self.w
                image = pg.Surface((self.w, self.h), pg.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x, y, self.w, self.h))
                self.frames.append(image)

        self.how_many = len(self.frames)
        self.image = self.frames[self.index]

    def animarFrames(self):
        self.current_time += self.animation_time
        if self.current_time > FPS:
            self.current_time = 0
            self.index += 1

            if self.index >= self.how_many:
                self.index = 0

            self.image = self.frames[self.index]

    def update(self):
        self.loadFrames()
        self.animarFrames()

        self.velocidad_x = random.randrange(1, 4)
        self.rect.x -= self.velocidad_x

        if self.rect.right < 0:
            self.rect.x = ANCHO_P
            self.rect.y = random.randrange(ALTO_P - self.rect.height)
            self.rect.x -= self.rect.width

        


class MeteoritoMediano(Sprite):
    def __init__(self):
        super().__init__()
        self.w = 96
        self.h = 96
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_P - self.rect.width
        self.rect.y = random.randrange(ALTO_P-self.rect.height)
        if self.rect.bottom == ALTO_P:
            self.rect.y = ALTO_P - 100
        if self.rect.top == 0:
            self.rect.top = 0

        # Almacenar los frames
        self.frames = []
        self.index = 0
        self.how_many = 0
        self.animation_time = FPS // 3

        self.current_time = 0

    def loadFrames(self):

        sprite_sheet = pg.image.load(os.path.join(
            "resources", "images", "asteroids_medium.png"))

        for fila in range(5, 8):
            y = fila * self.h
            for columna in range(8):
                x = columna * self.w
                image = pg.Surface((self.w, self.h), pg.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x, y, self.w, self.h))
                self.frames.append(image)

        self.how_many = len(self.frames)
        self.image = self.frames[self.index]

    def animarFrames(self):
        self.current_time += self.animation_time
        if self.current_time > FPS:
            self.current_time = 0
            self.index += 1

            if self.index >= self.how_many:
                self.index = 0

            self.image = self.frames[self.index]

    def update(self):
        self.loadFrames()
        self.animarFrames()

        self.velocidad_x = random.randrange(3, 6)
        self.rect.x -= self.velocidad_x

        if self.rect.right < 0:
            self.rect.x = ANCHO_P
            self.rect.y = random.randrange(ALTO_P - self.rect.height)
            self.rect.x -= self.rect.width

        


class MeteoritoPequenio(Sprite):
    def __init__(self):
        super().__init__()
        self.w = 41.5
        self.h = 50
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_P - self.rect.width
        self.rect.y = random.randrange(ALTO_P-self.rect.height)
        if self.rect.bottom == ALTO_P:
            self.rect.y = ALTO_P - 100
        if self.rect.top == 0:
            self.rect.top = 0

        # Almacenar los frames
        self.frames = []
        self.index = 0
        self.how_many = 0
        self.animation_time = FPS // 4

        self.current_time = 0

    def loadFrames(self):

        sprite_sheet = pg.image.load(os.path.join(
            "resources", "images", "asteroids_usmall.png"))

        for fila in range(5):
            y = fila * self.h
            for columna in range(6):
                x = columna * self.w
                image = pg.Surface((self.w, self.h), pg.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x, y, self.w, self.h))
                self.frames.append(image)

        self.how_many = len(self.frames)
        self.image = self.frames[self.index]

    def animarFrames(self):
        self.current_time += self.animation_time
        if self.current_time > FPS:
            self.current_time = 0
            self.index += 1

            if self.index >= self.how_many:
                self.index = 0

            self.image = self.frames[self.index]

    def update(self):
        self.loadFrames()
        self.animarFrames()

        self.velocidad_x = random.randrange(7, 10)
        self.rect.x -= self.velocidad_x

        if self.rect.right < 0:
            self.rect.x = ANCHO_P
            self.rect.x -= self.rect.width
            self.rect.y = random.randrange(ALTO_P - self.rect.height)

        
