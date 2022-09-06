import os
import pygame as pg
import sqlite3

from . import ANCHO_P, ALTO_P


class GestorBD:
    def __init__(self, ruta):
        self.ruta = ruta

    def obtenerRecords(self):
        "Consulta todos los records almacenados en la base de datos"
        consulta = "SELECT * FROM records ORDER BY puntos DESC LIMIT 10"

        # 1- Conectar con la base de datos
        conexion = sqlite3.connect(self.ruta)

        # 2- Generar el cursor de la consulta
        cursor = conexion.cursor()

        # 3- Pasar la consulta a SQL y ejecutar
        cursor.execute(consulta)

        self.records = []
        nombres_columnas = []

        for desc_columna in cursor.description:
            nombres_columnas.append(desc_columna[0])

        datos = cursor.fetchall()
        for dato in datos:
            self.record = {}
            indice = 0
            for nombre in nombres_columnas:
                self.record[nombre] = dato[indice]
                indice += 1
            self.records.append(self.record)

        conexion.close()

        return self.records

    def guardarRecords(self, nombre, puntos):
        "Guarda nuevo record en la base de datos"
        consulta = "INSERT INTO records (nombre,puntos) VALUES (?,?)"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta, (nombre, puntos))
        conexion.commit()
        conexion.close()

    def eliminarRecords(self):
        "Método para pruebas. Manejar con cuidado. Elimina todos los datos"
        consulta = "DELETE FROM records"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        conexion.close()

class InputBox:

    def __init__(self, pantalla: pg.Surface, color_texto="white", color_fondo="black", title=""):
        font_file = os.path.join(
            "resources", "fonts", "game_sans_serif_7.ttf")
        self.tipografia = pg.font.Font(font_file, 20)
        self.texto = ""
        self.color_fondo = color_fondo
        self.color_texto = color_texto
        self.pantalla = pantalla
        self.padding = 30
        self.crear_elementos_fijos()

    def get_text(self):
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE and len(self.texto) > 0:
                        self.texto = self.texto[:-1]
                    elif event.key == pg.K_RETURN:
                        salir = True
                    else:
                        self.texto += event.unicode
            self.pintar()
            pg.display.flip()
        return self.texto

    def pintar(self):
        pg.draw.rect(self.pantalla, self.color_fondo, self.fondo)
        self.pantalla.blit(self.titulo, (self.x_titulo, self.y_titulo))

        superficie_texto = self.tipografia.render(
            self.texto, True, self.color_texto, self.color_fondo)
        pos_x = self.x_titulo
        pos_y = self.y_titulo + self.titulo.get_height()
        self.pantalla.blit(superficie_texto, (pos_x, pos_y))

    def crear_elementos_fijos(self):
        # el título
        self.titulo = self.tipografia.render(
            "Nuevo record. Escribe tu nombre:", True, self.color_texto, self.color_fondo)
        self.x_titulo = (ANCHO_P-self.titulo.get_width())//2
        self.y_titulo = (ALTO_P-self.titulo.get_height())//2

        # el rectángulo de fondo
        x_fondo = self.x_titulo - self.padding
        y_fondo = self.y_titulo - self.padding
        w_fondo = self.titulo.get_width() + self.padding * 2
        h_fondo = self.titulo.get_height() * 2 + self.padding * 2
        self.fondo = pg.Rect(x_fondo, y_fondo, w_fondo, h_fondo)
