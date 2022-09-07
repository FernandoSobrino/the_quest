import pygame as pg

from . import ALTO_P, ANCHO_P
from .pantallas import Pantalla, PantallaPrincipal, PantallaJuego, PantallaJuego2, PantallaRecords


class Quest:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((ANCHO_P, ALTO_P))
        pg.display.set_caption("THE QUEST")
        pg.mixer.init()
        self.pantallas = [PantallaPrincipal(self.display),
                          PantallaJuego(self.display), PantallaJuego2(
                              self.display),
                          PantallaRecords(self.display)]

    def jugar(self):
        contador_pantallas = 0
        while contador_pantallas < 4:
            pantalla_activa = self.pantallas[contador_pantallas]
            pantalla_activa.bucle_principal()
            contador_pantallas += 1
            if contador_pantallas == 4:
                contador_pantallas = 0
