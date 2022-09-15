import os
import pygame as pg

from . import ALTO_P, ANCHO_P, VIDAS
from .pantallas import PantallaPrincipal, PantallaJuego, PantallaJuego2, PantallaRecords, PantallaHistoria
from .objetos import Marcador


class Quest:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((ANCHO_P, ALTO_P))
        icono_juego = pg.image.load(os.path.join(
        "resources","images","icono_planeta.png"))
        pg.display.set_icon(icono_juego)
        pg.display.set_caption("THE QUEST")
        pg.mixer.init()

    def jugar(self):
        contador_pantallas = 0
        while contador_pantallas < 5:
            if contador_pantallas == 0:
                pantalla_activa = PantallaPrincipal(self.display)
            if contador_pantallas == 1:
                pantalla_activa = PantallaHistoria(self.display)
            if contador_pantallas == 2:
                self.marcador = Marcador(VIDAS)
                pantalla_activa = PantallaJuego(
                    self.display, self.marcador)
            if contador_pantallas == 3:
                pantalla_activa = PantallaJuego2(
                    self.display, self.marcador)
            if contador_pantallas == 4:
                pantalla_activa = PantallaRecords(self.display)

            fin_juego = pantalla_activa.bucle_principal()
            if fin_juego == True:
                contador_pantallas = 4
            else:
                contador_pantallas += 1
            if contador_pantallas == 5:
                contador_pantallas = 0
