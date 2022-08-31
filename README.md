# The Quest

Año 2045. El planeta Tierra ha sido asolado por una fuerte tormenta solar.
Los únicos supervivientes han tomado rumbo en un transbordador espacial hacia 
un nuevo planeta habitable en el espacio exterior. Lleva a estos supervivientes 
esquivando los peligros del espacio y consigue liberar a la raza humana
de la extinción inminente.

## Para jugar

1. Clonar el repositorio

````
# con ssh
git clone ssh:// (lo que sigue)

# con https
git clone https:// (lo que sigue)

````

2. Crear un entorno virtual dentro de la raíz del repositorio

    Asegúrese de que se encuentra en el directorio raíz. Para ello,
    ejecute en su consola:

`````
cd quest

# Para crear el entorno virtual:

python -m venv nombre_del_entorno
(se recomienda env por defecto)

`````

3. Instalar las dependencias

````
pip install -r requirements.txt
````


4. Arrancar el juego

    Por último, ejecute la activación del entorno virtual:

````
# en Windows:
.\env\Scripts\activate

# en Mac, Linux:
source ./env/bin/activate

#ejecute el módulo principal para jugar:
python main.py
````

## Para colaborar en el proyecto

Siga los pasos 1 y 2 anteriores tal y como se indican.

3. Instalar las dependencias

````
pip install requirements-dev.txt
````

4. Abra el repositorio como directorio en tu IDE favorito
