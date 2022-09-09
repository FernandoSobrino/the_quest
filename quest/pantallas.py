import os
import random
import pygame as pg

from . import ANCHO_P, ALTO_P, COLOR_TEXTO, COLOR_TEXTO2, FPS, MUSICA_FADE_OUT, PUNTOS_PARTIDA, RUTA

from .objetos import Explosion, Meteorito, MeteoritoDorado, MeteoritoMediano, Nave, Planeta
from .records import GestorBD, InputBox


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

    def __init__(self, pantalla: pg.Surface, marcador):
        super().__init__(pantalla)

        # creación de la nave
        self.jugador = Nave()

        # creación de los meteoritos
        self.meteoritos = pg.sprite.Group()
        self.crear_meteoritos()

        self.meteoritos_m = pg.sprite.Group()
        self.crear_meteoritos_m()

        self.grupo_dorado = pg.sprite.Group()

        # creación del planeta
        imagen_planeta1 = pg.image.load(os.path.join("resources", "images",
                                                     "planeta1.png"))
        self.planeta = Planeta(imagen_planeta1)

        # creación de las explosiones
        self.explosiones = pg.sprite.Group()

        # creación del marcador de puntos
        self.marcador = marcador

        # carga del sonido de la explosión
        self.sonido_explosion = pg.mixer.Sound(os.path.join(
            "resources", "sounds", "sonido_explosion.wav"))

        self.sonido_meteorito = pg.mixer.Sound(os.path.join(
            "resources", "sounds", "sonido_meteorito.mp3"))

        # carga de la música del juego
        self.musica = pg.mixer.music.load(os.path.join(
            "resources", "sounds", "musica_juego.mp3"))

    def bucle_principal(self):
        "Método que controla el juego"

        # Punto para empezar a contar los ticks del juego
        ticks_juego = pg.time.get_ticks()

        # Flags de salida del juego y de fase de aterrizaje
        salir = False
        aterrizaje = False

        # Flag que controla la salida de un meteorito dorado en la partida
        meteorito_instanciado = False

        # Reproducción de la música del juego (en bucle)
        pg.mixer.music.play(-1)

        while not salir:
            self.reloj.tick(FPS)

            # para medir el tiempo que transcurre durante la partida
            contador_juego = (pg.time.get_ticks() - ticks_juego)//1000
            # print(contador_juego)
            """
            Parte comentada para pruebas: activa, mide los FPS por seg. para
            ver problemas de ejecución del juego
            """
            #tiempo_fps = self.reloj.get_fps()
            # print(tiempo_fps)
            # Condición para cerrar el juego si pulsamos la X de la ventana
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            # Para pintar el fondo del nivel
            self.pintar_fondo()

            # Para mover y pintar la nave y mover el planeta cuando la nave aterrice
            self.mover_nave_planeta(aterrizaje)

            # Para pintar objetos que forman parte de la partida
            self.pintar_objetos_partida()

            # Colisión de la nave con meteorito, aparece explosion (efecto y sonido) y
            # desaparece la nave. También desactiva colisiones durante el aterrizaje
            self.comportamiento_meteoritos(aterrizaje)

            # Para pintar el marcador de puntos
            self.marcador.pintar_marcador(self.pantalla)

            # Condición para que en un momento aleatorio en el rango marcado,
            # salga un meteorito dorado que otorga 1000 puntos al jugador.
            if contador_juego == random.randint(20, 40):
                if not meteorito_instanciado:
                    self.crear_meteorito_dorado()
                    meteorito_instanciado = True

            # Condición que activa el flag de aterrizaje (Tiempo transcurrido)
            if contador_juego == 45:
                aterrizaje = True

            # Condiciones para realizar la finalización de nivel 1
            if self.jugador.fin_rotacion:
                self.pintar_fin_nivel("¡NIVEL 1 SUPERADO!")
            if contador_juego == 60:
                salir = True

            # Actualización de todos los elementos que se están mostrando en la partida
            pg.display.flip()

            # Para cerrar el juego si se pierden todas las vidas
            if self.marcador.vidas == 0:
                pg.quit()
                print("Perdiste todas las vidas")

    # -------------MÉTODOS DE FUNCIONAMIENTO FUERA DEL BUCLE PRINCIPAL-----------#

    def crear_meteoritos(self):
        """"Este método genera los meteoritos grandes al inicio de la partida, les asigna puntuación y
        es llamado de nuevo desde el método regenerar las veces que el meteorito finaliza su ciclo de vida"""""
        cantidad_meteoritos = random.randrange(1, 3)
        for i in range(cantidad_meteoritos):
            puntos = (i + 10) - i
            meteorito = Meteorito(puntos)
            self.meteoritos.add(meteorito)

    def crear_meteoritos_m(self):
        """"Este método genera los meteoritos medianos al inicio de la partida, les asigna puntuación
         y es llamado de nuevo desde el método regenerar las veces que el meteorito finaliza su ciclo de vida"""""
        cantidad_meteoritos_m = random.randrange(2, 4)
        for i in range(cantidad_meteoritos_m):
            puntos_m = (i + 20) - i
            meteorito_m = MeteoritoMediano(puntos_m)
            self.meteoritos_m.add(meteorito_m)

    def crear_meteorito_dorado(self):
        self.meteo_dorado = MeteoritoDorado(PUNTOS_PARTIDA)
        self.grupo_dorado.add(self.meteo_dorado)

    def comportamiento_meteoritos(self, aterrizar):
        if not aterrizar:
            colision = pg.sprite.spritecollide(
                self.jugador, self.meteoritos, True)
            colision_m = pg.sprite.spritecollide(
                self.jugador, self.meteoritos_m, True)
            colision_dorado = pg.sprite.spritecollide(
                self.jugador, self.grupo_dorado, True)

            if colision or colision_m:
                explosion = Explosion(self.jugador.rect.center)
                self.explosiones.add(explosion)
                self.jugador.esconder_nave()
                self.sonido_explosion.play()
                self.marcador.perder_vida()
            if colision_dorado:
                self.marcador.aumentar(1000)
                self.sonido_meteorito.play()

            for meteorito in self.meteoritos.sprites():
                if meteorito.rect.right < 0:
                    if not self.jugador.nave_escondida:
                        self.marcador.aumentar(meteorito.puntos)
                    self.meteoritos.remove(meteorito)
            if len(self.meteoritos.sprites()) < 1:
                self.crear_meteoritos()

            for meteorito_m in self.meteoritos_m.sprites():
                if meteorito_m.rect.right < 0:
                    if not self.jugador.nave_escondida:
                        self.marcador.aumentar(meteorito_m.puntos)
                    self.meteoritos_m.remove(meteorito_m)
            if len(self.meteoritos_m.sprites()) < 1:
                self.crear_meteoritos_m()
        else:
            self.meteoritos.clear(self.pantalla, self.pantalla)
            self.meteoritos_m.clear(self.pantalla, self.pantalla)

    def mover_nave_planeta(self, aterrizar):
        "Este método incluye las maniobras de la nave y el comportamiento del planeta"
        self.jugador.update()
        if not aterrizar:
            self.pantalla.blit(self.jugador.image, self.jugador.rect)
        else:
            self.pantalla.blit(self.planeta.image, self.planeta.rect)
            self.planeta.mover_planeta(aterrizar)
            self.jugador.aterrizar_nave(aterrizar, self.pantalla)

    def pintar_fin_nivel(self, texto):
        "Este método pinta el mensaje que indica el fin del nivel"
        font_file = os.path.join("resources", "fonts",
                                 "light_sans_serif_7.ttf")
        self.tipografia = pg.font.Font(font_file, 50)
        mensaje = texto
        texto = self.tipografia.render(mensaje, True, COLOR_TEXTO2)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = texto.get_height()*3
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_fondo(self):
        "Este método pinta el fondo de estrellas de la pantalla del juego"
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo_nivel.jpeg"))
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_objetos_partida(self):
        "Este método incluye el update y el pintado de elementos del juego"
        # Para dibujar y actualizar el grupo de meteoritos
        self.meteoritos.update()
        self.meteoritos.draw(self.pantalla)

        self.meteoritos_m.update()
        self.meteoritos_m.draw(self.pantalla)

        self.grupo_dorado.update()
        self.grupo_dorado.draw(self.pantalla)

        # Para dibujar y actualizar las explosiones
        self.explosiones.update()
        self.explosiones.draw(self.pantalla)


