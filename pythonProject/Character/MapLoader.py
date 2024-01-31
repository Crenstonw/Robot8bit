from config import *


class MapLoader:
    bombas = 0
    diamantes = 0
    pociones = 0
    trajes = 0
    lines = []
    def __init__(self):
        self.route = 'assets/map.txt'
        with open(self.route, 'r') as map:
            MapLoader.lines = map.readlines()
        bombas, diamantes, pociones, trajes = self.lines[0].split(',')
        bombas.split(':')
        MapLoader.bombas = int(bombas[2])
        diamantes.split(':')
        MapLoader.diamantes = int(diamantes[2])
        pociones.split(':')
        MapLoader.pociones = int(pociones[2])
        trajes.split(':')
        MapLoader.trajes = int(trajes[2])

