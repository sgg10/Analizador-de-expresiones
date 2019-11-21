from programa import ejecutar
import os

def verInstrucciones():
    mensaje = "La calculado tiene 2 modos: \n"
    mensaje += "1. Modo dinamico : aqui podras evaluar las expresiones que gustes (incluye funciones).\n"
    mensaje += "2. Modo Fichero : aqui podras evaluar las expresiones que hay en un archivo de texto.\n\n"
    mensaje += "Diviertete calculando :)\n\n----------------------------------------\n"
    mensaje += "Calculadora realizada por Sebastian Granda"
    print (mensaje)

def verMenu():
    menu = "1. Ingresar\n"
    menu += "2. Ver instrucciones\n"
    menu += "9. Salir\n-------------------------------------------\n"
    menu += "Ingrese una opcion: "
    opt = input(menu)
    return opt

def limpiar():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

opt = 0

while opt != "9":
    opt = verMenu()
    if opt == "1":
        limpiar()
        ejecutar()
    elif opt == "2":
        limpiar()
        verInstrucciones()
    else: 
        print ("Opcion no valida")

limpiar()
