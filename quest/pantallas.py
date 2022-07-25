import os
import pygame as pg

from quest import ANCHO_P, ALTO_P, COLOR_AMARILLO

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
        self.reloj.tick(60)
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
        self.crear_meteoritos()
        

    def bucle_principal(self):
        self.reloj.tick(60)
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True

            self.pintar_fondo()
            

            # Para mover y pintar la nave
            self.player.update()
            self.pantalla.blit(self.player.image, self.player.rect)
            self.meteoritos.update()
            self.meteoritos.draw(self.pantalla)
            
            pg.display.flip()

    def pintar_fondo(self):
        self.pantalla.blit(self.fondo, (0, 0))


    def crear_meteoritos(self):
        self.meteoritos = pg.sprite.Group()
        for x in range(10):
            self.meteorito = Asteroide()
            self.meteoritos.add(self.meteorito)

    
        
        


        