class PantallaJuego2(PantallaJuego):
    def __init__(self, pantalla: pg.Surface, marcador):
        super().__init__(pantalla, marcador)

        # creación del planeta
        imagen_planeta2 = pg.image.load(os.path.join("resources", "images",
                                                     "planeta2.png"))
        self.planeta = Planeta(imagen_planeta2)

    def bucle_principal(self):
        "Método que controla el juego"

        # Punto para empezar a contar los ticks del juego
        ticks_juego = pg.time.get_ticks()

        # Flags de salida del juego y de fase de aterrizaje
        salir = False
        aterrizaje = False

        # Flag que controla la salida de un meteorito dorado en la partida
        meteorito_instanciado = False

        # Reproducción de la música del juego (en bucle)
        pg.mixer.music.play(-1)

        while not salir:
            self.reloj.tick(FPS)

            # para medir el tiempo que transcurre durante la partida
            contador_juego = (pg.time.get_ticks() - ticks_juego)//1000
            # print(contador_juego)
            """
            Parte comentada para pruebas: activa, mide los FPS por seg. para
            ver problemas de ejecución del juego
            """
            #tiempo_fps = self.reloj.get_fps()
            # print(tiempo_fps)

            # Condición para cerrar el juego si pulsamos la X de la ventana
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            # Para pintar el fondo del nivel
            self.pintar_fondo()

            # Para mover y pintar la nave y mover el planeta cuando la nave aterrice
            self.mover_nave_planeta(aterrizaje)

            # Para pintar los elementos de la partida
            self.pintar_objetos_partida()

            # Colisión de la nave con meteorito, aparece explosion (efecto y sonido) y
            # desaparece la nave. También desactiva colisiones durante el aterrizaje
            self.comportamiento_meteoritos(aterrizaje)

            # Para pintar el marcador de puntos
            self.marcador.pintar_marcador(self.pantalla)

            # Condición para que en un momento aleatorio en el rango marcado,
            # salga un meteorito dorado que otorga 1000 puntos al jugador.
            if contador_juego == random.randint(30, 60):
                if not meteorito_instanciado:
                    self.crear_meteorito_dorado()
                    meteorito_instanciado = True

            # Condición que activa el flag de aterrizaje (Tiempo transcurrido)
            print(aterrizaje, contador_juego)
            if contador_juego == 90:
                aterrizaje = True

            # Condiciones para realizar la finalización de nivel 2
            if self.jugador.fin_rotacion:
                self.pintar_fin_nivel("¡ENHORABUENA! HAS GANADO")

            if contador_juego == 105:
                inputbox = InputBox(self.pantalla)
                pg.mixer.music.fadeout(MUSICA_FADE_OUT)
                nombre = inputbox.recoger_nombre()
                bd = GestorBD(RUTA)
                bd.guardarRecords(nombre, self.marcador.valor)
                pg.mixer.music.stop()
                salir = True

            # Actualización de todos los elementos que se están mostrando en la partida
            pg.display.flip()

            # Para cerrar el juego si se pierden todas las vidas
            if self.marcador.vidas == 0:
                pg.quit()
                print("Perdiste todas las vidas")

    # -------------MÉTODOS DE FUNCIONAMIENTO DIFERENTES DEL NIVEL 1 (EN PROGRESO)-----------#

    def crear_meteoritos(self):
        """"Este método genera los meteoritos grandes al inicio de la partida, les asigna puntuación y
        es llamado de nuevo desde el método regenerar las veces que el meteorito finaliza su ciclo de vida"""""
        cantidad_meteoritos = random.randrange(2, 4)
        for i in range(cantidad_meteoritos):
            puntos = (i + 10) - i
            meteorito = Meteorito(puntos)
            self.meteoritos.add(meteorito)

    def crear_meteoritos_m(self):
        """"Este método genera los meteoritos medianos al inicio de la partida, les asigna puntuación
         y es llamado de nuevo desde el método regenerar las veces que el meteorito finaliza su ciclo de vida"""""
        cantidad_meteoritos_m = random.randrange(3, 5)
        for i in range(cantidad_meteoritos_m):
            puntos_m = (i + 20) - i
            meteorito_m = MeteoritoMediano(puntos_m)
            self.meteoritos_m.add(meteorito_m)


