# imports ----------------------------------------------------------------------------------------------------------------------------------------------------
import requests
ships = requests.get("https://saman-caribbean.vercel.app/api/cruise-ships").json()

# DATA -------------------------------------------------------------------------------------------------------------------------------------------------------
data = None
lim = [10, 100, 'No Hay Limite', 15]

def crear_text(): # funcion que crea el text file 
    with open("proyecto/data_tours.txt", "w+") as datos:
        for ship in ships:
            datos.write(",".join(map(str, lim)))   
            datos.write('\n')                      
        datos.write('\n') 

try: # se trata de abrir el text file, si no existe retorna un error
    with open("proyecto/data_tours.txt", "r+") as datos:
        data = datos.read().splitlines() 
except: # en caso de error se llama a la funcion crear_text()
    crear_text()
    with open("proyecto/data_tours.txt", "r+") as datos:
        data = datos.read().splitlines() 

# CONSTANTES ----------------------------------------------------------------------------------------------------------------------------------------------------
cupos = data[0:5]
error = '>>> Dato ingresado incorrectamente, intente de nuevo. <<<\n'
mensaje = '\nModulo de Venta de Tours, aqui podra consultar los tours disponibles;\n'
line = '_________________________________________________________________________________________________________________________________________________'

limite = [4, 2, " ", 4] 
precios = [30, 100, 0, 40] 
horas = ["7 A.M", "12 P.M", "6 A.M", "10 A.M"]

# VARIABLES ------------------------------------------------------------------------------------------------------------------------------------------------------
av = [cupos[0].split(','),cupos[1].split(','),cupos[2].split(','),cupos[3].split(',')] # Cupos disponibles, se extraen del txt file de base de datos.
reservaciones = data[5: ]

# CLASE ---------------------------------------------------------------------------------------------------------------------------------------------------------
class Tour():
    def __init__(self, dni, tour, cantidad, limite, precio, horario, ship_number, int_av):
        self.dni = dni
        self.tour_num = tour
        self.disponibles = int_av[tour-1] # se extrae solo los cupos del tour seleccionado (tour-1 ya que index empieza en 0)
        self.pedidos = cantidad
        self.limites = limite[tour-1]
        self.precio = precio[tour-1]
        self.horario = horario[tour-1]
        self.number = ship_number
        self.cupos = int_av

    # funcion para chequear si hay cupos 
    def check_cupos(self): 
        if type(self.disponibles) == int:   # si los cupos disponiples no son un numero, automaticamente sabemos que es el tour que no tiene limite de cupos(tour 3).
            if self.pedidos == 0:           # si la persona pide 0 cupos simplemente no se tomo en cuenta
                return(f"\n{error}")  
            if self.limites < self.pedidos: # si la persona pide mas cupos de los que se permiten por reserva retorna un mensaje (error).
                return(f"\n>>> Limite de personas por reservacion excedido, intente de nuevo <<<\nLimite: {self.limites}\n")                                                                                                                               
            else:
                if self.disponibles < self.pedidos: # si la persona pide mas cupos de los que hay disponibles retorna un mensaje (error).
                    return(f"\n>>> Tour no disponible o se han acabado los cupos <<<\nDisponibles: {self.disponibles}\n")
                else:
                    return self.procesar_resv() # si se cumplen todos los requisitos se pasa a la funcion donde se procesara la informacion (restar cupos y precio total)
        else:
            return self.procesar_resv()     # si es el tour 3 pasamos directo a procesar

    # funcion que procesa la reservacion
    def procesar_resv(self):
        descuento = 0.1 
        if self.tour_num == 1 or self.tour_num == 4: # si el tour es el 1 o el 4 aplicamos descuento (siempre y cuando se reserven mas de 2 cupos). 
            if self.pedidos < 3: 
                total = self.pedidos * self.precio # si son 2 o menos se calcula el total sin descuento y se imprime los detalles de la reservacion.
                print(f"\nDNI:{self.dni} - Personas:{self.pedidos} - Total:{total} - Hora:{self.horario}")
                return self.guardar(total)

            else:
                con_descuentos = (self.pedidos - 2) * (self.precio * descuento) # cupos - 2 nos da los cupos que llevan descuento (3 o 4) y se le aplica el precio con descuento.
                sin_descuentos = 2 * self.precio # se calcula el precio de cupos sin descuento
                total = con_descuentos + sin_descuentos # se suman el precio de todos los cupos y se imprime los detalles de la reservacion.
                print(f"\nDNI:{self.dni} - Personas:{self.pedidos} - Total:{total} - Hora:{self.horario}")
                return self.guardar(total)

        else:
            total = self.pedidos * self.precio # si no llevan descuento simplemente se calcula el total y  se imprime los detalles de la reservacion.
            print(f"\nDNI:{self.dni} - Personas:{self.pedidos} - Total:{total} - Hora:{self.horario}")
            return self.guardar(total)
   
    # funcion que pasa la informacion a la base de datos(guarda)
    def guardar(self,total):
        print(f'Confirme la reservacion: [1]Procesar [2]Eliminar\n') # pregunta si desea guardar la reservacion o cancelarla
        while True:
            try:
                confirmacion = int(input(">>>> "))
                if confirmacion == 1: # si se decide guardar, se modifica la base de datos en base a lo reservado
                    self.cupos[self.tour_num-1] -= self.pedidos # restamos los cupos pedidos a los disponibles
                    reservaciones.append(f'DNI:{self.dni} - Personas:{self.pedidos} - Total:{total} - Hora:{self.horario}') # se agrega la nueva reservacion a las anteriores
                    av[self.number] = self.cupos  # se agregan los cupos actualizados a la lista 
                    with open("proyecto/data_tours.txt", "w") as datos: # abrimos el documento en modo "write"
                        for ship in av:
                            datos.write(",".join(map(str, ship)))   # se escriben los cupos de cada tour separado por una comma 
                            datos.write('\n')                       # se escriben los cupos del siguiente barco 
                        datos.write('\n')                           # linea vacia
                        for reservacion in reservaciones:
                            datos.write(f'{reservacion}\n') # se re-escriben las reservaciones, mas las nuevas
                    return('>>> Tour reservado exitosamente <<<')
                elif confirmacion == 2: # si se cancela simplemente se descarta todo y no se modifica la base de datos
                    return('>>> Reservacion cancelada <<<')
                    
                else:
                    print(f"\n{error}")
            except:
                print(f"\n{error}")

