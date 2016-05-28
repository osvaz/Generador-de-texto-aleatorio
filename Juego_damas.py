#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# PARADIGMAS DE PROGRAMACION - CURSO 2013-14
# PRACTICA 1: DAMAS ESPANOLAS

# Un tablero esta formado por una lista de listas de casillas
# Cada casilla es una tupla indicando:
# - Si esta vacia (true) o no (false)
# - Si contiene una pieza blanca (true) o negra (false)
# - Si la pieza es un peon (true) o una reina (false)

# Constantes selectoras de cada parte de la tupla
SEL_VACIA = 0
SEL_COLOR = 1
SEL_REINA = 2

# Las 5 posibilidades para cada casilla:
PEON_BLANCO   = (False,True,False)
PEON_NEGRO    = (False,False,False)
REINA_BLANCA  = (False,True,True)
REINA_NEGRA   = (False,False,True)
CASILLA_VACIA = (True,False,False)

# Para pasar de coordenadas numericas a caracteres
NOM_FIL = "ABCDEFGH"
NOM_COL = "1 2 3 4 5 6 7 8"

# Mensajes asociados al valor devuelto por verificar_jugada
MSG_STATUS = [
    "Sintaxis no valida",
    "Casilla origen vacia",
    "Casilla origen no contiene pieza del color correspondiente al turno actual",
    "Movimiento no diagonal",
    "Existen piezas intermedias en el movimiento",
    "Casilla de destino no es adyacente",
    "Casilla de destino ocupada por pieza del mismo color",
    "No se puede capturar una pieza en el borde del tablero",
    "Captura bloqueada por otra pieza adyacente"]

# DIRS es una lista con las direcciones de las 4 diagonales
DIRS = [(-1,-1),(-1,1),(1,-1),(1,1)]

# Crea y devuelve un tablero con la posicion inicial
def tablero_inicial():
    tab = [[],[],[],[],[],[],[],[]]
    for fil in range(8):
        for col in range(8):
            if (fil+col) % 2 == 1:
                if fil < 3:
                    tab[fil].append(PEON_NEGRO)
                elif fil > 4:
                    tab[fil].append(PEON_BLANCO)
                else:
                    tab[fil].append(CASILLA_VACIA)
            else:
                tab[fil].append(CASILLA_VACIA)
    return tab

# Traduce una casilla a texto
def casilla_a_texto(casilla):
    if casilla == PEON_NEGRO:
        return "n "
    elif casilla == PEON_BLANCO:
        return "b "
    elif casilla == REINA_NEGRA:
        return "N "
    elif casilla == REINA_BLANCA:
        return "B "
    else:
        return "- "

# Escribe un tablero en pantalla
def tablero_mostrar(tablero):
    print "  "+NOM_COL
    print "  " + "-"*16
    for fil in range(7,-1,-1):
        lin = NOM_FIL[fil]+"|"
        for col in range(8):
            lin += casilla_a_texto(tablero[fil][col])
        lin += "|"+NOM_FIL[fil]
        print lin
    print "  " + "-"*16
    print "  "+NOM_COL

# Lee una jugada y devuelve la tupla (fil0,col0,fil1,col1)
# Si fich es distinto de None la lee del fichero, en caso contrario por teclado
# Las filas y columnas son enteros en el rango 0..7
# Pueden no estar en ese rango si el usuario introduce valores erroneos
def lee_jugada(turno, fich = None):
    if fich != None:
        cad = fich.readline(4)
        fich.readline()
    else:
        cad = ''
    # Si el fichero no existe o se ha terminado (cad vacia) se lee de teclado
    if cad == '':
        cad = raw_input("B> " if turno else "N> ")
    else:
        print "B>" if turno else "N>", cad
    if len(cad) != 4:
        return (-1,-1,-1,-1)
    else:
        return (ord(cad[0])-ord("A"),ord(cad[1])-ord("1"),
                ord(cad[2])-ord("A"),ord(cad[3])-ord("1"))

# Devuelve +1 si x > 0, -1 si x < 0, 0 si x == 0
def signo(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)

# Verifica si una jugada es correcta dado un tablero y el turno actual
# Devuelve un entero indicando el estado:
# -1  : Movimiento correcto, no hay captura
# -2  : Movimiento correcto con captura de pieza
# >=0 : Movimiento incorrecto, la lista MSG_STATUS informa del tipo de error
def verificar_jugada(tablero, turno, jugada):
    # Sintaxis valida
    for i in jugada:
        if i < 0 or i > 7:
            return 0
    (f0,c0,f1,c1) = jugada
    # Casilla de origen vacia
    if tablero[f0][c0] == CASILLA_VACIA:
        return 1
    # Casilla de origen con pieza de color distinto al turno
    if tablero[f0][c0][SEL_COLOR] != turno:
        return 2
    # Movimiento diagonal
    # Nota: No es necesario comprobar que d > 0, error captura pieza propia
    d = abs(f1-f0)
    if d != abs(c1-c0):
        return 3
    sf, sc = signo(f1-f0), signo(c1-c0)
    # Movimiento adyacente si es un peon o libre de obstaculos si reina
    if tablero[f0][c0][SEL_REINA]:
        for i in range(1,d):
            if tablero[f0+i*sf][c0+i*sc] != CASILLA_VACIA:
                return 4
    else:
        if d != 1:
            return 5
    # Casilla de destino vacia (resultado correcto, no hay captura)
    if tablero[f1][c1] == CASILLA_VACIA:
        return -1
    # Casilla de destino ocupada:
    # Comprobar que es pieza de distinto color al del turno
    if tablero[f1][c1][SEL_COLOR] == turno:
        return 6
    # Captura: Calcular celda de destino tras captura
    f2, c2 = f1+sf, c1+sc
    # Comprobar que este en rango y vacia
    if f2 < 0 or f2 > 7 or c2 < 0 or c2 > 7:
        return 7
    if tablero[f2][c2] != CASILLA_VACIA:
        return 8
    # Movimiento correcto y se produce captura
    return -2

