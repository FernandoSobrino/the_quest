import os
import pygame as pg
import random

from . import ANCHO_P, ALTO_P, COLOR_TEXTO, COLOR_TEXTO2, FPS, VIDAS

from .objetos import MeteoritoMediano, Nave, Meteorito, Explosion, ContadorVidas


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
            "resources", "images", "fondo_intro.jpg")).convert()
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_texto_instrucciones(self):

        posiciones = [325, 400, 450, 500, 550]
        mensajes = ["Como jugar:", "- Pulsa ARRIBA/ABAJO para mover la nave.",
                    "- Esquiva los meteoritos para ganar puntos.", "- Tienes 3 vidas. "
                    "Pierdes vidas si chocas con los meteoritos.",
                    "- Aguanta el tiempo suficiente para aterrizar en el planeta."]

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
        self.meteoritos = pg.sprite.Group()
        self.explosiones = pg.sprite.Group()
        self.contador_vidas = ContadorVidas(VIDAS)
        self.crear_meteoritos()
        self.crear_meteoritos_m()
        self.exp_sound = pg.mixer.Sound(os.path.join(
            "resources", "sounds", "explosion_larga.wav"))

    def bucle_principal(self):
        salir = False
        while not salir:
            self.reloj.tick(FPS)
            tiempo_fps = self.reloj.get_fps()
            # print(tiempo_fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True

            self.pintar_fondo()

            #Pintar el marcador de vidas
            self.contador_vidas.pintar_marcador_vidas(self.pantalla)

            # Para mover y pintar la nave
            self.pantalla.blit(self.player.image, self.player.rect)
            self.player.update()

            # Para dibujar y actualizar el grupo de meteoritos
            self.meteoritos.draw(self.pantalla)
            self.meteoritos.update()

            self.explosiones.draw(self.pantalla)
            self.explosiones.update()

            # Colisión de la nave con meteorito y aparece explosion (efecto y sonido)
            colision = pg.sprite.spritecollide(
                self.player, self.meteoritos, True)
            if colision:
                self.contador_vidas.perder_vida()
                #self.player.ha_colisionado(self.meteorito, self.meteorito_m)
                self.explosion = Explosion(self.player.rect.center)
                self.exp_sound.play()
                self.explosiones.add(self.explosion)

            # Para sacar meteoritos del grupo una vez llegan al final de la pantalla y vuelve a crearlos
            self.regenerar_meteoritos()
            self.regenerar_meteoritos_m()

            # Recarga de todos los elementos que funcionan en el juego
            pg.display.flip()

            if self.contador_vidas.vidas == 0:
                salir = True
        
            
    def pintar_fondo(self):
        "Este método pinta el fondo de estrellas de la pantalla del juego"
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo_nivel.jpeg")).convert()
        self.pantalla.blit(self.fondo, (0, 0))

    def crear_meteoritos(self):
        """"Este método genera los meteoritos grandes al inicio de la partida y
        es llamado de nuevo desde el método regenerar las veces que el meteorito finaliza su ciclo de vida"""""
        cantidad_meteoritos = random.randrange(1, 3)
        for i in range(cantidad_meteoritos):
            self.meteorito = Meteorito()
            self.meteoritos.add(self.meteorito)

    def crear_meteoritos_m(self):
        """"Este método genera los meteoritos medianos al inicio de la partida y
        es llamado de nuevo desde el método regenerar las veces que el meteorito finaliza su ciclo de vida"""""
        cantidad_meteoritos = random.randrange(2, 5)
        for i in range(cantidad_meteoritos):
            self.meteorito_m = MeteoritoMediano()
            self.meteoritos.add(self.meteorito_m)

    def regenerar_meteoritos(self):
        """"El método saca el meteorito grande del grupo de sprites y regenera
        de nuevo los meteoritos si ya no quedan en el grupo (a mejorar)"""""
        if self.meteorito.rect.right < 0:
            self.meteoritos.remove(self.meteorito)
        if not self.meteorito.alive():
            self.crear_meteoritos()

    def regenerar_meteoritos_m(self):
        """"El método saca el meteorito mediano del grupo de sprites y regenera
        de nuevo los meteoritos si ya no quedan en el grupo (a mejorar)"""""
        if self.meteorito_m.rect.right < 0:
            self.meteoritos.remove(self.meteorito_m)
        if not self.meteorito_m.alive():
            self.crear_meteoritos_m()



