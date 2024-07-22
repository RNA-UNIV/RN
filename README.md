<div align="center">
  <hr>
  <h1><strong>Repositorio RNA de Github</strong></h1>
    <a href="https://colab.research.google.com/github/RNA-UNIV/rna/blob/main/DemoRNA.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg"/></a>
  <hr>
</div>


El repositorio para aprendizaje de redes neuronales está disponible de forma  pública en https://github.com/RNA-UNIV/rna

El objetivo del repositorio es el de proveer funciones y clases con implementaciones básicas de algoritmos de redes neuronales, carga de datasets, carga de modelos y carga de ejemplos para pruebas y visualizciones.

Se instala directamente desde el repositorio mediante **pip install git+https://github.com/RNA-UNIV/rna.git**. Esta instalación descarga los archivos python para trabajar y prepara las estructuras de carpetas para realizar descargas de recursos (datasets, modelos, archivos, etc.) bajo demanda. Estos son los módulos dentro del paquete rna donde se encuentran definidos clases y funciones para diferentes tareas:
* **audio**: procesamiento de audio.
* **callbacks**: callbacks para tensorflow.
* **datos**: carga de recursos.
* **fuentes**: clases con algoritmos de redes neuronales.
* **imagenes**: procesamiento de imagenes.

# Uso de clase DataLoader para carga de recursos
Esta clase tiene como objetivo la carga de recursos, principalmente datasets. Crea la carpeta de trabajo **rna_descargas** y subcarpetas para el almacenamiento bajo demanda de datasets, modelos y ejemplos puntuales para pruebas (imagenes, audios, etc.).

## Carga de Modelos
La clase **DataLoader** definida en **rna.datos** se encarga del manejo de todo lo asociado a la carga de datasets. Cada dataset se conoce con un nombre único. Algunas de las funciones que realiza son:
* **list_datasets**: listas los datasets disponibles en el repositorio git.
* **load_dataframe**: carga un dataset como dataframe.
* **load_array**: carga un dataset como arreglo numpy.
* **dataset_info**: ofrece información del dataset (nombre, descripción, autores, url de descarga, descripión breve de atributos, cantidad de ejemplos, etc.).
* **dataset_directory**: directorio local donde se encuentra el dataset. Útil para realizar algun tipo de procesamiento para archivos individuales como audios e imágenes.

En el repositorio git cada dataset tiene asociada una carpeta (nombre del dataset) y dentro de la carpeta se encuentra un archivo .csv o .zip con el dataset y un archivo adicional con la información del dataset (info.json). Estos archivos se descargan bajo demanda en la subcarpeta con el nombre del repositorio dentro de la carpeta **modelos** .
