from __future__ import division
import math
import random
import io

TNUMERO = 0
TOP1 = 1
TOP2 = 2
TVAR = 3
TLLAMADOFUNCION = 4

#================CLASE TOKEN=============================
class Token():
    def __init__(self, tipo_, index_, prio_, numero_): #prio = prioridad
        self.tipo_ = tipo_
        self.index_ = index_ or 0
        self.prio_ = prio_ or 0
        self.numero_ = numero_ if numero_ != None else 0

    def toString(self):
        if self.tipo_ == TNUMERO:
            return self.numero_
        if self.tipo_ == TOP1 or self.tipo_ == TOP2 or self.tipo_ == TVAR:
            return self.index_
        elif self.tipo_ == TLLAMADOFUNCION:
            return 'Llamado'
        else:
            return 'Token invalido'
#================FIN CLASE TOKEN=========================

#================CLASE EXPRESION=========================
class Expresion():
    def __init__(self, tokens, ops1, ops2, funciones):
        self.tokens = tokens #SERA UNA LISTA
        self.ops1 = ops1
        self.ops2 = ops2
        self.funciones = funciones

    def simplificar(self, valores):
        valores = valores or {}
        nStack = []
        nuevaExpresion = []
        L = len(self.tokens)
        for i in range(0, L):
            item = self.tokens[i]
            tipo_ = item.tipo_
            if tipo_ == TNUMERO:
                nStack.append(item)
            elif tipo_ == TVAR and item.index_ in valores:
                item = Token(TNUMERO, 0, 0, valores[item.index_])
                nStack.append(item)
            elif tipo_ == TOP2 and len(nStack) > 1:
                n2 = nStack.pop()
                n1 = nStack.pop()
                f = self.ops2[item.index_]
                item = Token(TNUMERO, 0, 0, f(n1.numero_, n2.numero_))
                nStack.append(item)
            elif tipo_ == TOP1 and nStack:
                n1 = nStack.pop()
                f = self.ops1[item.index_]
                item = Token(TNUMERO, 0, 0, f(n1.numero_))
                nStack.append(item)
            else:
                while len(nStack) > 0:
                    nuevaExpresion.append(nStack.pop(0))
                nuevaExpresion.append(item)
        while nStack:
            nuevaExpresion.append(nStack.pop(0))

        return Expresion(nuevaExpresion, self.ops1, self.ops2, self.funciones)

    def sustituir(self, variable, exp):
        if not isinstance(exp, Expresion):
            exp = Parser().parse(str(exp))
        nuevaExpresion = []
        L = len(self.tokens)
        for i in range(0, L):
            item = self.tokens[i]
            tipo_ = item.tipo_
            if tipo_ == TVAR and item.index_ == variable:
                for j in range(0, len(exp.tokens)):
                    expItem = exp.tokens[j]
                    replItem = Token(expItem.tipo_, expItem.index_, expItem.prio_, expItem.numero_)
                    nuevaExpresion.append(replItem)
            else:
                nuevaExpresion.append(item)

        ret = Expresion(nuevaExpresion, self.ops1, self.ops2, self.funciones)
        return ret

    def evaluar(self, valores):
        valores = valores or {}
        nStack = []
        for item in self.tokens:
            tipo_ = item.tipo_
            if tipo_ == TNUMERO:
                nStack.append(item.numero_)
            elif tipo_ == TOP2:
                n2 = nStack.pop()
                n1 = nStack.pop()
                f = self.ops2[item.index_]
                nStack.append(f(n1, n2))
            elif tipo_ == TVAR:
                if item.index_ in valores:
                    nStack.append(valores[item.index_])
                elif item.index_ in self.funciones:
                    nStack.append(self.funciones[item.index_])
                else:
                    raise Exception('Variable indefinida: '+ item.index_)
            elif tipo_ == TOP1:
                n1 = nStack.pop()
                f = self.ops1[item.index_]
                nStack.append(f(n1))
            elif tipo_ == TLLAMADOFUNCION:
                n1 = nStack.pop()
                f = nStack.pop()
                if callable(f):
                    if type(n1) is list:
                        nStack.append(f(*n1))
                    else:
                        nStack.append(f(n1))
                else:
                    raise Exception(f + ' no es una funcion')
            else:
                raise Exception('Expresion invalida')
        if len(nStack) > 1:
            raise Exception('Expresion invalida')
        return nStack[0]

    def toString(self, toJS = False):
        nStack = []
        L = len(self.tokens)
        for i in range(0, L):
            item = self.tokens[i]
            tipo_ = item.tipo_
            if tipo_ == TNUMERO:
                if type(item.numero_) == str:
                    nStack.append("'"+item.numero_+"'")
                else:
                    nStack.append(item.numero_)
            elif tipo_ == TOP2:
                n2 = nStack.pop()
                n1 = nStack.pop()
                f = item.index_
                if toJS and f == '^':
                    nStack.append('math.pow(' + n1 + ',' + n2 + ')')
                else:
                    frm = '({n1}{f}{n2})'
                    if f == ',':
                        frm = '{n1}{f}{n2}'
                    nStack.append(frm.format(n1=n1, n2=n2, f=f))
            elif tipo_ == TVAR:
                nStack.append(item.index_)
            elif tipo_ == TOP1:
                n1 = nStack.pop()
                f = item.index_
                if f == '-':
                    nStack.append('(' + f + n1 + ')')
                else:
                    nStack.append(f + '(' + n1 + ')')
            elif tipo_ == TLLAMADOFUNCION:
                n1 = nStack.pop()
                f = nStack.pop()
                nStack.append(f+'(' + n1 + ')')
            else:
                raise Exception('Expresion invalida')
        if len(nStack) > 1:
            raise Exception('Expresion invalida')
        return nStack[0]

    def __str__(self):
        return self.toString()
    
    def simbolos(self):
        vars = []
        for i in range(0, len(self.tokens)):
            item = self.tokens[i]
            if item.tipo_ == TVAR and not item.index_ in vars:
                vars.append(item.index_)
        return vars

    def variables(self):
        return [var for var in self.variables() if var not in self.funciones]