class PantallaRecords(Pantalla):
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        self.musica = pg.mixer.music.load(os.path.join(
            "resources", "sounds", "musica_records.mp3"))
        self.bd = GestorBD(RUTA)
        self.records = []
        font_file = os.path.join("resources", "fonts", "game_sans_serif_7.ttf")
        self.tipografia = pg.font.Font(font_file, 25)
        self.tipo_titulos = pg.font.Font(font_file, 30)
        self.tipo_reiniciar = pg.font.Font(font_file, 30)
        self.nombres_record = []
        self.nombres_render = []
        self.puntos_record = []
        self.puntos_render = []

    def bucle_principal(self):
        salir = False
    # Para almacenar los valores de NOMBRE y PUNTOS en listas independientes
    # para poder ser renderizados
        pg.mixer.music.play(-1)
        self.cargar_datos()

    # Renderizado de cada una de las listas de NOMBRE y PUNTOS
        for nombre in self.nombres_record:
            texto_renderizar = self.tipografia.render(str(nombre),
                                                      True, COLOR_TEXTO2)
            self.nombres_render.append(texto_renderizar)

        for punto in self.puntos_record:
            texto_renderizar2 = self.tipografia.render(str(punto),
                                                       True, COLOR_TEXTO)
            self.puntos_render.append(texto_renderizar2)

        # Bucle de funcionamiento del juego
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    pg.mixer.music.stop()
                    salir = True

            # Para pintar el fondo de estrellas de la pantalla
            self.pintar_fondo()

            # Para pintar los nombres y los records en la pantalla
            self.pintar_records(self.nombres_render, self.puntos_render, texto_renderizar,
                                texto_renderizar2)

            # Recarga de todos los elementos presentes en la pantalla
            pg.display.flip()


