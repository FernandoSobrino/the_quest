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


class Asteroide(Sprite):
    def __init__(self):
        super().__init__()
        self.w = 128
        self.h = 128
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_P - self.rect.width
        self.rect.y = random.randrange(ALTO_P-self.rect.height)

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

        
    
    def tamaño_frames(self):
        self.img_aleatoria = random.randrange(3)
        if self.img_aleatoria == 0:
            self.image = pg.transform.scale((self.image).convert(), (100, 100))
        if self.img_aleatoria == 1:
            self.image = pg.transform.scale(
                (self.image).convert(), (50, 50))
        if self.img_aleatoria == 2:
            self.image = pg.transform.scale(
                (self.image).convert(), (25, 25))
        


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
        self.tamaño_frames()
        self.animarFrames()
        
        
        self.velocidad_x = random.randrange(6, 10)
        self.rect.x -= self.velocidad_x

        if self.rect.right < 0:
            self.rect.x = ANCHO_P - self.rect.width
            self.rect.y = random.randrange(ALTO_P - self.rect.height)
            self.rect.x -= self.rect.width

        if self.rect.y > ALTO_P:
            self.rect.y = ALTO_P - 30
        if self.rect.y < 0:
            self.rect.y = 0

        

        # Comentado, primera solución que tuve para hacer meteoritos de diferentes tamaños: no funciona
        """
        self.imagen_aleatoria = random.randrange(3)
        if self.imagen_aleatoria == 0:
            pg.transform.scale(self.image,(100,100))
            self.radius = 25
        if self.imagen_aleatoria == 1:
            pg.transform.scale(self.image,(50,50))
            self.radius = 12.5
        if self.imagen_aleatoria == 2:
            pg.transform.scale(self.image, (25, 25))
            self.radius = 7
        """
