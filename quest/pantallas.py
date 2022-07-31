import os
import pygame as pg
import random

from quest import ANCHO_P, ALTO_P, COLOR_AMARILLO, FPS

from .objetos import Nave, Asteroide


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
            pg.display.flip()

    def pintar_texto_titulo(self):
        mensaje = "THE QUEST"
        texto = self.tipografia.render(mensaje, True, COLOR_AMARILLO)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = ALTO_P/4
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_texto_partida(self):
        mensaje = "Pulsa 'ESPACIO' para comenzar la partida"
        texto = self.tipo_titulo.render(mensaje, True, COLOR_AMARILLO)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = ALTO_P - 150
        self.pantalla.blit(texto, (pos_x, pos_y))


class PantallaJuego(Pantalla):

    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "espacio.jpeg"))
        self.player = Nave()
        self.meteoritos = pg.sprite.Group()

        generador_meteoritos = random.randrange(6)
        for x in range(generador_meteoritos):
            self.meteorito = Asteroide()
            self.meteoritos.add(self.meteorito)
        
        
    def bucle_principal(self):
        self.reloj.tick(FPS)
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True

            self.pintar_fondo()

            
            # Para mover y pintar la nave
            self.player.update()
            self.pantalla.blit(self.player.image, self.player.rect)
            self.meteoritos.draw(self.pantalla)
            self.meteoritos.update()
            # Para actualizar y dibujar el meteorito
            
            
            
            

            """
            self.hit = pg.sprite.spritecollide(
                self.player, self.meteoritos, False)
            if self.hit:
                self.player.image.set_alpha(0)
            """
            

            pg.display.flip()

    
    def pintar_fondo(self):
        self.pantalla.blit(self.fondo, (0, 0))


