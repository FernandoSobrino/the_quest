import pygame as pg

from . import ALTO_P, ANCHO_P, VIDAS
from .pantallas import PantallaPrincipal, PantallaJuego, PantallaJuego2, PantallaRecords
from .objetos import Marcador, ContadorVidas

class Quest:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((ANCHO_P, ALTO_P))
        pg.display.set_caption("THE QUEST")
        pg.mixer.init()
        self.marcador = Marcador()
        self.vidas = ContadorVidas(VIDAS)

    def jugar(self):
        contador_pantallas = 0
        while contador_pantallas < 4:
            if contador_pantallas == 0:
                pantalla_activa = PantallaPrincipal(self.display)
            if contador_pantallas == 1:
                self.marcador = Marcador()
                self.vidas = ContadorVidas(VIDAS)
                pantalla_activa = PantallaJuego(self.display,self.vidas,self.marcador)
            if contador_pantallas == 2:
                pantalla_activa = PantallaJuego2(self.display,self.vidas, self.marcador)
            if contador_pantallas == 3:
                pantalla_activa = PantallaRecords(self.display)

            pantalla_activa.bucle_principal()
            contador_pantallas += 1
            if contador_pantallas == 4:
                contador_pantallas = 0
