import os
import random

import pygame as pg
from pygame.sprite import Sprite

from . import ANCHO_P, ALTO_P, COLOR_TEXTO2, FPS, MARGEN_LATERAL, POS_PLANETA, PUNTOS_PARTIDA


class Nave(Sprite):
    velocidad_mover = 5
    velocidad_aterrizar = 1

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join(
            "resources", "images", "spaceship.png"))
        self.rect = self.image.get_rect()
        self.rect.y = ALTO_P/2
        self.rect.x = MARGEN_LATERAL
        self.angulo = 0
        self.nave_escondida = False
        self.nave_aterrizando = False
        self.rotacion = False
        self.fin_rotacion = False

    def esconder_nave(self):
        """Este método permite posicionar la nave en un punto lejano de la pantalla tras morir
        para simular un refresco (1ª versión)"""
        self.tiempo_renacer = pg.time.get_ticks()/1000
        self.nave_escondida = True
        self.rect.y = -1000

    def aterrizar_nave(self, aterrizando, pantalla):
        """Este método hace las maniobras de aterrizaje de la nave"""
        self.nave_aterrizando = aterrizando
        if aterrizando:
            self.rect.x += self.velocidad_aterrizar
            if self.rect.y > (ALTO_P - self.rect.height)/2:
                self.rect.y -= self.velocidad_aterrizar
            else:
                self.rect.y += self.velocidad_aterrizar

            if self.rect.x > ANCHO_P/2 + 30:
                self.rect.x = ANCHO_P/2 + 30
                self.rotacion = True

                # self.centro_original = self.image.get_rect(
                # topleft=(self.rect.x,self.rect.y)).center
                if self.angulo == 180:
                    self.rotacion = False
                    self.fin_rotacion = True
                    img_rotada2 = pg.transform.rotate(self.image, 180)
                    rect_rotado2 = img_rotada2.get_rect(
                        center=self.rect.center)
                    pantalla.blit(img_rotada2, rect_rotado2)

                if self.rotacion:
                    self.angulo += 2
                    img_rotada = pg.transform.rotate(self.image, self.angulo)
                    #rect_rotado = img_rotada.get_rect(center=self.centro_original)
                    rect_rotado = img_rotada.get_rect(center=self.rect.center)
                    pantalla.blit(img_rotada, rect_rotado)

            else:
                pantalla.blit(self.image, self.rect)

    def mover_nave(self, aterrizando):
        "Estos son los controles que permiten mover la nave"
        tecla_mov = pg.key.get_pressed()
        if not aterrizando:
            if tecla_mov[pg.K_UP]:
                self.rect.y -= self.velocidad_mover
                if self.rect.top < 0:
                    self.rect.y = 0
            if tecla_mov[pg.K_DOWN]:
                self.rect.y += self.velocidad_mover
                if self.rect.bottom > ALTO_P:
                    self.rect.bottom = ALTO_P

    def update(self):
        """El método incluye el movimiento de la nave + la aparición de la nave
           en su punto original tras perder una vida"""

        self.mover_nave(self.nave_aterrizando)

        # Esta parte del código permite devolver la nave a su punto original pasado un tiempo
        # tras perder una vida
        if self.nave_escondida and pg.time.get_ticks()/1000 - self.tiempo_renacer > 1.5:
            self.nave_escondida = False
            self.rect.centery = ALTO_P/2
            self.rect.x = MARGEN_LATERAL


