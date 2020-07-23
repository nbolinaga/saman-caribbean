# imports ----------------------------------------------------------------------------------------------------------------------------------------------------
import requests
import json
import math

# CONSTANTES -------------------------------------------------------------------------------------------------------------------------------------------------
ships = requests.get("https://saman-caribbean.vercel.app/api/cruise-ships").json()
error = '>>> Dato ingresado incorrectamente, intente de nuevo. <<<\n'

tipos = ['[1] Simple','[2] Premium','[3] VIP']
opciones = ['[1] Chequear habitaciones disponibles','[2] Reservar habitacion','[3] Desocupar habitacion','[4] Buscar habitacion','[5] Salir']
line = '_________________________________________________________________________________________________________________________________________________'
e = {'simple': 'Si puede tener servicio a la habitación.', 'premium': 'Si posee vista al mar', 'vip': 'Sí puede albergar fiestas privadas'}
types = {1: "simple", 2: "premium", 3: "vip"}
ind = {'S': "simple", 'P': "premium", 'V': "vip"}

# DATA -------------------------------------------------------------------------------------------------------------------------------------------------------
data = None
def crear_text(): # funcion que crea el text file 
    with open("proyecto/data_rooms.txt", "w+") as datos:
        for ship in ships:
            rooms = ship.get("rooms")
            habs = {"simple":{},"premium":{},"vip":{}}
            for pisos in rooms:
                for pasillos in range(rooms.get(f'{pisos}')[0]):
                    for room in range(rooms.get(f'{pisos}')[1]):
                        habs[f"{pisos}"][f"{chr(ord('A') + pasillos)}{room + 1}"] = 0
            datos.write(f'{habs}\n')

try: # se trata de abrir el text file, si no existe retorna un error
    with open("proyecto/data_rooms.txt", "r+") as datos:
        data = datos.read().splitlines()
except: # en caso de error se llama a la funcion crear_text()
    crear_text()
    with open("proyecto/data_rooms.txt", "r+") as datos:
        data = datos.read().splitlines() 

lista_habitaciones = data[:5]
json_habitaciones = []
reservaciones = []

for listas in lista_habitaciones: # se convierten los strings a json para facilitar la manipulacion
    listas = listas.replace("'", '"') # se replazan la single qoutes con double
    listas =  json.loads(listas)
    json_habitaciones.append(listas)    # se agrega el string ya convertido a la lista

clientes = data[5: ]

# CLASE ---------------------------------------------------------------------------------------------------------------------------------------------------------
class Piso(): # clase que se encarga de 'construir' los pisos
    def __init__(self, rooms, piso):
        self.rooms = rooms
        self.piso = piso
        self.habitaciones = []
    
    def chequear(self):
        for room, status in self.rooms.get(self.piso).items():
            if status == 0:
                self.habitaciones.append(room) #si la habitacion esta disponible se agrega a la lista de disponibles
            else:
                self.habitaciones.append(self.strike(room)) #si la habitacion no esta disponible se llama a la funcion strike
        return self.habitaciones

    def strike(self, text):
        result = ''
        for c in text:
            result = result + '\u0336' + c # se tachan las habitaciones no disponibles
        return result

