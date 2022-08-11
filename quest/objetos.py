import os
import random

import pygame as pg
from pygame.sprite import Sprite

from . import ANCHO_P, ALTO_P, COLOR_TEXTO2, FPS


class Nave(Sprite):
    margen_lateral = 20
    velocidad = 5
    #perder_vida = False
    #colision = False

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join(
            "resources", "images", "spaceship.png"))
        self.rect = self.image.get_rect()
        self.rect.centery = ALTO_P/2
        self.rect.x = self.margen_lateral

    def ha_colisionado(self, otro, otro2):
        if self.rect.colliderect(otro):
            self.colision = True
        if self.rect.colliderect(otro2):
            self.colision = True

    def update(self):
        "Estos son los controles que permiten mover la nave"
        tecla_mov = pg.key.get_pressed()
        if tecla_mov[pg.K_UP]:
            self.rect.y -= self.velocidad
            if self.rect.top < 0:
                self.rect.y = 0
        if tecla_mov[pg.K_DOWN]:
            self.rect.y += self.velocidad
            if self.rect.bottom > ALTO_P:
                self.rect.bottom = ALTO_P
        if self.ha_colisionado:
            self.perder_vida = True


class Meteorito(Sprite):
    def __init__(self):
        super().__init__()
        self.w = 128
        self.h = 128
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_P - self.rect.width
        self.rect.y = random.randrange(ALTO_P-self.rect.height)

        # Almacenar los frames
        self.imagenes = []
        self.contador = 0
        self.tiempo_animacion = FPS // 4
        self.momento_actual = 0
        self.cargarFrames()

    def cargarFrames(self):
        """Este método sirve para cargar las imágenes que harán el efecto de que
        el meteorito gire sobre sí mismo al desplazarse"""

        sprite_sheet = pg.image.load(os.path.join(
            "resources", "images", "asteroids.png"))

        """Esta parte del código recorre el sprite sheet y almacena cada
        fotograma en una variable en forma de lista para preparar la animación"""
        for fila in range(4):
            y = fila * self.h
            for columna in range(8):
                x = columna * self.w
                image = pg.Surface((self.w, self.h), pg.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x, y, self.w, self.h))
                self.imagenes.append(image)

                self.siguiente_imagen = 0
                self.siguiente_imagen = len(self.imagenes)
                self.image = self.imagenes[self.contador]

    def update(self):
        # para animar los frames de la imagen del meteorito
        self.momento_actual += self.tiempo_animacion
        if self.momento_actual == FPS:
            self.momento_actual = 0
            self.contador += 1

            if self.contador >= self.siguiente_imagen:
                self.contador = 0

            self.image = self.imagenes[self.contador]

        # controla la velocidad del meteorito
        self.velocidad_x = random.randrange(3, 5)
        self.rect.x -= self.velocidad_x

        # controla que el meteorito no se salga por abajo(un margen) y por arriba
        if self.rect.bottom == ALTO_P:
            self.rect.y = ALTO_P
        if self.rect.top == 0:
            self.rect.y = 0


class MeteoritoMediano(Sprite):
    def __init__(self):
        super().__init__()
        self.w = 96
        self.h = 96
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_P - self.rect.width
        self.rect.y = random.randrange(ALTO_P-self.rect.height)

        # Almacenar los frames
        self.imagenes = []
        self.contador = 0
        self.tiempo_animacion = FPS // 3
        self.momento_actual = 0
        self.cargarFrames()

    def cargarFrames(self):

        sprite_sheet = pg.image.load(os.path.join(
            "resources", "images", "asteroids_medium.png"))

        for fila in range(5, 8):
            y = fila * self.h
            for columna in range(8):
                x = columna * self.w
                image = pg.Surface((self.w, self.h), pg.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x, y, self.w, self.h))
                self.imagenes.append(image)

        self.imagenes_cargadas = 0
        self.imagenes_cargadas = len(self.imagenes)
        self.image = self.imagenes[self.contador]

    def update(self):
        self.momento_actual += self.tiempo_animacion
        if self.momento_actual > FPS:
            self.momento_actual = 0
            self.contador += 1

            if self.contador >= self.imagenes_cargadas:
                self.contador = 0

            self.image = self.imagenes[self.contador]

        self.velocidad_x = random.randrange(3, 7)
        self.rect.x -= self.velocidad_x

        if self.rect.bottom == ALTO_P:
            self.rect.y = ALTO_P
        if self.rect.top == 0:
            self.rect.top += 150



