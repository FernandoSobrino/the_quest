import os
import random

import pygame as pg

from . import ANCHO_P, ALTO_P, COLOR_TEXTO, COLOR_TEXTO2, FPS, VIDAS

from .objetos import ContadorVidas, Explosion, Marcador, Meteorito, MeteoritoMediano, Nave, Planeta


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

        # creación de la nave
        self.jugador = Nave()

        # creación de los meteoritos
        self.meteoritos = pg.sprite.Group()
        self.crear_meteoritos()
        self.crear_meteoritos_m()

        # creación del planeta
        self.planeta = Planeta()

        # creación de las explosiones
        self.explosiones = pg.sprite.Group()

        # creación del contador de vidas
        self.contador_vidas = ContadorVidas(VIDAS)

        # creación del marcador de puntos
        self.marcador = Marcador()

        # carga del sonido de la explosión
        self.exp_sound = pg.mixer.Sound(os.path.join(
            "resources", "sounds", "sonido_explosion.wav"))

        # carga de la música del juego
        self.musica = pg.mixer.music.load(os.path.join(
            "resources", "sounds", "musica_juego.mp3"))

    def bucle_principal(self):
        "Método que controla el juego"

        # Flags de salida del juego y de fase de aterrizaje
        salir = False
        aterrizaje = False

        # Reproducción de la música del juego (en bucle)
        pg.mixer.music.play(-1)

        while not salir:
            self.reloj.tick(FPS)
            """
            Parte comentada para pruebas: activa, mide los FPS por seg. para
            ver problemas de ejecución del juego
            """
            #tiempo_fps = self.reloj.get_fps()
            # print(tiempo_fps)

            # Condición para cerrar el juego si pulsamos la X de la ventana
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    salir = True

            # Para pintar el fondo del nivel
            self.pintar_fondo()

            # Para mover y pintar la nave y mover el planeta cuando la nave aterrice
            self.jugador.update()
            if not aterrizaje:
                self.pantalla.blit(self.jugador.image, self.jugador.rect)
            else:
                self.jugador.aterrizar_nave(aterrizaje, self.pantalla)
                self.planeta.mover_planeta(aterrizaje)

            # Para pintar el marcador de puntos
            self.marcador.pintar_marcador(self.pantalla)

            # Para dibujar y actualizar el grupo de meteoritos
            self.meteoritos.update()
            self.meteoritos.draw(self.pantalla)

            # Para dibujar el planeta
            self.pantalla.blit(self.planeta.image, self.planeta.rect)

            # Para dibujar y actualizar las explosiones
            self.explosiones.update()
            self.explosiones.draw(self.pantalla)

            # Para pintar el marcador de vidas
            self.contador_vidas.pintar_marcador_vidas(self.pantalla)

            # Colisión de la nave con meteorito, aparece explosion (efecto y sonido) y
            # desaparece la nave. También desactiva colisiones durante el aterrizaje
            if not aterrizaje:
                self.colision = pg.sprite.spritecollide(
                    self.jugador, self.meteoritos, True)

                if self.colision:
                    self.explosion = Explosion(self.jugador.rect.center)
                    self.explosiones.add(self.explosion)
                    self.jugador.esconder_nave()
                    self.exp_sound.play()
                    self.contador_vidas.perder_vida()

            # Para contar puntos por cada meteorito que se esquiva (no va bien - mejorable)
            if self.meteorito.rect.right < 0:
                self.marcador.aumentar(self.meteorito.puntos)
            if self.meteorito_m.rect.right < 0:
                self.marcador.aumentar(self.meteorito_m.puntos)

            # Para sacar meteoritos del grupo una vez llegan al final de la pantalla y vuelve a crearlos
            # if not aterrizaje: (a desarrollar)
            self.regenerar_meteoritos(aterrizaje)
            self.regenerar_meteoritos_m(aterrizaje)

            # Condición que activa el flag de aterrizaje
            if self.marcador.valor >= 200:
                aterrizaje = True

            # Actualización de todos los elementos que se están mostrando en la partida
            pg.display.flip()

            # Estas líneas de código sirven para cerrar el juego si se pierden todas las vidas
            if self.contador_vidas.vidas == 0:
                salir = True

    # -------------MÉTODOS DE FUNCIONAMIENTO INDEPENDIENTES DE LAS CLASES-----------#

    def pintar_fondo(self):
        "Este método pinta el fondo de estrellas de la pantalla del juego"
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo_nivel.jpeg")).convert()
        self.pantalla.blit(self.fondo, (0, 0))

    def crear_meteoritos(self):
        """"Este método genera los meteoritos grandes al inicio de la partida, les asigna puntuación y
        es llamado de nuevo desde el método regenerar las veces que el meteorito finaliza su ciclo de vida"""""
        cantidad_meteoritos = random.randint(1, 3)
        for i in range(cantidad_meteoritos):
            puntos = (i + 10) - i
            self.meteorito = Meteorito(puntos)
            self.meteoritos.add(self.meteorito)

    def regenerar_meteoritos(self, fin_viaje):
        """"El método saca el meteorito grande del grupo de sprites y regenera
        de nuevo los meteoritos si ya no quedan en el grupo"""""
        if not fin_viaje:
            if self.meteorito.rect.right < 0:
                self.meteoritos.remove(self.meteorito)
            if not self.meteorito.alive():
                self.crear_meteoritos()
        else:
            self.meteorito.kill()

    def crear_meteoritos_m(self):
        """"Este método genera los meteoritos medianos al inicio de la partida, les asigna puntuación
         y es llamado de nuevo desde el método regenerar las veces que el meteorito finaliza su ciclo de vida"""""
        cantidad_meteoritos_m = random.randint(2, 4)
        for i in range(cantidad_meteoritos_m):
            puntos_m = (i + 20) - i
            self.meteorito_m = MeteoritoMediano(puntos_m)
            self.meteoritos.add(self.meteorito_m)

    def regenerar_meteoritos_m(self, fin_viaje):
        """"El método saca el meteorito mediano del grupo de sprites y regenera
        de nuevo los meteoritos si ya no quedan en el grupo"""""
        if not fin_viaje:
            if self.meteorito_m.rect.right < 0:
                self.meteoritos.remove(self.meteorito_m)
            if not self.meteorito_m.alive():
                self.crear_meteoritos_m()
        else:
            self.meteorito_m.kill()