class Reservacion(): # clase que construye las reservaciones
    def __init__(self,ship,rooms,piso,cantidad,numero):
        self.numero = numero                                        # numero de barco (0-3)
        self.piso = types.get(piso)                                 # tipo de piso (ej: simple) se toma del dict types
        self.rooms = rooms.get(f'{self.piso}')                      # cuartos
        self.cantidad = cantidad                                    # cantidad de personas para la reservacion
        self.capacidad = ship.get('capacity').get(f'{self.piso}')   # capacidad por habitacion segun el tipo
        self.price = ship.get('cost').get(f'{self.piso}')           # pricio de la habitacion segun el tipo 
        self.iva = 0.16                                             # impuestos
        self.habitaciones = self.av()                               # se llama la funcion donde el usuario elije sus habitaciones
        self.personas = self.reserv()                               # se llama la funcion donde el usuario indica las personas que viajaran
        self.total = self.calc_total()                              # se llama la fucnion que calcula el total
        self.mostrar()                                              # se imprime la reservacion
        
    def av(self): # func donde el usuario elije sus habitaciones
        habitaciones = []
        if self.cantidad == 0: # si la cantidad de personas es 0 se devuelve un error
            print(f"\n{error}")
            return
        if self.capacidad >= self.cantidad: # si la cantidad de personas es menor or igual a la capacidad de la habitacion solo se necesita 1
            print(f'\nSolo es necesaria una habitacion')
            cuartos = 1
        else:
            cuartos = math.ceil(self.cantidad/self.capacidad) # se divide las personas entre la capacidad y se redondea hacia arriba (ej: 10/4 = 2.5 son 3 habitaciones) 
            print(f'\nDebera reservar:\n>>> {cuartos} habitaciones <<<\n')
        disponibles = []
        for room, status in self.rooms.items(): # se chequean las habitaciones disponibles y se muestran al usuario para que seleccione
            if status == 0:
                disponibles.append(f'{room}')
        print(f'Habitaciones disponibles en piso: {self.piso}\n')
        print(f'{disponibles}\n')
        for cuarto in range(cuartos): # se pregunta que habitacion quiere segun el numero de habitaciones que se necesiten
            print(f'Ingrese el codigo de UNA habitacion que desea (ej: A1)')
            check = input(">>>> ").upper()
            if check in disponibles: # si todas las habitaciones que el usuario selecciono estan disponibles se guardan en la lista
                habitaciones.append(check)
            else:
                print(f"Codigo de habitacion ingresado incorrectamente") # si la persona ingresa el codigo mal o la habitacion no esta disponible 
                return
        return habitaciones

    def reserv(self): #func donde el usuario indica las personas que viajaran ( a su vez llama otra funcion que se encarga de tomar inputs persona por persona)
        cupos = self.cantidad # mal llamado cupos (se refiere a la cantidad que pidio el usuario)
        personas = []
        for habitacion in self.habitaciones: # por cada habitacion se preguntan las personas que se hospedan
            print(habitacion)
            if cupos >= self.capacidad:                         # si se necesitan mas cupos que la capacidad 
                for persona in range(self.capacidad):           # se muestra la cantidad de 'inscripciones' como la habitacion lo permita
                    personas.append(self.ingresar_persona())
            elif 1 <= cupos < self.capacidad:                    # si se necesitan menos cupos que la capacidad 
                for persona in range(cupos):                     # se muestra la cantidad de 'inscripciones' como el usuario necesite
                    personas.append(self.ingresar_persona())
            cupos -= self.capacidad  # se restan la cantidad de cupos ya usados y se repite
        return personas # si los cupos son 0 se termina la funcion

    def ingresar_persona(self): # funcion que toma los datos de la persona
        nombre = input('Nombre: ')
        dni = int(input('DNI: '))
        edad = int(input('Edad: '))
        print('Posee alguna discapacidad - [1] si [2] no')
        check_disc = int(input('>>>> '))
        if check_disc  == 1:
            discapacidad = 1
        elif check_disc  == 2:
            discapacidad = 0
        else:
            print(f"\n{error}")
        return [nombre, dni, edad, discapacidad]

    def calc_total(self):
        sub_total = (len(self.personas)*self.price) # sub_total sin ningun descuento (precio x persona)
        total = 0                                   # aqui se guardara el total con los descuentos
        for persona in self.personas:
            descuento = 0                   # ya que no sabia si se podian dar mas de un descuento o no, estos se suman
            if prime(persona[1]) == True:   # si la cedula de la persona es prima 10% descuento
                descuento += 0.10
            elif abundant(persona[1]) == True: # si la cedula de la persona es abundante 15% descuento
                descuento += 0.15
            if persona[3] == 1: # si la persona tiene alguna discapacidad 30 de descuento
                descuento += 0.30
            total += self.price - (self.price*descuento)    #se calcula el total de la persona y se suma al total de todas
        return [sub_total, total]

    def mostrar(self):
        print('\nReservacion:') # prints de informacion
        print(self.personas)
        print(self.habitaciones)
        print(f'Subtotal:{self.total[0]}')
        print(f'Descuentos:{self.total[0] - self.total[1]}')
        print(f'Total:{self.total[0]+(self.total[0]*self.iva)}')
        print(f'\nDesea Procesar la reservacion? [1] si [2] no')
        check_disc = int(input('>>>> '))
        if check_disc  == 1:
            return(self.procesar()) # si la persona acepta se procesa la reservacion
        elif check_disc  == 2:
            print('\n>>> Reservacion Cancelada')
            return
        else:
            print(f"\n{error}")

    def procesar(self): # funcion que procesa la infromacion
        reserva = []
        for persona in self.personas: # se agregan las personas a la resera
            reserva.append(persona)
        for habs in self.habitaciones: # se actualiza cada habitacion con las personas
            self.rooms.update({f'{habs}': reserva})
        json_habitaciones[self.numero].update({f'{self.piso}': reserva}) # se actualiza el piso
        with open("proyecto/data_rooms.txt", "w") as datos: # se escribe en el text file
            for ship in json_habitaciones:
                datos.write(f'{(ship)}\n')
                for cliente in clientes:
                    for persona in cliente:
                        datos.write(f'{persona}\n')

        
