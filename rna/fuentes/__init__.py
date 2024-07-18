# paquete/fuentes/__init__.py
import glob
import os

__all__ = []

for filename in glob.glob(os.path.join(os.path.dirname(__file__), "*.py")):
    if os.path.isfile(filename) and not os.path.basename(filename).startswith('__'):
        module_name = os.path.basename(filename)[:-3]
        module = __import__(f"{__name__}.{module_name}", fromlist=['*'])
        for attr in dir(module):
            if not attr.startswith('__'):
                globals()[attr] = getattr(module, attr)
                __all__.append(attr)