class MeteoritoPequenio(Meteorito):
    "Clase a construir o eliminar (NO ACTIVA)"

    def __init__(self):
        super().__init__()
        self.w = 41.5
        self.h = 50

        # Cambio del tiempo de animación según la clase padre Meteorito
        self.animation_time = FPS // 2
        self.loadFrames()

    def loadFrames(self):

        sprite_sheet = pg.image.load(os.path.join(
            "resources", "images", "asteroids_usmall.png"))

        for fila in range(5):
            y = fila * self.h
            for columna in range(6):
                x = columna * self.w
                image = pg.Surface((self.w, self.h), pg.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x, y, self.w, self.h))
                self.imagenes.append(image)

        self.how_many = len(self.imagenes)
        self.image = self.imagenes[self.index]

    def update(self):
        self.current_time += self.animation_time
        if self.current_time > FPS:
            self.current_time = 0
            self.index += 1

            if self.index >= self.how_many:
                self.index = 0

            self.image = self.imagenes[self.index]

        self.velocidad_x = random.randrange(5, 9)
        self.rect.x -= self.velocidad_x

        if self.rect.bottom == ALTO_P:
            self.rect.y = ALTO_P - 100
        if self.rect.top == 0:
            self.rect.top = 0
# clase a construir o a eliminar


class Explosion(Sprite):
    "Clase a construir (ACTIVA PERO MEJORABLE)"

    def __init__(self, centro):
        super().__init__()
        self.w = 100
        self.h = 100
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = centro

        # Almacenar los frames
        self.imagenes = []
        self.contador = 0
        self.tiempo_animacion = FPS // 2

        self.act_tiempo = pg.time.get_ticks()
        self.cargarFrames()

    def cargarFrames(self):

        sprite_sheet = pg.image.load(os.path.join(
            "resources", "images", "imagen_explosiones.png"))

        for fila in range(6):
            y = fila * self.h
            for columna in range(6):
                x = columna * self.w
                image = pg.Surface((self.w, self.h), pg.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x, y, self.w, self.h))
                self.imagenes.append(image)

        self.image = self.imagenes[self.contador]

    def update(self):
        """Aquí se ha usado un modo distinto para animar, para probar un nuevo
        sistema de funcionamiento. Nos basamos en los ticks del juego"""
        ahora = pg.time.get_ticks()
        if ahora - self.act_tiempo > self.tiempo_animacion:
            self.contador += 1
            self.act_tiempo = ahora
            if self.contador == len(self.imagenes):
                self.kill()
            
            else:
                self.image = self.imagenes[self.contador]
                
            
class ContadorVidas:
    def __init__(self, vidas_iniciales):
        self.vidas = vidas_iniciales
        font_file = os.path.join("resources", "fonts",
                                 "sans_serif_plus_7.ttf")
        self.tipografia = pg.font.Font(font_file, 20)

    def perder_vida(self):
        self.vidas -= 1
        return self.vidas < 1

    def pintar_marcador_vidas(self,pantalla):
        texto_marcador_vidas = f"Vidas: {self.vidas}"
        texto = self.tipografia.render(str(texto_marcador_vidas),True,COLOR_TEXTO2)
        pos_x = texto.get_width()
        pos_y = texto.get_height() + 20
        pg.surface.Surface.blit(pantalla,texto,(pos_x-60,pos_y))