class Meteorito(Sprite):
    """Superclase Meteorito"""
    puntuacion = PUNTOS_PARTIDA

    def __init__(self, puntuacion):
        super().__init__()
        self.puntos = puntuacion
        self.w = 128
        self.h = 128
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.plantilla_imagenes = pg.image.load(os.path.join(
            "resources", "images", "asteroids.png"))
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_P - self.rect.width
        self.rect.y = random.randrange(ALTO_P-self.rect.height)
        self.velocidad_x = random.randint(3, 8)

        # Código para almacenar los frames del sprite sheet en una lista
        self.imagenes = []
        self.contador = 0
        self.tiempo_animacion = FPS // 4
        self.momento_actual = 0
        self.cargarFrames(self.plantilla_imagenes)

    def cargarFrames(self, sprite_sheet):
        """Esta parte del código recorre el sprite sheet y almacena cada
        fotograma en una lista para preparar la animación"""
        for fila in range(4):
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
        # para animar los frames de la imagen del meteorito
        self.momento_actual += self.tiempo_animacion
        if self.momento_actual == FPS:
            self.momento_actual = 0
            self.contador += 1

            if self.contador >= self.imagenes_cargadas:
                self.contador = 0

            self.image = self.imagenes[self.contador]

        # controla la velocidad del meteorito
        self.rect.x -= self.velocidad_x

        # controla que el meteorito no se salga por abajo y por arriba
        if self.rect.bottom == ALTO_P:
            self.rect.y = ALTO_P
        if self.rect.top == 0:
            self.rect.y += 150


class MeteoritoMediano(Meteorito):
    """Subclase. Sólo conserva aquellos atributos que difieren de la superclase
    Meteorito"""""

    def __init__(self, puntuacion):
        super().__init__(puntuacion)
        self.w = 96
        self.h = 96
        self.velocidad_x = random.randint(4, 10)
        self.plantilla_imagenes = pg.image.load(os.path.join(
            "resources", "images", "asteroids_medium.png"))

        # Para almacenar los frames del sprite sheet del meteorito mediano
        self.imagenes = []
        self.tiempo_animacion = FPS // 3
        self.cargarFrames(self.plantilla_imagenes)


class Planeta(Sprite):
    velocidad_x = 1

    def __init__(self):
        self.image = pg.image.load(os.path.join("resources", "images",
                                                "planeta1.png"))
        self.rect = self.image.get_rect()
        self.rect.x = POS_PLANETA
        self.rect.y = (ALTO_P-self.image.get_height())/2

    def mover_planeta(self, nave_aterrizando):
        if nave_aterrizando:
            self.rect.x -= self.velocidad_x
            if self.rect.x < ANCHO_P - self.rect.height:
                self.rect.x = ANCHO_P - self.rect.height


class Explosion(Sprite):
    "Clase que pinta las explosiones de la nave cuando choca con los meteoritos"

    def __init__(self, centro):
        super().__init__()
        self.w = 100
        self.h = 100
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = centro

        # Almacena las imágenes del sprite sheet y se establecen los atributos de animación
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
        sistema de funcionamiento. Nos basamos en los ticks del juego y en el método kill
        para reiniciar la secuencia de imágenes de la explosión"""
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

    def pintar_marcador_vidas(self, pantalla):
        texto_marcador_vidas = f"Vidas: {self.vidas}"
        texto = self.tipografia.render(
            str(texto_marcador_vidas), True, COLOR_TEXTO2)
        pos_x = texto.get_width() - 60
        pos_y = texto.get_height() + 20
        pg.surface.Surface.blit(pantalla, texto, (pos_x, pos_y))


class Marcador:
    def __init__(self):
        self.valor = 0
        font_file = os.path.join("resources", "fonts", "sans_serif_plus_7.ttf")
        self.tipografia = pg.font.Font(font_file, 20)

    def aumentar(self, puntos):
        self.valor += puntos

    def pintar_marcador(self, pantalla):
        texto_marcador = f"Puntos: {self.valor}"
        texto = self.tipografia.render(str(texto_marcador), True, COLOR_TEXTO2)
        pos_x = texto.get_width() - 72
        pos_y = ALTO_P - texto.get_height() - 30
        pg.surface.Surface.blit(pantalla, texto, (pos_x, pos_y))


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

        self.velocidad_x = random.randint(5, 9)
        self.rect.x -= self.velocidad_x

        if self.rect.bottom == ALTO_P:
            self.rect.y = ALTO_P - 100
        if self.rect.top == 0:
            self.rect.top = 0
