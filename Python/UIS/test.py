h = """2. CIRCUITOS DIGITALES Y COMPUERTAS LOGICAS


2.1. FUNCIONES Y COMPUERTAS LOGICAS
Se ha denominado compuerta lógica a aquel dispositivo que bajo algún principio, ya sea
eléctrico, mecánico, hidráulico, neumático, electrónico o cualquier otro, permite realizar
las funciones lógicas del Algebra de Boolean.
Las funciones lógicas más importantes y su representación simbólica son: [ ]
FUNCION AND: F toma el valor de uno solamente cuando A, B Y C están en uno.


FUNCION OR: F toma el valor de uno cuando por lo menos una de las entradas A, B O

C toman el valor de uno.
FUNCION NOT: F toma el valor inverso de A.

FUNCION YES: F toma el mismo valor de A.

FUNCION AND-NOT: """
h = h.split(r"\n")
h = [sub.replace("\n","") for sub in h]