# MENU MODULO --------------------------------------------------------------------------------------------------------------------------------------------------------
def tours(ship,number):
    tours = ['1 ● Tour en el puerto: el precio es de $30/persona, hasta 4 personas, con descuento de 10% para la tercera y cuarta; empieza a las 7 A.M.','2 ● Degustación de comida local: el precio es de $100/persona, empieza a las 12 P.M y es hasta 2 personas.','3 ● Trotar por el pueblo/ciudad: es gratis, empieza a las 6 A.M.','4 ● Visita a lugares históricos, el precio es de $40/personas, con descuento de 10% a partir de la tercera; empieza a las 10 A.M y es hasta 4 personas.']
    int_av = [int(ele) if ele.isdigit() else ele for ele in av[number]]
    while True:
        print(line)
        print(f"{mensaje}\n{tours[0]}\n>>> disponibilidad: {int_av[0]} <<<\n\n{tours[1]}\n>>> disponibilidad: {int_av[1]} <<<\n\n{tours[2]}\n>>> disponibilidad: {int_av[2]} <<<\n\n{tours[3]}\n>>> disponibilidad: {int_av[3]} <<<")
        try:
            print(f"\nIndique el DNI del cliente (presione solo ENTER para salir):")
            dni = input(">>>> ")
            if dni == "":
                return
            print(f"\nIndique el numero del tour que desea:")
            tour = int(input(">>>> "))
            print(f"\n{tours[tour-1]}\nDisponibilidad:{int_av[tour-1]}")
            if 1 <= tour <= 4:
                print(f"\nIndique el numero de personas que tomaran el tour:")
                personas = int(input(">>>> "))
                print(Tour(dni, tour, personas, limite, precios, horas, number, int_av).check_cupos())
            else:   
                print(f"\n{error}")
                continue
        except:
            print(f"\n{error}")