# imports ----------------------------------------------------------------------------------------------------------------------------------------------------
import requests
import json
# DATA -------------------------------------------------------------------------------------------------------------------------------------------------------
data = None
def crear_text(): # funcion que crea el text file 
    with open("proyecto/data_menu.txt", "w+") as datos:
        for ship in range(4):
            datos.write('{' + '}\n')

try: # se trata de abrir el text file, si no existe retorna un error
    with open("proyecto/data_menu.txt", "r+") as datos:
        data = datos.read().splitlines()
except: # en caso de error se llama a la funcion crear_text()
    crear_text()
    with open("proyecto/data_menu.txt", "r+") as datos:
        data = datos.read().splitlines() 

# CONSTANTES --------------------------------------------------------------------------------------------------------------------------------------------------
error = '>>> Dato ingresado incorrectamente, intente de nuevo. <<<\n'
line = '_________________________________________________________________________________________________________________________________________________'
# VARIABLES --------------------------------------------------------------------------------------------------------------------------------------------------
ships = data[:5]

# Clase para los productos --------------------------------------------------------------------------------------------------------------------------------------------------
class Producto():
    def __init__(self,nombre,clasificacion,tipo,precio,productos):
        self.iva = 0.16
        self.nombre = nombre.capitalize() # capitalize se encarga de que siempre este en mayuscula la primera letra
        self.clasificacion = clasificacion
        self.tipo = tipo
        self.precio = precio + (precio*self.iva) # se calcula el iva
        self.productos = productos

    def anadir(self):
        self.productos[f'{self.nombre}'] = [[self.clasificacion, self.tipo], self.precio] # se agrega el procuto como un diccionario al dict de productos
        return(self.productos) # se retorna el dict de productos

# Clase para los combos --------------------------------------------------------------------------------------------------------------------------------------------------
class Combos():
    def __init__(self,nombre,items,precio,productos):
        self.iva = 0.16
        self.nombre = nombre
        self.items = items
        self.precio = precio + (precio*self.iva)
        self.individuales = []
        self.productos = productos

    def anadir(self):
        for item in self.items:
            producto = self.productos.get(f'{item}')    # si no se encuentra el producto en la lista se retorna un mensaje de error
            if producto == None:
                print(f'\n>>> Uno o mas productos no encontrado en el menu <<<')
                return
            else:
                self.individuales.append({item: producto}) # si se encuentra el producto se agrega a la lista

        self.productos[f'{self.nombre}'] = [self.individuales, self.precio] # se agrega el combo al dict de productos
        print('\n>>> Agregado exitosamente <<<')
        return(self.productos) # se retorna el dict de productos

# Funciones--------------------------------------------------------------------------------------------------------------------------------------------------
def get_info(nombre,productos): # funcion que toma la informacion del producto que quiere agregar o modificar el usuario
    print('Clasificacion - [1] bebida [2] comida')
    clasificacion = int(input('>>>> '))
    if clasificacion == 1:
        clasificacion = 'bebida'
        print('Tamaño - [1] pequeña [2] mediana [3] grande')
        check_tamano = int(input('>>>> '))
        if check_tamano == 1:
            tipo = 'pequeña'
        elif check_tamano == 2:
            tipo = 'mediana'
        elif check_tamano == 3:
            tipo = 'grande'
        else:
            print(f"\n{error}")
            return
    elif clasificacion == 2:
        clasificacion = 'comida'
        print('Tipo - [1] empaquetada [2] preparada')
        check_tipo = int(input('>>>> '))
        if check_tipo == 1:
            tipo = 'empaquetada'
        elif check_tipo == 2:
            tipo = 'preparada'
        else:
            print(f"\n{error}")
            return
    precio = int(input('Precio: '))
    print(f'\n{nombre}: {clasificacion}-{tipo} ${precio} (sin iva)')
    print('[1] Confirmar [2] Cancelar')
    check = int(input('>>>> '))
    if check == 1:
        return(Producto(nombre,clasificacion,tipo,precio,productos).anadir()) # se llama a la clase producto
    elif check == 2:
        print('\n>>> Cancelado <<<')
        return
    else:
        print(f"\n{error}")
        return


def agregar_p(productos): # funcion para agregar un producto
    print('\nIngrese el producto que desea agregar:')
    nombre = input('Nombre: ')
    print('\n>>> Agregado exitosamente <<<')
    return(get_info(nombre,productos)) # solo pregunta el nombre del porducto y se llama a la funcion get_info


