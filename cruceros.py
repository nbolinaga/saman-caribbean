# imports ----------------------------------------------------------------------------------------------------------------------------------------------------
import requests
from datetime import datetime

# CONSTANTES -----------------------------------------------------------------------------------------------------------------------------------------------------------
us = '\033[4m' # underline start
ue = '\033[0m' # underline end

# se llama al API y se guarda en la variable 'ships' ----------------------------------------------------------------------------------------------------------------------------------------------------
ships = requests.get("https://saman-caribbean.vercel.app/api/cruise-ships").json()

# CLASE ---------------------------------------------------------------------------------------------------------------------------------------------------------
class Cruise():
    def __init__(self, barco):
        self.name = barco.get("name")
        self.route = barco.get("route")
        self.departure = datetime.strptime(barco.get("departure"), "%Y-%m-%dT%H:%M:%S.%fZ") # se formatea la string de fecha como objeto con datetime
        self.cost = barco.get("cost")
        self.rooms = barco.get("rooms")
        self.capacity = barco.get("capacity")

    def imprimir(self,i):
        print(f"\n>>> Crucero Numero {i} <<<")
        print(f"Barco: {self.name}")
        print("Ruta: ", end='')
        print(*self.route, sep = ' ---> ')
        print(f"Fecha de Salida: {self.departure.strftime('%d/%m/%Y')}") # se impreme la fecha como dia, mes y a~o
        print(f"Habitaciones Sencillas:{self.rooms.get('simple')[0] * self.rooms.get('simple')[1]}\n{us}costo: ${self.cost.get('simple')} - capacidad: {self.capacity.get('simple')}{ue}")
        print(f"Habitaciones Premium:{self.rooms.get('premium')[0] * self.rooms.get('premium')[1]}\n{us}costo: ${self.cost.get('premium')} - capacidad: {self.capacity.get('premium')}{ue}")
        print(f"Habitaciones VIP:{self.rooms.get('vip')[0] * self.rooms.get('vip')[1]}\n{us}costo: ${self.cost.get('vip')} - capacidad: {self.capacity.get('vip')}{ue}\n")
    
    def names(self):
        return (self.name)

# main funct --------------------------------------------------------------------------------------------------------------------------------------------------------
def cruceros():
    i = 1
    cruceros = []
    for barco in ships:
        Cruise(barco).imprimir(i)
        cruceros.append(Cruise(barco).names())
        i += 1
    return(cruceros)