# Realiza un movimiento (debe verificarse previamente que es correcto)
# Almacena todos los datos del movimiento en una pila
# No solo posiciones de origen y destino sino informacion de pieza
# capturada y si se ha producido promocion a reina
# Formato: (f0,c0,f1,c1,f2,c2,casilla capturada,promocion)
# Deteccion de captura: f1 != f2
# Devuelve True si se ha realizado una captura
def hacer_movimiento(tablero, jugada, pila):
    (f0,c0,f1,c1) = jugada
    # Detectar si es captura y calcular posicion final
    captura = tablero[f1][c1] != CASILLA_VACIA
    if captura:
        f2,c2 = f1+signo(f1-f0), c1+signo(c1-c0)
    else:
        f2,c2 = f1,c1
    # Detectar si es promocion a reina
    color = tablero[f0][c0][SEL_COLOR]
    if tablero[f0][c0][SEL_REINA]:
        promocion = False
    else:
        promocion = (color and f2 == 0) or (not color and f2 == 7)
    # Incluir movimiento en pila
    pila.append((f0,c0,f1,c1,f2,c2,tablero[f1][c1],promocion))
    # Actualizar tablero
    if promocion:
        tablero[f2][c2] = (False, color, True)
    else:
        tablero[f2][c2] = tablero[f0][c0]
    if captura:
        tablero[f1][c1] = CASILLA_VACIA
    tablero[f0][c0] = CASILLA_VACIA
    return captura

# Deshace el ultimo movimiento realizado (almacenado en la pila)
# Es el inverso del procedimiento anterior
def deshacer_movimiento(tablero, pila):
    (f0,c0,f1,c1,f2,c2,casilla,promocion) = pila.pop()
    color = tablero[f2][c2][SEL_COLOR]
    if promocion:
        tablero[f0][c0] = (False, color, False)
    else:
        tablero[f0][c0] = tablero[f2][c2]
    tablero[f2][c2] = CASILLA_VACIA
    if f1 != f2: # Captura
        tablero[f1][c1] = casilla

# Realiza una jugada completa (maximo numero de capturas)
# Supone que la jugada es correcta
# Adapta el tablero a la nueva posicion
# No cambia el turno
def jugar(tablero, jugada, turno, pila):
    if hacer_movimiento(tablero, jugada, pila):
        # Se ha producido una captura: Explorar posibles nuevas capturas
        (_,_,_,_,f0,c0,_,_) = pila[-1]
        (n,f1,c1) = explorar(tablero, f0, c0, turno, pila)
        if n > 0: # Existen nuevas capturas, la optima comienza por (f1,c1)
            tablero_mostrar(tablero)
            jugar(tablero, (f0,c0,f1,c1), turno, pila)

# Explora las posibles capturas de la pieza en posicion (f0,c0) y devuelve
# una tupla (n,f1,c1) con el movimiento que produce un mayor numero de
# capturas (n). Si no hay ninguna captura posible entonces n = 0
def explorar(tablero, f0, c0, turno, pila):
   nmax = 0 # Numero maximo de capturas
   fmax = cmax = -1 # Movimiento con mayor numero de capturas
   reina = tablero[f0][c0][SEL_REINA]
   # Examinar las 4 diagonales
   for (sf,sc) in DIRS:
       f1, c1 = f0+sf, c0+sc
       # Si es reina, avanzar por la diagonal hasta encontrar una pieza
       if reina:
           while 0 <= f1 <= 7 and 0 <= c1 <= 7 and tablero[f1][c1][SEL_VACIA]:
               f1 += sf
               c1 += sc
       # Si el movimiento es valido y es una captura..
       if verificar_jugada(tablero, turno, (f0,c0,f1,c1)) == -2:
           # Hacer movimiento
           hacer_movimiento(tablero, (f0,c0,f1,c1), pila)
           # Explorar a partir del movimiento
           (_,_,_,_,f2,c2,_,_) = pila[-1]
           (n,_,_) = explorar(tablero, f2, c2, turno, pila)
           # Deshacer movimiento
           deshacer_movimiento(tablero, pila)
           # Comprobar si las capturas superan el maximo
           n += 1
           if n > nmax:
               nmax, fmax, cmax = n, f1, c1
   # Devolver el resultado
   return (nmax,fmax,cmax)

# Numero de piezas del color del turno
def num_piezas(tablero, turno):
    n = 0
    for fila in tablero:
        for (vacia,color,_) in fila:
            if not vacia and color == turno:
                n += 1
    return n
           
# Programa principal
def main(nomfich = ""):
    # Inicializacion
    tablero = tablero_inicial()
    turno = True
    pila = []
    if nomfich != "":
        fich = open(nomfich,'r')
    else:
        fich = None
    try:        
        while True:
            tablero_mostrar(tablero)
            jugada = lee_jugada(turno,fich)
            res = verificar_jugada(tablero,turno,jugada)
            if res < 0:
                jugar(tablero,jugada,turno,pila)
                turno = not turno
            else:
                print "Error:", MSG_STATUS[res]
                break
            # Deteccion de final de partida
            if num_piezas(tablero,turno) == 0:
                tablero_mostrar(tablero)
                if turno:
                    print "Han ganado las negras"
                else:
                    print "Han ganado las blancas"
                break
    finally:
        if fich != None:
            fich.close()

if __name__=='__main__':
    main()