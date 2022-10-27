# -*- coding: utf-8 -*-

# autores: Óscar Vázquez Blanco y Diego Vázquez Blanco

import random
import sys
from codecs import open


# Retorna el texto fuente a partir de la lectura del fichero donde se encuentra
def leer_fichero(fichero):

	text = ''
	fich = open(fichero, 'r', 'utf-8')

	# recorre el fichero linea por linea
	for line in fich:
		text += line  #.strip('\n') si no queremos recoger saltos de linea

	return text


# Retorna el alfabeto del texto
def crear_claves_alfabeto(texto):
 
	alfabet = []
	# variable k para comprobar si un caracter ya esta en el texto
	k = False
	# recorre los caracteres del texto uno por uno
	for a in texto:
		for b in alfabet:
			if a == b:
				k = True
		if k == False:
			alfabet.append(a)
		else:
			k = False
	# ordena el alfabeto
	alfabet.sort()
	return alfabet


# Retorna un array indicando el numero de veces que aparecen los caracteres del alfabeto en el texto
def crear_valores_alfabeto(texto, claves_alfabeto):

	valores_alfabet = []
	# inicializamos el array del numero de veces que aparece un caracter a 0
	for a in claves_alfabeto:
		valores_alfabet.append(0)
	# añadimos los valores al array
	for i,a in enumerate(claves_alfabeto):
		for b in texto:
			if a == b:
				valores_alfabet[i] += 1

	return valores_alfabet 


# Retorna una matriz con el numero de veces que aparece un caracter seguido de otro
def crear_valores_nivel_2(texto, claves_alfabeto):

	valores_nivel_2 = []
	# inicializamos a 0
	for i,a in enumerate(claves_alfabeto):
		valores_nivel_2.append([])
		for b in claves_alfabeto:
			valores_nivel_2[i].append(0)

	# introduce el numero de veces que aparece un caracter seguido de otro
	for i,a in enumerate(claves_alfabeto):
		for j,b in enumerate(texto[:-1]): # excluimos el ultimo caracter del texto porque no tiene caracter siguiente
			if a == b:
				for k,c in enumerate(claves_alfabeto):
					if c == texto[j+1]:
						valores_nivel_2[i][k] += 1

	return valores_nivel_2


# Retorna una multimatriz vacía de nivel n
def crea_dic_multimatriz(dic_multimatriz, texto, nivel):

	for i in range(len(texto)-nivel+1):
		subcadena = texto[i:nivel+i-1]
		dic_multimatriz[subcadena] = ''

	for i in range(len(texto)-nivel+1):
		subcadena = texto[i:nivel+i-1]
		car = dic_multimatriz[subcadena]
		car += texto[nivel+i-1]
		dic_multimatriz[subcadena] = car 


# Genera un texto aleatorio a partir de las claves del alfabeto
def nivel_0(claves_alfabeto, caracteres):

	for a in range(caracteres):
		# imprime sin espacios
		sys.stdout.write(random.choice(claves_alfabeto))
	print ('')


# Genera un texto a partir de los valores del alfabeto
def nivel_1(texto, claves_alfabeto, valores_alfabeto, caracteres):
	
	for i in range(caracteres):
		aux = 0
		aleatorio = random.randint(1, len(texto)-1)
		for j,a in enumerate(claves_alfabeto):
			aux += valores_alfabeto[j]
			if aux >= aleatorio:
				sys.stdout.write(claves_alfabeto[j])
				break
	print ('')


# Genera un texto aleatorio a partir del caracter anterior al que se escribe
def nivel_2(texto, caracteres):

	dic_matriz = {}

	for i in range(len(texto)-3):
		subcadena = texto[i:i+1]
		dic_matriz[subcadena] = ''

	for i in range(len(texto)-3):
		subcadena = texto[i:i+1]
		car = dic_matriz[subcadena]
		car += texto[i+1]
		dic_matriz[subcadena] = car

	# primer caracter es uno aleatorio del texto
	aleatorio = random.randint(0, len(texto))
	char_anterior = texto[aleatorio]
	sys.stdout.write(char_anterior)

	# imprime el resto de caracteres a partir de su anterior
	for i in range(caracteres - 1):
		letra = random.choice(dic_matriz[char_anterior])
		sys.stdout.write(letra)
		char_anterior = letra

	print ('')


# Genera un texto aleatorio a partir de los n caracteres anteriores al que se escribe
def nivel_n(texto, caracteres, nivel):

	dic_multimatriz = {}

	crea_dic_multimatriz(dic_multimatriz, texto, nivel)
	
	caract = ''
	# Primeros n-1 caracteres, usaremos caract para guardar los caracteres anteriores a la letra a escribir
	aleatorio = random.randint(1, len(texto)-nivel+1)
	for i in range(nivel-1):
		caract += texto[aleatorio + i]
		sys.stdout.write(caract[i])

	# imprime el resto de caracteres a partir de sus n-1 anteriores
	for i in range(caracteres - nivel + 1): 
		letra = random.choice(dic_multimatriz[caract])
		sys.stdout.write(letra)
		caract = caract[1:] + letra
	
	print ('')


# Programa principal
def main():

	fichero = input('Introduzca nombre del fichero: ')

	texto = leer_fichero(fichero)

	claves_alfabeto = crear_claves_alfabeto(texto)
	valores_alfabeto = crear_valores_alfabeto(texto, claves_alfabeto)

	m = True

	while( m == True ):

		nivel = int(input('Nivel: '))
		caracteres = int(input('Tamaño texto generado: '))
		if (nivel > caracteres) or (nivel > len(texto)-1):
			print ('El nivel debe ser menor que el tamaño del texto generado o longitud del texto fuente.\n')
		else:
			m = False

	texto += texto[:nivel]

	if nivel == 0:

		nivel_0(claves_alfabeto, caracteres)

	elif nivel == 1:

		nivel_1(texto, claves_alfabeto, valores_alfabeto, caracteres)
	
	elif nivel == 2:

		nivel_2(texto, caracteres)

	else:
		
		nivel_n(texto, caracteres, nivel)


if __name__ == '__main__':
	main()