# -------- MÉTODOS PARA PINTAR LOS ELEMENTOS QUE SE MUESTRAN EN LA PANTALLA --------- #

    def cargar_datos(self):
        """Este método almacena los elementos a pintar en listas independientes para
        poder renderizarlos después"""
        self.records = self.bd.obtenerRecords()
        for record in self.records:
            record.pop('id')
            for value in record.values():
                if isinstance(value, str):
                    self.nombres_record.append(value)
                else:
                    self.puntos_record.append(value)

    def pintar_fondo(self):
        "Este método pinta el fondo de estrellas de la pantalla de records"
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo_intro.jpg"))
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_records(self, nombres, puntos, renderizado, renderizado2):
        "Este método hace el pintado de información (títulos y datos) de los records"
        # para pintar los títulos de los records
        pos_x_titulo = 300
        pos_x_titulo2 = 600
        pos_y_titulo = 100
        titulo_nombre = "NOMBRE"
        titulo_puntos = "PUNTOS"

        nombres_jugador_render = self.tipo_titulos.render(
            titulo_nombre, True, COLOR_TEXTO2)
        self.pantalla.blit(nombres_jugador_render,
                           (pos_x_titulo, pos_y_titulo))

        puntos_jugador_render = self.tipo_titulos.render(
            titulo_puntos, True, COLOR_TEXTO)
        self.pantalla.blit(puntos_jugador_render,
                           (pos_x_titulo2, pos_y_titulo))

        # para pintar los datos de los records
        salto_linea = 200
        separacion_x = 200

        for i in range(len(nombres)):
            pos_x = ANCHO_P/3 + renderizado.get_width() - 50
            pos_y = i * renderizado.get_height() + salto_linea
            self.pantalla.blit(nombres[i], (pos_x, pos_y))

        for j in range(len(puntos)):
            pos_x2 = ANCHO_P/3 + renderizado2.get_width() + separacion_x + 50
            pos_y2 = j * renderizado.get_height() + salto_linea
            self.pantalla.blit(puntos[j], (pos_x2, pos_y2))

        # para pintar el mensaje de volver a jugar
        texto_reiniciar = "Pulsa 'ESPACIO' para jugar de nuevo"
        reiniciar_render = self.tipo_reiniciar.render(
            texto_reiniciar, True, COLOR_TEXTO2)
        ancho_texto = reiniciar_render.get_width()
        pos_x_fin = (ANCHO_P - ancho_texto)/2
        pos_y_fin = ALTO_P - 75
        self.pantalla.blit(
            reiniciar_render, (pos_x_fin, pos_y_fin))