def prime(num): # funcion que chequea si un numero es primo
    if num > 1: 
        for i in range(2, num): 
            if (num % i) == 0: 
                return False
            else: 
                return True
    else: 
        return False  

def abundant(num): # funcion que chequea si un numero es abundante
    total = 0
    is_abundant = 0
    for i in range(1,num):
        if(num % i == 0):
            total = total + i 
            if(total > num):
                is_abundant = 1
                break

    if((total > num) or (is_abundant ==1)):
        return True
    else :
        return False
# RESERVAR -------------------------------------------------------------------------------------------------------------------------------------------
def reservar(ship,rooms,numero): # funcion que llama a la clase reservacion y pasa ciertos datos
    try:
        print(f'\nReservacion de habitaciones:\n({ship.get("name")})')
        print(f"\nSeleccione uno de los siguientes pisos:")
        print(f'{tipos[0]}\n{tipos[1]}\n{tipos[2]}')
        input_piso = int(input(">>>> "))
        if 1 <= input_piso <=3:
            print(f'\nIngrese la cantidad de personas que viajen:')
            cantidad = int(input(">>>> "))
            Reservacion(ship,rooms,input_piso,cantidad,numero)
        else:
            print(f"\n{error}")
    except:
            print(f"\n{error}")
    return

# DESOCUPAR -------------------------------------------------------------------------------------------------------------------------------------------
def desocupar(ship,rooms,numero): # funcion que desocupa la habitacion
    print(f'\nPara desocupar ingrese el codigo de la habitacion (ej: SA1):')
    check = input(">>>> ")
    if len(check) <= 4: # se chequea que el usuario ingreso un codigo valido(que no sea mas largo de lo permitido)
            check = check.upper() # se convierte a mayuscula
            if check[0] == 'S' or check[0].upper() == 'P' or check[0].upper() == 'V': # se chequea si el codigo es valido(que comience con una de las letras validas)
                tipo_piso = ind.get(check[0])   # se toma la letra y se busca a que piso se refiere
                piso = rooms.get(tipo_piso)     # se busca el piso 
                room = piso.get(check[1:])      # se busca la habitacion
                if room == 0:                   # si room es 0 quiere decir que esta vacio por lo que no hace falta vaciarlo
                    print(f'\n>>> Esta habitacion ya se encuentra desocupada <<<')
                else:                           # si room es cualquier otra cosa quiere decir que se encuentra ocupado
                    print(f'\nHabitacion ocupada por:')
                    for personas in room:       # se imprimen las personas que se encuentran en la habitacion
                        print(f'{personas}')
                    print(f'\nSeguro que quiere desocuparla: [1]si 2[no]')
                    seguro = input(">>>> ")     # se confirma que sea la habitacion
                    if int(seguro) == 1:
                        print(f'\n>>> Habitacion desocupada exitosamente <<<')
                        clientes.append(room)   # se guarda la informacion del cliente para la posterioridad
                        piso.update({f'{check[1:]}': 0}) # se establece la habitacion como 0 (desocupada)
                        json_habitaciones[numero].update({f'{tipo_piso}': piso})
                        with open("proyecto/data_rooms.txt", "w") as datos: # se actualiza el text file
                            for ship in json_habitaciones:
                                datos.write(f'{(ship)}\n')
                            for cliente in clientes:
                                for persona in cliente:
                                    datos.write(f'{persona}\n')
                        
                    elif int(seguro) == 2: # si no es la habitacion se cancela
                        print(f'\n>>> Cancelado <<<')
                    else:
                        print(f"\n{error}")
                return
            else:
                print(f"\n{error}")
    return

