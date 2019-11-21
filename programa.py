from analizador import Parser

litaNoVariables = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sqrt',
        'log', 'abs', 'ceil', 'floor', 'round', 'exp', "and", "or", 'random', 'fac', 'min',
        'max', 'pyt', 'pow', 'atan2', 'concat', 'if', 'E', 'PI']

def calcularFuncion(exp, dic):
    par = Parser()
    return par.parse(exp).evaluar(dic)

def ejecutar():
    opt = input("Digite 1 para entrar en el modo interactivo o 2 para leer un fichero: ")
    par = Parser()
    if opt == "1":
        print ("Cuando quiera cambiar de modo, digite la letra c")
        while True:
            exp = input('> ') #-> Usar esta line si se encuntra en la version de python 3.X
            #exp = raw_input('> ') #Esta linea se usa en python 2.X debido a que la funcion input puede generar error
            if exp == "c":
                break
            variables = [] #Lista que contendra las variables que se usaron en la expresion
            valores = [] #Lista que contendra los valores respectivos a cada variable

            #Estas lista omitira las palabras que no son variables al analizar si es funcion o no
            expSeparar = ''
            cont = 0
            for noVariable in litaNoVariables:
                if cont == 0:
                    expSeparar = exp.replace(noVariable, '')
                    cont += 1
                expSeparar = expSeparar.replace(noVariable, '')
            for caracter in expSeparar: # Ciclo para obtener las variables
                if ((caracter >= 'a' and caracter <= 'z') or (caracter >= 'A' and caracter <= 'Z')):
                    if caracter in variables:
                        pass
                    else:
                        variables.append(caracter)
            for variable in variables: #Ciclo para darle valores a cada variable
                valores.append(input("Ingrese el valor que tendra " + variable + ": "))
            
            #Generar diccionario que se pasa por parametro y evaluar la funcion
            dic = {}
            for i in range (0, len(variables)):
                dic.update({variables[i]: valores[i]})
            
            resultado = calcularFuncion(exp, dic)
            print(resultado)
    elif opt == "2":
        archivo = open("expresiones.txt", 'r')
        linea = archivo.readline()
        while linea != '':
            valor = par.parse(linea).evaluar({})
            print(linea + " = " + str(valor))
            linea = archivo.readline()
            print