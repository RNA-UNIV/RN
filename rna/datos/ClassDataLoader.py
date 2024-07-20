import os
import requests
import pandas as pd
import json
from chardet.universaldetector import UniversalDetector


class DataLoader:
    _models_dir = 'modelos'
    _data_dir = 'datos'
    _samples_dir = 'ejemplos'
    _repo_download_dir = 'descargas'
    _instance = None
    _base_path = None
    _base_url = "https://api.github.com/repos/RNA-UNIV/rna/contents"


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataLoader, cls).__new__(cls, *args, **kwargs)
            cls._base_path = os.path.join(os.getcwd(), 'rna_descargas')
            cls._create_directories()
        return cls._instance

    @classmethod
    def _create_directories(cls):
        if not os.path.exists(cls._base_path):
            os.makedirs(cls._base_path)
        cls.models_path = os.path.join(cls._base_path, cls._models_dir)
        cls.data_path = os.path.join(cls._base_path, cls._data_dir)
        cls.samples_path = os.path.join(cls._base_path, cls._samples_dir)
        os.makedirs(cls.models_path, exist_ok=True)
        os.makedirs(cls.data_path, exist_ok=True)
        os.makedirs(cls.samples_path, exist_ok=True)

    @classmethod
    def _list_files(cls, subfolder, filetype =['file', 'dir']):
        url = f"{cls._base_url}/{subfolder}"
        response = requests.get(url)
        if response.status_code == 200:
            files = response.json()
            return [file['name'] for file in files if file['type'] in filetype]
        else:
            return []

    @classmethod
    def list_datasets(cls):
        return cls._list_files(f"{cls._repo_download_dir}/{cls._data_dir}", filetype=['dir'])

    @classmethod
    def _download_file(cls, url, local_path):
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, 'wb') as file:
            file.write(response.content)

    @classmethod
    def _download_directory(cls, github_path, local_path, force=False, verbose=1):
        url = f"{cls._base_url}/{github_path}"
        response = requests.get(url)
        response.raise_for_status()
        contents = response.json()

        for item in contents:
            if item['type'] == 'file':
                file_url = item['download_url']
                file_path = os.path.join(local_path, item['name'])
                if force or not os.path.exists(file_path):
                    if verbose:
                        print(f"Descargando {file_path}")
                    cls._download_file(file_url, file_path)
            elif item['type'] == 'dir':
                new_local_path = os.path.join(local_path, item['name'])
                os.makedirs(new_local_path, exist_ok=True)
                cls._download_directory(item['path'], new_local_path, force, verbose)

    @classmethod
    def load_data(cls, github_path, local_subpath, force=False, verbose=1):
        local_path = os.path.join(cls._base_path, local_subpath)
        os.makedirs(local_path, exist_ok=True)
        cls._download_directory(github_path, local_path, force, verbose)

    @classmethod
    def load_dataframe(cls, nombre, encoding=None, separator=None):
        nombre = nombre.lower()
        local_path = os.path.join(cls.data_path, nombre)
        github_path = f"{cls._repo_download_dir}/{cls._data_dir}/{nombre}"

        if not os.path.exists(local_path):
            os.makedirs(local_path, exist_ok=True)
            cls._download_directory(github_path, local_path)

        files = [f for f in os.listdir(local_path) if f.endswith('.csv')]
        if not files:
            raise FileNotFoundError(f"No se encontraron archivos .csv en la carpeta {local_path}")

        file_path = os.path.join(local_path, files[0])
        if encoding is None:
            encoding = cls._detect_encoding(file_path)
        if separator is None:
            separator = cls._detect_separator(file_path, encoding)

        df = pd.read_csv(file_path, encoding=encoding, sep=separator)
        return df

    @classmethod
    def load_array(cls, nombre, encoding=None, separator=None):
        df = cls.load_dataframe(nombre, encoding, separator)
        return (df.columns, df.to_numpy())

    @classmethod
    def _detect_encoding(cls, file_path):
        detector = UniversalDetector()
        with open(file_path, 'rb') as f:
            for line in f:
                detector.feed(line)
                if detector.done:
                    break
        detector.close()
        return detector.result['encoding']

    @classmethod
    def _detect_separator(cls, file_path, encoding):
        with open(file_path, 'r', encoding=encoding) as f:
            first_line = f.readline()
            separators = [',', ';', '\t']
            return max(separators, key=lambda sep: first_line.count(sep))

    @classmethod
    def dataset_info(cls, nombre):
        nombre = nombre.lower()
        local_path = os.path.join(cls.data_path, nombre)
        github_path = f"{cls._repo_download_dir}/{cls._data_dir}/{nombre}"

        if not os.path.exists(local_path):
            os.makedirs(local_path, exist_ok=True)
            cls._download_directory(github_path, local_path)

        info_file_path = os.path.join(local_path, 'info.json')
        if not os.path.exists(info_file_path):
            raise FileNotFoundError(f"No se encontró información sobre el dataset \"{nombre}\"")

        with open(info_file_path, 'r', encoding='utf-8') as f:
            info_data = json.load(f)

        return info_data

    @classmethod
    def dataset_directory(cls, nombre):
        nombre = nombre.lower()
        local_path = os.path.join(cls.data_path, nombre)
        github_path = f"{cls._repo_download_dir}/{cls._data_dir}/{nombre}"

        if not os.path.exists(local_path):
            os.makedirs(local_path, exist_ok=True)
            cls._(github_path, local_path)

        return local_path