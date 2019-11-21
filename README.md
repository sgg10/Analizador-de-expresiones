# Analizador de expresiones
Proyecto final de la materia Lenguajes de programacio, universidad EAFIT.
Analizador de expresiones matemáticas con Python mediante un proceso de Parser.

### Parser
---
Para realizar la evaluacion de una expresion matematica, es necesario crear una instancia de la clase Parser, alojada en el script analizador.py:
```python
from analizador import Parser
parcer = Parser()
```
Luego de realizar la instancia, se puede crear una expresion mediante el uso del metodo parse y para obtener el resultado se emplea el metodo evaluar como se muestra:
```python
parcer.parse("(5-9) * 8").evaluar()
#Retorna -32.0
```
El metodo evaluar() toma como parametro un diccionario con todas las variables que se vayan a usar en la expresion, de no existir variables, puede omitirse este parametro. A continuación se dara algunos otros ejemplos del uso del metodo.
```python
parcer.parse(" 3 + x").evaluar( {'x' :  4} ) #Retorna 7.0
parcer.parse(" x + y ").evaluar( {'x' :  3, 'y' : 4} ) #Retorna 7.0
```
### Algunas Operaciones
| Operación | Ejemplo |
| ------------ | ------------ |
| + | parcer.parse(" 3 + x").evaluar( {'x' :  4} ) |
|  - | parcer.parse(" x - 90").evaluar( {'x' :  150} )  |
|  * |  parcer.parse(" x * 5 ").evaluar( {'x' :  4} ) |
|  / |  parcer.parse(" 8 / x").evaluar( {'x' :  4} ) |
|  % | parcer.parse(" 8 % x").evaluar( {'x' :  4} )  |
|  PI |  parcer.parse(" PI ").evaluar() |
|  E |   parcer.parse(" E ").evaluar() |
| sin(x)  |   parcer.parse(" sin(x)").evaluar( {'x' :  0} ) |
| cos(x)  |   parcer.parse(" cos(x)").evaluar( {'x' :  0} ) |
| tan(x)  |   parcer.parse(" tan(x)").evaluar( {'x' :  0} ) |
| csc(x)  |   parcer.parse(" csc(x)").evaluar( {'x' :  0} ) |