import pygame as pg

from . import ALTO_P, ANCHO_P
from .pantallas import Pantalla, PantallaPrincipal, PantallaJuego, PantallaJuego2, PantallaRecords


class Quest:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((ANCHO_P, ALTO_P))
        pg.display.set_caption("THE QUEST")
        pg.mixer.init()
        self.pantallas = [
            Pantalla(self.display),
            PantallaPrincipal(self.display),
            PantallaJuego(self.display),PantallaJuego2(self.display),
            PantallaRecords(self.display)]

    def jugar(self):
        for pantalla in self.pantallas:
            pantalla.bucle_principal()