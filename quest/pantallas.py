import os
import pygame as pg
import random

from . import ANCHO_P, ALTO_P, COLOR_AMARILLO, FPS

from .objetos import MeteoritoMediano, Nave, Meteorito, MeteoritoPequenio


class Pantalla:
    def __init__(self, pantalla: pg.Surface):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        pass


class PantallaPrincipal(Pantalla):
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        font_file = os.path.join("resources", "fonts",
                                 "light_sans_serif_7.ttf")
        font_file2 = os.path.join("resources", "fonts",
                                  "game_sans_serif_7.ttf")
        self.tipografia = pg.font.Font(font_file, 100)
        self.tipo_titulo = pg.font.Font(font_file2, 30)

    def bucle_principal(self):
        self.reloj.tick(FPS)
        # pg.mixer.music.play()
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    # pg.mixer.music.stop()
                    salir = True
                if event.type == pg.QUIT:
                    pg.quit()
            self.pantalla.fill((0, 0, 0))
            self.pintar_texto_titulo()
            self.pintar_texto_partida()
            self.pintar_texto_instrucciones()
            pg.display.flip()

    def pintar_texto_titulo(self):
        mensaje = "THE QUEST"
        texto = self.tipografia.render(mensaje, True, COLOR_AMARILLO)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = ALTO_P/8
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_texto_partida(self):
        mensaje = "Pulsa 'ESPACIO' para comenzar la partida"
        texto = self.tipo_titulo.render(mensaje, True, COLOR_AMARILLO)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = ALTO_P - 75
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_texto_instrucciones(self):
        mensaje = "Como jugar:"
        mensaje2 = "- Pulsa ARRIBA/ABAJO para mover la nave"
        mensaje3 = "- Esquiva los meteoritos para ganar puntos"
        mensaje4 = "- Tienes 3 vidas. Pierdes vidas si chocas con los meteoritos"
        texto = self.tipo_titulo.render(mensaje, True, COLOR_AMARILLO)
        texto2 = self.tipo_titulo.render(mensaje2, True, COLOR_AMARILLO)
        texto3 = self.tipo_titulo.render(mensaje3, True, COLOR_AMARILLO)
        texto4 = self.tipo_titulo.render(mensaje4, True, COLOR_AMARILLO)
        ancho_texto = texto.get_width()
        ancho_texto2 = texto2.get_width()
        ancho_texto3 = texto3.get_width()
        ancho_texto4 = texto4.get_width()
        pos_x = (ANCHO_P - ancho_texto)/3
        pos_x2 = (ANCHO_P - ancho_texto2)/3
        pos_x3 = (ANCHO_P - ancho_texto3)/3
        pos_x4 = (ANCHO_P - ancho_texto4)/3
        pos_y = ALTO_P - 400
        pos_y_2 = ALTO_P - 350
        pos_y_3 = ALTO_P - 300
        pos_y_4 = ALTO_P - 250
        self.pantalla.blit(texto, (pos_x, pos_y))
        self.pantalla.blit(texto2, (pos_x2, pos_y_2))
        self.pantalla.blit(texto3, (pos_x3, pos_y_3))
        self.pantalla.blit(texto4, (pos_x4, pos_y_4))


class PantallaJuego(Pantalla):

    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        self.player = Nave()
        self.crear_meteoritos()

    def bucle_principal(self):
        self.reloj.tick(FPS)
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True

            self.pintar_fondo()

            # Para mover y pintar la nave
            self.pantalla.blit(self.player.image, self.player.rect)
            self.player.update()

            # Para actualizar y dibujar el meteorito
            self.meteoritos.draw(self.pantalla)
            self.meteoritos.update()

            # Camino futuro para la colisión de nave con meteorito
            """
            self.hit = pg.sprite.spritecollide(
                self.player, self.meteoritos, False)
            if self.hit:
                self.player.image.set_alpha(0)
            """

            pg.display.flip()

    def pintar_fondo(self):
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "espacio.jpeg")).convert()
        self.pantalla.blit(self.fondo, (0, 0))

    def crear_meteoritos(self):
        self.meteoritos = pg.sprite.Group()
        self.meteoritos.empty()
        margen_y = 40

        for i in range(1):
            self.meteorito = Meteorito()
            self.meteorito.rect.y -= margen_y
            self.meteoritos.add(self.meteorito)
        for i in range(2):
            self.meteorito_mediano = MeteoritoMediano()
            self.meteorito.rect.y -= margen_y
            self.meteoritos.add(self.meteorito_mediano)
        for i in range(4):
            self.meteorito_pequenio = MeteoritoPequenio()
            self.meteorito.rect.y -= margen_y
            self.meteoritos.add(self.meteorito_pequenio)
