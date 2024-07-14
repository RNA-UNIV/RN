from setuptools import setup, find_packages

setup(
    name="rna",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    package_data={
        "": ["descargas/**/*"],
    },
    install_requires=[
        # Dependencias del paquete
    ],
    author="César",
    author_email="tu@email.com",
    description="Paquete para aprendizaje de redes neuronales",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/mi_paquete",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
