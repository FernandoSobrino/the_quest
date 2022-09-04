from ast import operator
import sqlite3


class GestorBD:
    def __init__(self, ruta):
        self.ruta = ruta

    def obtenerRecords(self):
        "Consulta todos los records almacenados en la base de datos"
        consulta = "SELECT * FROM records ORDER BY puntos DESC"

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

    def pregunta_nombre(self):
        pedir_nombre = True
        while pedir_nombre:
            self.nombre = input("¿Cuál es tu nombre?")
            try:
                if len(self.nombre) == 3:
                    pedir_nombre = False
            except:
                print("Sólo puede tener tres caracteres")

        return self.nombre
