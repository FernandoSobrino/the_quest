import os
import pygame as pg
import random

from . import ANCHO_P, ALTO_P, COLOR_TEXTO, COLOR_TEXTO2, FPS

from .objetos import Nave, Meteorito, Explosion


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
        self.tipo_juego = pg.font.Font(font_file2, 30)
        self.tipo_info = pg.font.Font(font_file2, 20)

    def bucle_principal(self):
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
            self.pintar_fondo()
            self.pintar_texto_titulo()
            self.pintar_texto_instrucciones()
            self.pintar_texto_partida()
            pg.display.flip()

    def pintar_fondo(self):
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo1.jpg")).convert()
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_texto_instrucciones(self):

        posiciones = [325, 400, 450, 500]
        mensajes = ["Como jugar:", "- Pulsa ARRIBA/ABAJO para mover la nave.",
                    "- Esquiva los meteoritos para ganar puntos.", "- Tienes 3 vidas. "
                    "Pierdes vidas si chocas con los meteoritos."]

        pos_x = ANCHO_P - 800
        conta_posiciones = 0

        for mensaje in mensajes:
            texto_render = self.tipo_info.render(
                (mensaje), True, COLOR_TEXTO)
            self.pantalla.blit(
                texto_render, (pos_x, posiciones[conta_posiciones]))
            conta_posiciones += 1

    def pintar_texto_partida(self):
        mensaje = "Pulsa 'ESPACIO' para comenzar la partida"
        texto = self.tipo_juego.render(mensaje, True, COLOR_TEXTO2)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = ALTO_P - 75
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_texto_titulo(self):
        mensaje = "THE QUEST"
        texto = self.tipografia.render(mensaje, True, COLOR_TEXTO2)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = ALTO_P/8
        self.pantalla.blit(texto, (pos_x, pos_y))


class PantallaJuego(Pantalla):

    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        self.player = Nave()
        self.crear_meteoritos()

    def bucle_principal(self):
        salir = False
        while not salir:
            self.reloj.tick(FPS)
            tiempo_fps = self.reloj.get_fps()
            print(tiempo_fps)
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

            # Colisión de la nave con meteorito y aparece explosion
            self.hit = pg.sprite.spritecollide(
                self.player, self.meteoritos, True)
            
            if self.hit:
                self.explosion = Explosion()
                self.pantalla.blit(self.explosion.image,self.player.rect)
            

            #Para sacar meteoritos del grupo una vez llegan al final de la pantalla
            self.regenerar_meteoritos()

            # Instanciar nuevos meteoritos cuando se acaben
            if len(self.meteoritos.sprites()) == 0:
                self.crear_meteoritos()


            pg.display.flip()

    def pintar_fondo(self):
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "espacio.jpeg")).convert()
        self.pantalla.blit(self.fondo, (0, 0))


    def crear_meteoritos(self):
        self.meteoritos = pg.sprite.Group()
        self.meteoritos.empty()
        margen_y = 40
        cantidad_meteoritos = random.randrange(4)

        for i in range(cantidad_meteoritos):
            self.meteorito = Meteorito()
            self.meteorito.rect.y -= margen_y
            self.meteorito.rect.y = random.randrange(ALTO_P - self.meteorito.rect.height)
            self.meteoritos.add(self.meteorito)
            
    
    def regenerar_meteoritos(self):
        if self.meteorito.rect.right < 0:
            self.meteorito.kill()
        if not self.meteorito.alive():
            self.crear_meteoritos()
            
        