#================FIN CLASE EXPRESION=====================

#================CLASE PARSER============================
class Parser:
    class Expresion(Expresion):
        pass

    PRIMARIO        = 1
    OPERADOR        = 2
    FUNCION         = 4
    PARENTESIS_A    = 8 #Parentesis Abre
    PARENTESIS_C    = 16 #Parentesis Cierra
    COMA            = 32
    SIGN            = 64
    CALL            = 128
    NULLARY_CALL    = 256

    def suma(self, a, b):
        return a + b

    def resta(self, a, b):
        return a - b

    def multiplicacion(self, a, b):
        return a * b

    def division(self, a, b):
        return a / b

    def modulo(self, a, b):
        return a % b

    def concat(self, a, b, *args):
        resultado = u'{0}{1}'.format(a, b)
        for arg in args:
            resultado = u'{0}{1}'.format(resultado, arg)
        return resultado

    def igual(self, a, b):
        return a == b

    def noIgual(self, a, b):
        return a != b

    def mayorQue(self, a, b):
        return a > b

    def menorQue(self, a, b):
        return a < b
    
    def mayorIgualQue(self, a, b):
        return a >= b

    def menorIgualQue(self, a, b):
        return a <= b

    def operadorY(self, a, b):
        return (a and b)

    def operadorO(self, a, b):
        return (a or b)

    def negativo(self, a):
        return -a

    def aleatorio(self, a):
        return random.random() * (a or 1)

    def factorial(self, a):
        return math.factorial(a)

    def pyt(self, a, b):
        return math.sqrt(a * a + b * b)

    def siFuncion(self, a, b, c):
        return b if a else c

    def append(self, a, b):
        if type(a) != list:
            return [a, b]
        a.append(b)
        return a

    def __init__(self):
        self.exito = False
        self.msgError = ''
        self.expresion = ''

        self.pos = 0

        self.numeroTokens = 0
        self.tokenPrio = 0
        self.tokenIndex = 0
        self.tempPrio = 0

        self.ops1 = {
            'sin' : math.sin,
            'cos' : math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sqrt': math.sqrt,
            'log': math.log,
            'abs': abs,
            'ceil': math.ceil,
            'floor': math.floor,
            'round': round,
            '-': self.negativo,
            'exp': math.exp,
        }

        self.ops2 = {
            '+': self.suma,
            '-': self.resta,
            '*': self.multiplicacion,
            '/': self.division,
            '%': self.modulo,
            '^': math.pow,
            ',': self.append,
            '||': self.concat,
            '==': self.igual,
            "!=": self.noIgual,
            ">": self.mayorQue,
            "<": self.menorQue,
            ">=": self.mayorIgualQue,
            "<=": self.menorIgualQue,
            "and": self.operadorY,
            "or": self.operadorO
        }

        self.funciones = {
            'random': random,
            'fac': self.factorial,
            'min': min,
            'max': max,
            'pyt': self.pyt,
            'pow': math.pow,
            'atan2': math.atan2,
            'concat':self.concat,
            'if': self.siFuncion
        }

        self.constantes = {
            'E': math.e,
            'PI': math.pi,
        }

        self.valores = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sqrt': math.sqrt,
            'log': math.log,
            'abs': abs,
            'ceil': math.ceil,
            'floor': math.floor,
            'round': round,
            'random': self.aleatorio,
            'fac': self.factorial,
            'exp': math.exp,
            'min': min,
            'max': max,
            'pyt': self.pyt,
            'pow': math.pow,
            'atan2': math.atan2,
            'E': math.e,
            'PI': math.pi
        }
    
    def parse(self, exp):
        self.msgError = ''
        self.exito = True
        stackOperadores = []
        stackTokens = []
        self.tempPrio = 0
        esperado = self.PRIMARIO | self.PARENTESIS_A | self.FUNCION | self.SIGN
        noOperadores = 0
        self.expresion = exp
        self.pos = 0

        while self.pos < len(self.expresion):
            if self.esOperador():
                if self.isSing() and esperado & self.SIGN:
                    if self.esSignoNegativo():
                        self.tokenPrio = 5
                        self.tokenIndex = '-'
                        noOperadores += 1
                        self.funcionSuma(stackTokens, stackOperadores, TOP1)
                    esperado = \
                        self.PRIMARIO | self.PARENTESIS_A | self.FUNCION | self.SIGN
                elif self.esComentario():
                    pass #Ignora
                else:
                    if esperado and self.OPERADOR == 0:
                        self.error_parsing(self.pos, "Operador inesperado")
                    noOperadores += 2
                    self.funcionSuma(stackTokens, stackOperadores, TOP2)
                    esperado = \
                        self.PRIMARIO | self.PARENTESIS_A | self.FUNCION | self.SIGN
            elif self.esNumero():
                if esperado and self.PRIMARIO == 0:
                    self.error_parsing(self.pos, 'Numero inesperado')
                token = Token(TNUMERO, 0, 0, self.numeroTokens)
                stackTokens.append(token)
                esperado = self.OPERADOR | self.PARENTESIS_C | self.COMA
            elif self.esString():
                if(esperado & self.PRIMARIO) == 0:
                    self.error_parsing(self.pos, 'String inesperado')
                token = Token(TNUMERO, 0, 0, self.numeroTokens)
                stackTokens.append(token)
                esperado = self.OPERADOR | self.PARENTESIS_C | self.COMA
            elif self.esParentesisA():
                if (esperado & self.PARENTESIS_A) == 0:
                    self.error_parsing(self.pos, 'Inesperado \"(\"')
                if esperado & self.CALL:
                    noOperadores += 2
                    self.tokenPrio = -2
                    self.tokenIndex = -1
                    self.funcionSuma(stackTokens, stackOperadores, TLLAMADOFUNCION)
                esperado = \
                    self.PRIMARIO | self.PARENTESIS_A | self.FUNCION | \
                    self.SIGN | self.NULLARY_CALL
            elif self.esParentesisC():
                if esperado & self.NULLARY_CALL:
                    token = Token(TNUMERO, 0, 0, [])
                    stackTokens.append(token)
                elif (esperado & self.PARENTESIS_C) == 0:
                    self.error_parsing(self.pos, 'Inesperado \")\"')
                esperado = self.OPERADOR | self.PARENTESIS_C | self.COMA | \
                    self.PARENTESIS_A | self.CALL
            elif self.esComa():
                if (esperado & self.COMA) == 0:
                    self.error_parsing(self.pos, 'Inesperado \",\"')
                self.funcionSuma(stackTokens, stackOperadores, TOP2)
                noOperadores += 2
                esperado = \
                    self.PRIMARIO | self.PARENTESIS_A | self.FUNCION | self.SIGN
            elif self.esConstante():
                if (esperado & self.PRIMARIO) == 0:
                    self.error_parsing(self.pos, 'Constante inesperada')
                constToken = Token(TNUMERO, 0, 0, self.numeroTokens)
                stackTokens.append(constToken)
                esperado = self.OPERADOR | self.PARENTESIS_C | self.COMA
            elif self.esOp2():
                if(esperado & self.FUNCION) == 0:
                    self.error_parsing(self.pos, 'Funcion inesperada')
                self.funcionSuma(stackTokens, stackOperadores, TOP2)
                noOperadores += 2
                esperado = self.PARENTESIS_A
            elif self.esOp1():
                if(esperado & self.FUNCION) == 0:
                    self.error_parsing(self.pos, 'Funcion inesperada')
                self.funcionSuma(stackTokens, stackOperadores, TOP1)
                noOperadores += 1
                esperado = self.PARENTESIS_A
            elif self.esVar():
                if (esperado & self.PRIMARIO) == 0:
                    self.error_parsing(self.pos, 'Variable inesperada')
                varToken = Token(TVAR, self.tokenIndex, 0, 0)
                stackTokens.append(varToken)
                esperado = \
                    self.OPERADOR | self.PARENTESIS_C | self. COMA | \
                    self.PARENTESIS_A | self.CALL
            elif self.esBlanco():
                pass #Ignora espacio es blanco
            else:
                if self.msgError == '':
                    self.error_parsing(self.pos, 'Caracter desconocido')
                else:
                    self.error_parsing(self.pos, self.msgError)
            
        if self.tempPrio < 0 or self.tempPrio >=10:
            self.error_parsing(self.pos, 'Sin par \"()\"')
        while len(stackOperadores) > 0:
            tmp = stackOperadores.pop()
            stackTokens.append(tmp)
        if (noOperadores + 1) != len (stackTokens):
            self.error_parsing(self.pos, 'Igualdad/Par \"()\"')
        return Expresion(stackTokens, self.ops1, self.ops2, self.funciones)

    def evaluar(self, exp, variables):
        return self.parse(exp).evaluar(variables)
    
    def error_parsing(self, column, msg):
        self.exito = False
        self.msgError = 'Error en el parcer [Columna ' + str(column) + ']: ' + msg
        raise Exception(self.msgError)
    
    def funcionSuma(self, stackToken, stackOperador, tipo_):
        operador = Token(tipo_, self.tokenIndex, self.tokenPrio + self.tempPrio,0,)
        while len(stackOperador) > 0:
            if operador.prio_ <= stackOperador[len(stackOperador) - 1].prio_:
                stackToken.append(stackOperador.pop())
            else:
                break
        stackOperador.append(operador)

    def esNumero(self):
        r = False
        str = ''
        while self.pos < len (self.expresion):
            code = self.expresion[self.pos]
            if (code >= '0' and code <= '9') or code == '.':
                if (len(str) == 0 and code == '.'):
                    str = '0'
                str += code
                self.pos += 1
                self.numeroTokens = float(str)
                r = True
            else:
                break
        return r

    def unescape(self, v, pos):
        buffer = []
        escaping = False

        for i in range(0, len(v)):
            c = v[i]
            if escaping:
                if c == "'":
                    buffer.append("'")
                    break
                elif c == '\\':
                    buffer.append('\\')
                    break
                elif c == '/':
                    buffer.append('/')
                    break
                elif c == 'b':
                    buffer.append('\b')
                    break
                elif c == 'f':
                    buffer.append('\f')
                    break
                elif c == 'n':
                    buffer.append('\n')
                    break
                elif c == 'r':
                    buffer.append('\r')
                    break
                elif c == 't':
                    buffer.append('\t')
                    break
                elif c == 'u':
                    codePoint = int(v[i + 1, i + 5], 16)
                    buffer.append(codePoint)
                    i += 4
                    break
                else:
                    raise self.error_parsing(
                        pos + i,
                        'Secuencia de escape ilegal: \'\\' + c + '\'',
                    )
                escaping = False
            else:
                if c == '\\':
                    escaping = True
                else:
                    buffer.append(c)

        return ''.join(buffer)

    def esString(self):
        r = False
        str = ''
        startpos = self.pos
        if self.pos < len(self.expresion) and  self.expresion[self.pos] == "'":
            self.pos += 1
            while self.pos < len(self.expresion):
                code = self.expresion[self.pos]
                if code != '\'' or (str != '' and str[-1] == '\\'):
                    str += self.expresion[self.pos]
                    self.pos += 1
                else:
                    self.pos += 1
                    self.numeroTokens = self.unescape(str, startpos)
                    r = True
                    break
            
        return r

    def esConstante(self):
        for i in self.constantes:
            L = len(i)
            str = self.expresion[self.pos:self.pos + L]
            if i == str:
                if len(self.expresion) <= self.pos + L:
                    self.numeroTokens = self.constantes[i]
                    self.pos += L
                    return True
                if not self.expresion[self.pos + L].isalnum() and self.expresion[self.pos + L] != "_":
                    self.numeroTokens = self.constantes[i]
                    self.pos += L
                    return True
        return False
    
    def esOperador(self):
        ops = (
            ('+', 2, '+'),
            ('-', 2, '-'),
            ('*', 3, '*'),
            (u'\u2219', 3, '*'),
            (u'\u2022', 3, '*'), 
            ('/', 4, '/'),
            ('%', 4, '%'),
            ('^', 6, '^'),
            ('||', 1, '||'),
            ('==', 1, '=='),
            ('!=', 1, '!='),
            ('<=', 1, '<='),
            ('>=', 1, '>='),
            ('<', 1, '<'),
            ('>', 1, '>'),
            ('and', 0, 'and'),
            ('or', 0, 'or'),
        )
        for token, prioridad, index in ops:
            if self.expresion.startswith(token, self.pos):
                self.tokenPrio = prioridad
                self.tokenIndex = index
                self.pos += len(token)
                return True
        return False

    def isSing(self):
        code = self.expresion[self.pos - 1]
        return (code == '+') or (code == '-')

    def esSignoPositivo(self):
        code = self.expresion[self.pos -1]
        return code =='+'
    
    def esSignoNegativo(self):
        code = self.expresion[self.pos -1]
        return code =='-'

    def esParentesisA(self):
        code = self.expresion[self.pos]
        if code == '(':
            self.pos += 1
            self.tempPrio +=10
            return True
        return False

    def esParentesisC(self):
        code = self.expresion[self.pos]
        if code == ')':
            self.pos += 1
            self.tempPrio -=10
            return True
        return False

    def esComa(self):
        code = self.expresion[self.pos]
        if code == ',':
            self.pos += 1
            self.tokenPrio =-1
            self.tokenIndex = ","
            return True
        return False

    def esBlanco(self):
        code = self.expresion[self.pos]
        if code.isspace():
            self.pos += 1
            return True
        return False

    def esOp1(self):
        str = ''
        for i in range(self.pos, len(self.expresion)):
            c = self.expresion[i]
            if c.upper() == c.lower():
                if i == self.pos or (c != '_' and (c < '0' or c > '9')):
                    break
            str += c
        if len(str) > 0 and str in self.ops1:
            self.tokenIndex = str
            self.tokenPrio = 7
            self.pos += len(str)
            return True
        return False

    def esOp2(self):
        str = ''
        for i in range(self.pos, len(self.expresion)):
            c = self.expresion[i]
            if c.upper() == c.lower():
                if i == self.pos or (c != '_' and (c < '0' or c > '9')):
                    break
            str += c
        if len(str) > 0 and (str in self.ops2):
            self.tokenIndex = str
            self.tokenPrio = 7
            self.pos += len(str)
            return True
        return False

    def esVar(self):
        str = ''
        inQuotes = False
        for i in range(self.pos, len(self.expresion)):
            c = self.expresion[i]
            if c.lower() == c.upper():
                if((i == self.pos and c != '"') or (not(c in '_."') and (c < '0' or c > '9'))) and not inQuotes:
                    break
            if c == '"':
                inQuotes = not inQuotes
            str += c
        if str:
            self.tokenIndex = str
            self.tokenPrio = 4
            self.pos += len(str)
            return True
        return False
    
    def esComentario(self):
        code = self.expresion[self.pos - 1]
        if code == '/' and self.expresion[self.pos] == '*':
            self.pos = self.expresion.index('*/', self.pos) + 2
            if self.pos == 1:
                self.pos = len(self.expresion)
            return True
        return False
#================FIN CLASE PARSER========================