# BUSCAR -------------------------------------------------------------------------------------------------------------------------------------------
def buscar(ship,rooms,numero):
    capacidad = ship.get('capacity') # se toma la capacidad de las habitaciones 
    print(f'\nPara buscar una habitacion ingrese; tipo de habitacion (simple,premium,vip), capacidad o codigo (ej: SA10):')
    check = input(">>>> ") # se toma el input
    posibles = [] # aqui se guardaran las posibles habitaciones
    try:                    # trata de convertir el input a un int, de no poderse se pasa al 'except'
        check = int(check)                    # si el input si es un int quiere decir que el usuario esta buscando habitaciones por capacidad
        for tipo, cap in capacidad.items():   # se buscan los tipos de habitaciones que pueden hospedar esa capacidad (asi alla espacio de sobra)
            if check <= cap:    
                posibles.append(tipo)         # se agregan los tipos de habitaciones posibles a la lista
        if posibles == []:                    # si la lista esta vacia quiere decir que no hay posibles
            print('No hay habitaciones con esa capacidad o no estan disponibles')
    except:    # si el input no es un int 
        if len(check) <= 4 and check != 'vip':        # se prueba si el input tiene 4 o menos caracteres y no es 'vip'
            check = check.upper()  # se coniverte a mayuscula el input
            if check[0] == 'S' or check[0].upper() == 'P' or check[0].upper() == 'V': # se chequea si el codigo es valido(que comience con una de las letras validas)
                tipo_piso = ind.get(check[0]) # de serlo se toma la letra y se busca a que piso se refiere
                piso = rooms.get(tipo_piso)   # se busca el piso 
                room = piso.get(check[1:])    # se busca la habitacion
                if room == 0:                 # si es igual a 0 quiere decir que esta disponible
                    print(f'\n>>> Habitacion Disponible <<<')
                else:                           
                    print(f'\nHabitacion ocupada por:') # si no es igual a 0 se impremen las personas que ocupan la habitacion
                    for personas in room:
                        print(f'{personas}')
                return
            else:
                print(f"\n{error}")
        elif check.lower() == 'simple' or check == 'premium' or check == 'vip': # si el input no es un int  o un codigo de habitacion
            posibles.append(check) # se agrega el input a la lista de posibles
        else:
            print(f"\n{error}")
    
    disponibles = []
    for piso in posibles: # se busca el la lista de posibles las habitaciones disponiles y se impremen
        for room, status in rooms.get(piso).items():
            if status == 0:
                for abv, tipo_piso in ind.items():
                    if piso == tipo_piso:
                        disponibles.append(f'{abv}{room}')

    print(f"\nHabitaciones disponibles (S = simple, P = premium, V = vip):{disponibles}")
    return

# MAIN -----------------------------------------------------------------------------------------------------------------------
options = {1: reservar, 2: desocupar, 3: buscar}
def habitaciones(ship,numero):
    rooms = json_habitaciones[numero]
    while True:
        print(line)
        print(f"\nModulo de Gestion de Habitaciones, aqui podra consultar las habitaciones disponibles;\n")
        try:
            print(f"Seleccione una de las siguientes opciones:")
            print(f'{opciones[0]}\n{opciones[1]}\n{opciones[2]}\n{opciones[3]}\n{opciones[4]}')
            check = int(input(">>>> "))
            if 2 <= check <= 4:
                options[check-1](ships[numero],rooms,numero)
            elif check == 1:
                print(f"\nSeleccione uno de los siguientes pisos (habitaciones ocupadas se mostraran tachadas):")
                print(f'{tipos[0]}\n{tipos[1]}\n{tipos[2]}')
                input_piso = int(input(">>>> "))
                piso = types.get(input_piso)
                print(f'\n{Piso(rooms, piso).chequear()}')
            elif check == 5:
                break
            else:
                print(f"\n{error}")
        except:
            print(f"\n{error}")


# NOTAS
# 2.a) no se le pregunta al usuario barco o destino ya que se seleccionado al comenzar el programa
# 2.d.iii.1) no se implemento el upgrade a los mayores de 65+ ya que por la forma como se manejan las habitaciones y las personas no daba tiempo de implementarlo
#            el upgrade eso para todos? o solo para la persona? que pasa si no hay habitaciones premium disponibles?
#            que pasa si son 4 +65 y no caben en una sola simple pero sin en una sola premium? se les dan dos premium?