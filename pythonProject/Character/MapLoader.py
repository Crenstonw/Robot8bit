import os.path

from config import *
import random
from sprites import *


class MapLoader:
    bombas = 0
    diamantes = 0
    pociones = 0
    trajes = 0
    lines = []

    def __init__(self):
        self.ruta = os.path.join(os.path.dirname(__file__), 'map.txt')
        with open(self.ruta, 'r') as map:
            self.lines = map.readlines()
        bombas, diamantes, pociones, trajes = self.lines[0].split(',')
        self.lines.pop(0)
        Config.maptile = self.lines
        self.map = [line.strip() for line in self.lines]
        bombas.split(':')
        self.bombas = int(bombas[2])
        diamantes.split(':')
        self.diamantes = int(diamantes[2])
        pociones.split(':')
        self.pociones = int(pociones[2])
        trajes.split(':')
        self.trajes = int(trajes[2])