def eliminar_p(productos): # funcion para eliminar productos
    print('Menu:')
    for key in productos.keys():
        print(key) #imprime el menu completo
    print('\nIngrese el nombre del producto que desea eliminar:')
    nombre = input('>>> ').capitalize()
    productos.pop(nombre, None) # simplemente buscar el nombre en el dict y lo elimina
    print(f'\n>>> {nombre} eliminado exitosamente <<<')
    return


def modificar_p(productos): # funcion para modificar un producto
    print('Menu:')
    for key in productos.keys():
        print(key) #imprime el menu completo
    print('\nIngrese el nombre del producto que desea modificar:')
    nombre = input('>>> ').capitalize()
    productos.pop(nombre, None) # esta funcion lo que hace es eliminar el producto y remplazarlo con la informacion nueva
    print(f'\n>>> {nombre} modificado exitosamente <<<')
    return(get_info(nombre,productos)) # solo pregunta el nombre del producto a modificar y se llama a la funcion get_info


def agregar_c(productos): # funcion para crear combos
    combo = []
    print('\nIngrese el nombre del combo que desea crear:')
    nombre = input('>>> ').capitalize()
    print('Ingrese el numero de productos en el combo:')
    cantidad = int(input('>>> '))
    print('\nMenu:')
    for key in productos.keys():
        print(key) #imprime el menu completo
    for producto in range(cantidad): # pregunta el nombre del producto el numero de veces que indico el usuario
        print(f'\nIngrese el nombre del producto {producto+1}:')
        nombre_producto = input('>>> ').capitalize()
        combo.append(nombre_producto) # se agrega el producto a una lista
    precio = int(input('Precio del combo: '))
    print(f'\n{combo}  ${precio}')
    print('[1] Confirmar [2] Cancelar')
    check = int(input('>>>> '))
    if check == 1:
        return(Combos(nombre,combo,precio,productos).anadir()) # se pasa la lista a la clase para procesar la informacion
    elif check == 2:
        print('\n>>> Cancelado <<<')
        return
    else:
        print(f"\n{error}")
        return
    return


def eliminar_c(productos): # funciona al igual que eliminar productos
    print('Menu:')
    for key in productos.keys():
        print(key)
    print('\nIngrese el nombre del combo que desea eliminar:')
    nombre = input('>>> ').capitalize()
    productos.pop(nombre, None)
    print(f'\n>>> {nombre} eliminado exitosamente <<<')
    return


def buscar(productos): # funcion para buscar la informacion de un producto
    print('Menu:')
    for key in productos.keys():
        print(key)
    print('\nIngrese el producto/combo que desea buscar:')
    nombre = input('Nombre: ').capitalize()
    producto = productos.get(f'{nombre}') # busca el producto en el dict si no lo encuentra se impreme un error
    if producto == None:
        print(f'\n>>> Producto o Combo no encontrado en el menu <<<')
    else:                                       
        print(f'>>> {nombre}: {producto[0][0]} {producto[0][1]} / Precio: ${producto[1]} <<<')  # si lo encuentra se impreme la informacion del producto
    return


# MAIN --------------------------------------------------------------------------------------------------------------------------------------------------
options = {1: agregar_p, 2: eliminar_p, 3: modificar_p, 4: agregar_c, 5: eliminar_c, 6: buscar}
def restaurant(ship, ship_number):
    productos = ships[ship_number]
    productos = productos.replace("'", '"')
    productos =  json.loads(productos)
    while True:
        print(line)    
        print('Bienvenido al restaurant, seleccionado una de las siguientes opciones:')
        print(f'[1]Agregar producto\n[2]Eliminar producto\n[3]Modificar producto\n[4]Agregar combo\n[5]Eliminar combo\n[6]Buscar producto/combo\n[7]Salir')
        try:
            check = int(input(">>>> "))    
            if 1 <= check <= 6:             
                ships[ship_number] = options[check](productos)
                with open("proyecto/data_menu.txt", "w") as datos: 
                    for ship in ships:
                        print(ship)
                        datos.write(f'{ship}\n')   
                        datos.write('\n')  
            elif check == 7:                
                return
            else:                          
                print(f"\n{error}")
        except:
            print(f"\n{error}")

# NOTAS
# la API proporciona productos para la venta pero la rubrica no indicaba que hacer con ellos por lo que se decidio obviarlos