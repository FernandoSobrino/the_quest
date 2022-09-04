import os
import random
from sys import byteorder

import pygame as pg

from . import ANCHO_P, ALTO_P, COLOR_TEXTO, COLOR_TEXTO2, FPS, RUTA, TIEMPO_FINALIZACION, VIDAS

from .objetos import ContadorVidas, Explosion, Marcador, Meteorito, MeteoritoMediano, Nave, Planeta
from .records import GestorBD


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
            "resources", "images", "fondo_intro.jpg"))
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

        self.meteoritos_m = pg.sprite.Group()
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

        # carga del gestor de la base de datos
        self.bd = GestorBD(RUTA)

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
                self.planeta.mover_planeta(aterrizaje)
                self.jugador.aterrizar_nave(aterrizaje, self.pantalla)

            # Para dibujar y actualizar el grupo de meteoritos
            self.meteoritos.update()
            self.meteoritos.draw(self.pantalla)

            self.meteoritos_m.update()
            self.meteoritos_m.draw(self.pantalla)

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
                colision = pg.sprite.spritecollide(
                    self.jugador, self.meteoritos, True)
                colision_m = pg.sprite.spritecollide(
                    self.jugador, self.meteoritos_m, True)

                if colision or colision_m:
                    explosion = Explosion(self.jugador.rect.center)
                    self.explosiones.add(explosion)
                    self.jugador.esconder_nave()
                    self.exp_sound.play()
                    self.contador_vidas.perder_vida()

            # Cuenta puntos por meteoritos esquivados, les asigna puntuación y los elimina de su grupo
            if not aterrizaje:
                for meteorito in self.meteoritos.sprites():
                    if meteorito.rect.right < 0:
                        self.marcador.aumentar(meteorito.puntos)
                        self.meteoritos.remove(meteorito)

                for meteorito_m in self.meteoritos_m.sprites():
                    if meteorito_m.rect.right < 0:
                        self.marcador.aumentar(meteorito_m.puntos)
                        self.meteoritos_m.remove(meteorito_m)

            # Crea nuevos meteoritos al salir de la pantalla
            if not aterrizaje:
                if not meteorito.alive():
                    self.crear_meteoritos()
                if not meteorito_m.alive():
                    self.crear_meteoritos_m()
            # Si la nave aterriza, ya no se crean más
            else:
                if meteorito.rect.right < 0:
                    meteorito.remove(self.meteoritos)
                if meteorito_m.rect.right < 0:
                    meteorito_m.remove(self.meteoritos_m)

            # Para pintar el marcador de puntos
            self.marcador.pintar_marcador(self.pantalla)

            # Condición que activa el flag de aterrizaje
            if self.marcador.valor >= 100:
                aterrizaje = True

            # (POSIBLE) condición para realizar la finalización de nivel (A DESARROLLAR)
            if self.jugador.fin_rotacion:
                self.pintar_fin_nivel()
                contador = pg.time.get_ticks()/10000
                # print(contador)
                if contador > TIEMPO_FINALIZACION:
                    self.bd.pregunta_nombre()
                    self.bd.guardarRecords(self.bd.nombre, self.marcador.valor)
                    print(self.bd.nombre)
                    print(self.marcador.valor)
                    salir = True

            # Actualización de todos los elementos que se están mostrando en la partida
            pg.display.flip()

            # Para cerrar el juego pasados 2.5 segundos tras el aterrizaje

            # Para cerrar el juego si se pierden todas las vidas
            if self.contador_vidas.vidas == 0:
                salir = self.contador_vidas.perder_vida()
                print("Perdiste todas las vidas")

    # -------------MÉTODOS DE FUNCIONAMIENTO INDEPENDIENTES DE LAS CLASES-----------#

    def pintar_fondo(self):
        "Este método pinta el fondo de estrellas de la pantalla del juego"
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo_nivel.jpeg"))
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_fin_nivel(self):
        font_file = os.path.join("resources", "fonts",
                                 "light_sans_serif_7.ttf")
        self.tipografia = pg.font.Font(font_file, 50)
        mensaje = "¡ENHORABUENA! HAS GANADO"
        texto = self.tipografia.render(mensaje, True, COLOR_TEXTO2)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = texto.get_height()*3
        self.pantalla.blit(texto, (pos_x, pos_y))

    def crear_meteoritos(self):
        """"Este método genera los meteoritos grandes al inicio de la partida, les asigna puntuación y
        es llamado de nuevo desde el método regenerar las veces que el meteorito finaliza su ciclo de vida"""""
        cantidad_meteoritos = random.randint(1, 3)
        for i in range(cantidad_meteoritos):
            puntos = (i + 10) - i
            meteorito = Meteorito(puntos)
            self.meteoritos.add(meteorito)

    def crear_meteoritos_m(self):
        """"Este método genera los meteoritos medianos al inicio de la partida, les asigna puntuación
         y es llamado de nuevo desde el método regenerar las veces que el meteorito finaliza su ciclo de vida"""""
        cantidad_meteoritos_m = random.randint(2, 4)
        for i in range(cantidad_meteoritos_m):
            puntos_m = (i + 20) - i
            meteorito_m = MeteoritoMediano(puntos_m)
            self.meteoritos_m.add(meteorito_m)


class PantallaRecords(Pantalla):
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        # self.musica = pg.mixer.music.load(os.path.join(
        # "resources", "sounds", "musica_records.mp3"))
        self.bd = GestorBD(RUTA)
        self.bd.obtenerRecords()
        font_file = os.path.join("resources", "fonts", "game_sans_serif_7.ttf")
        self.tipografia = pg.font.Font(font_file, 20)

    def bucle_principal(self):
        salir = False
        borde = 100
        d = 'id'
        nombres_record = []
        nombres_render = []
        puntos_record = []
        puntos_render = []

        for record in self.bd.records:
            record.pop(d)
            for value in record.values():
                if isinstance(value, str):
                    nombres_record.append(value)
                if isinstance(value, int):
                    puntos_record.append(value)

        for nombre in nombres_record:
            texto_render = self.tipografia.render(str(nombre),
                                                  True, COLOR_TEXTO2)
            nombres_render.append(texto_render)

        for punto in puntos_record:
            texto_render2 = self.tipografia.render(str(punto),
                                                   True, COLOR_TEXTO2)
            puntos_render.append(texto_render2)

        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            self.pintar_fondo()

            for i in range(len(nombres_render)):
                pos_x = ANCHO_P/2 - texto_render.get_width()
                pos_y = i*texto_render.get_height() + borde
                self.pantalla.blit(nombres_render[i], (pos_x, pos_y))

            for j in range(len(puntos_render)):
                pos_x = ANCHO_P/2 - texto_render2.get_width() + 200
                pos_y = j*texto_render2.get_height() + borde
                self.pantalla.blit(puntos_render[j], (pos_x, pos_y))

            pg.display.flip()

    def pintar_fondo(self):
        "Este método pinta el fondo de estrellas de la pantalla de records"
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo_intro.jpg"))
        self.pantalla.blit(self.fondo, (0, 0))
