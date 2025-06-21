# Dependencias necesarias para este proyecto:
# - numpy
# - opencv-python
# - tensorflow
# - pillow
# - pyserial
# - customtkinter

#Compilar
#pyinstaller --onefile --noconsole --icon=icon.ico --add-data "keras;keras" --name="Selector de PET" main.py


import os
import serial.tools.list_ports

NAME_APP = 'Slector de PET'

def get_available_port(exclude="COM3"):
    ports = [port.device for port in serial.tools.list_ports.comports()]
    ports = [p for p in ports if p.upper() != exclude.upper()]
    return ports[0] if ports else None

COM = get_available_port()
if COM is None:
    raise RuntimeError("No hay puertos COM disponibles (excepto COM3). Conecta el Arduino.")

BAUDRATE = 9600
TIMEOUT =.1

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIANZA = 85

LABEL_WIDTH = 640
LABEL_HEIGHT = 480

UPDATE_FRAME = 5

ICON_PATH = os.path.join(DIR_PATH, "icon.ico")

