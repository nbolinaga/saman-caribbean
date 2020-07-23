# Se importa cada Modulo 
import requests
from cruceros import cruceros
from habitaciones import habitaciones
from tours import tours
from restaurant import restaurant
from estadisticas import estadisticas


ops = ['[1] Gestion de Cruceros.','[1] Gestion de Habitaciones.','[2] Venta de Tours.','[3] Menu Restaurant.','[4] Estadisticas.','Salir.',]
error = '>>> Dato ingresado incorrectamente, intente de nuevo. <<<\n'
bye  = '>>> ¡Gracias por usar el sistema automatizado de Samán Caribbean! <<<'
line = '_________________________________________________________________________________________________________________________________________________'

# Dict con las respuestas a las opciones del menu, estas actuan como un "switch" en otro lenguaje 
options = {1: habitaciones, 2: tours, 3: restaurant, 4: estadisticas}

def opciones(ship,ship_number):
    while True:
        print(f'\nBienvenido a bordo de: {ship}')
        print(f'{ops[1]}\n{ops[2]}\n{ops[3]}\n{ops[4]}\n[5] {ops[5]}')
        try:
            check = int(input(">>>> "))     # el usuario ingresa un input segun la opcion que desee
            if 1 <= check <= 4:             # si la opcion es del 1 al 4 se llama al dict y se ejecuta la funcion correspondiente
                options[check](ship, ship_number)   
            elif check == 5:                # si la opcion es 5 (salir) se cierra el programa
                print(f"\n{bye}")
                break
            else:                           # si el input no esta entre 1 y 5, o no es un numero se imprime un mensaje de error
                print(f"\n{error}")
        except:
            print(f"\n{error}")

def menu():
    while True:
        i = 1                               # variable para contabilizar los cruceros
        print(line)                         
        print(f'\nBienvenido al sistema automatizado de Samán Caribbean. A continuacion se le mostraron los cruceros disponibles;')         
        ships = cruceros()                  # se llama la funcion cruceros y se retornan los nombres de cada uno
        print(f'Seleccione uno de los cruceros disponibles (inserte solo el numero):')                 
        for crucero in ships:               # se impreme cada crucero con su numero y la opcion de salir
            print(f"[{i}] {crucero}")
            i += 1
        print(f"[{i}] {ops[5]}")                
        try:
            selection = int(input(">>>> "))                         # el usuario debe seleccionar un numero (crucero o salir)
            if 1 <= selection <= len(ships):                        # se chequea si el input esta entre uno o el numero de cruceros  
                print(f'\nUsted ha seleccionado:')
                print(f'>>> {ships[selection-1]} <<<\n')
                print('Confirme su eleccion: [1]Aceptar [2]Cancelar')
                check = int(input(">>>> "))                         # se chequea si la opcion es correcta
                if check == 1:
                    opciones(ships[selection-1],(selection-1))      # si es correcta se llama la funcion opciones
                elif check == 2:                                    # si se cancela la seleccion se vuelve al principio
                    pass
                else:
                    print(f"\n{error}")
            elif selection == (len(ships)+1):                       # si se seleccion "salir" se imprime un mensaje y se cierra el programa
                print(f"\n{bye}")
                break
            else:                           
                print(f"\n{error}")
        except:
           print(f"\n{error}")
menu()



      