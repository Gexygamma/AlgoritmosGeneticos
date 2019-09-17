print("Importando librerias...")
print(" datetime...")
import datetime
print(" random...")
import random as rnd
print(" os...")
import os
print(" pandas...")
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
print(" PIL/pillow...")
from PIL import Image, ImageDraw
print("Hecho!")
 
# Crear lista de capitales
nombresCapital = [
	"Ciudad de Buenos Aires",
	"Córdoba",
	"Corrientes",
	"Formosa",
	"La Plata", #4
	"La Rioja",
	"Mendoza",
	"Neuquen",
	"Paraná", #8
	"Posadas",
	"Rawson",
	"Resistencia",
	"Río Gallegos", #12
	"San Fernando del Valle de Catamarca",
	"San Miguel de Tucumán",
	"San Salvador de Jujuy",
	"Salta", #16
	"San Juan",
	"San Luis",
	"Santa Fe",
	"Santa Rosa", #20
	"Santiago del Estero",
	"Ushuaia",
	"Viedma" ]

coordenadas = [
	(350, 388),
	(217, 288),
	(353, 179),
	(363, 136),
	(354, 398),
	(157, 249),
	(110, 342),
	(129, 522),
	(310, 305),
	(423, 182),
	(204, 649),
	(341, 172),
	(148, 905),
	(172, 208),
	(186, 164),
	(188, 85),
	(183, 95),
	(112, 305),
	(166, 345),
	(301, 298),
	(217, 454),
	(214, 185),
	(179, 990),
	(243, 577)
]

# Inicializar parámetros de ejecución
popSize = 50
chromSize = len(nombresCapital) # Son 24 capitales
probCrossover = 0.75
probMutacion = 0.1
number_list = list(range(chromSize))
distance_matrix = []

def clearScreen():
	# Limpia la terminal
	os.system('cls' if os.name == 'nt' else 'clear')
 
def decision(probability):
	# Toma una decision aleatoria en base a una probabilidad
	return rnd.random() < probability
 
def loadMatrix():
	# Carga matriz de distancias en memoria desde un archivo xlsx
	try: 
		data = pd.read_excel('TP3/TablaCapitales.xlsx')
	except FileNotFoundError:
		data = pd.read_excel('TablaCapitales.xlsx')
	for i in range(chromSize):
		distance_matrix.append([])
		for j in range(chromSize):
			distance_matrix[i].append(data.iloc[i, j+1])

def distance(capital1, capital2):
	# Calcula distancia entre dos capitales
	return distance_matrix[capital1][capital2]

def nearestCapital(path):
	capital = path[-1]
	distanciaMinima = -1
	for i in range(chromSize):
		if (not i in path) & ((distance(i, capital) < distanciaMinima) | (distanciaMinima == -1)):
			distanciaMinima = distance(i, capital)
			closest = i
	return closest

def drawChromToFile(chrom):
	# Dibuja el recorrido de un cromosoma dado
	print("Armando recorrido en mapa... ", end="")
	try:
		im = Image.open("TP3/base.png")
	except:
		im = Image.open("base.png")
	draw = ImageDraw.Draw(im)
	for i in range(len(chrom.gen)-1):
		capital1 = chrom.gen[i]
		capital2 = chrom.gen[i+1]
		draw.line(coordenadas[capital1]+coordenadas[capital2], fill=128, width=4)
	draw.line(coordenadas[chrom.gen[-1]]+coordenadas[chrom.gen[0]], fill=128, width=4)
	im.show() # A veces no funca :(
	filename = "Mapa_{date}.png".format(date=datetime.datetime.now().strftime("%d-%m-%Y_%H%M%S"))
	im.save(filename, "PNG")
	print("Hecho!")

class Chromosome(object):
 
	def __init__(self, size=None, madre=None, padre=None, punto=None):
		# Constructor del cromosoma
		self.gen = []
		if size == None:
			pass
		elif madre == None:
			self.gen = rnd.sample(number_list, size)
			self.calculateScore()
		elif padre != None:
			index = 0
			self.gen = [None]*size
			while(True):
				self.gen[index] = madre.gen[index]
				index = madre.gen.index(padre.gen[index])
				if (index == 0):
					break
			for i in range(size):
				if (self.gen[i] is None):
					self.gen[i] = padre.gen[i]
		else:
			for i in range(size):
				self.gen.append(madre.gen[i])
			self.score=madre.score
 
	def asString(self):
		# Devuelve un string en base al arreglo de genes
		string = []
		for i in range(24):
			string.append(str(self.gen[i]))
		return ",".join(string)
 
	def calculateScore(self):
		# Calcula y guarda el puntaje, que representa la distancia recorrida
		self.score = 0
		for i in range(len(self.gen)-1):
			self.score += distance(self.gen[i], self.gen[i+1])
		self.score += distance(self.gen[-1], self.gen[0])
 
	def calculateFitness(self, totalScore):
		# Calcula y guarda el valor fitness
		self.fitness = totalScore/self.score
 
	def mutate(self):
		# Muta al cromosoma, intercambiando dos genes aleatorios de lugar
		points = rnd.sample(number_list, k=2)
		cap1 = self.gen[points[0]]
		cap2 = self.gen[points[1]]
		self.gen[points[0]] = cap2
		self.gen[points[1]] = cap1
		self.calculateScore()
	 
class Population(object):
 
	def __init__(self, prevPopulation=None):
		# Constructor de la población
		self.chromosomes = []
		self.totalScore = 0
		# Crear población aleatoriamente
		if prevPopulation == None:
			for i in range(popSize):
				individuo = Chromosome(chromSize)
				self.addChromosome(individuo)
		# Crear población hija en base a la población previa
		else:
			# Aplicar elitismo
			self.addChromosome(Chromosome(chromSize, prevPopulation.chromosomes[-2]))
			self.addChromosome(Chromosome(chromSize, prevPopulation.chromosomes[-1]))
			for i in range(int(popSize/2)-1):
				padre = prevPopulation.selectWeightedChromosome()
				madre = prevPopulation.selectWeightedChromosome()
				# Aplicar crossover
				if decision(probCrossover) & (padre!=madre):
					hijo1 = Chromosome(chromSize, madre, padre)
					hijo2 = Chromosome(chromSize, padre, madre)
					isNew = True
				else:
					hijo1 = Chromosome(chromSize, padre)
					hijo2 = Chromosome(chromSize, madre)
					isNew = False
				# Aplicar mutación
				if decision(probMutacion):
					hijo1.mutate()
				elif isNew:
					hijo1.calculateScore()
				if decision(probMutacion):
					hijo2.mutate()
				elif isNew:
					hijo2.calculateScore()
				# Agregar cromosomas hijos
				self.addChromosome(hijo1)
				self.addChromosome(hijo2)
 
	def addChromosome(self, c):
		# Agrega un cromosoma a la población
		self.chromosomes.append(c)
 
	def calculateTotalScore(self):
		# Calcula y guarda la suma de los puntajes de todos los cromosomas
		for c in self.chromosomes:
			self.totalScore += c.score
 
	def sortByFitness(self):
		# Calcula los valores fitness de cada cromosoma y ordena de menor a mayor
		for c in self.chromosomes:
			c.calculateFitness(self.totalScore)
		self.chromosomes.sort(key = lambda Chromosome: Chromosome.fitness)
 
	def selectWeightedChromosome(self):
		# Devuelve un cromosoma, teniendo mayor probabilidad dependiendo de su valor fitness
		# Obtener lista de los valores fitness de los cromosomas
		w = []
		for c in self.chromosomes:
			w.append(c.fitness)
		# Devolver cromosoma aleatorio
		return rnd.choices(
			population = self.chromosomes,
			weights = w
		)[0]
 
	def printStats(self):
		# Imprime en pantalla estadisticas de la población
		minimo = self.chromosomes[0].score
		maximo = self.chromosomes[-1].score # Indice -1 devuelve el último item
		promedio = self.totalScore / len(self.chromosomes)
		print("Máximo: ", maximo, "Mínimo: ", minimo, "Promedio: ", promedio)
 
	def printChrom(self):
		# Imprime en pantalla la lista de cromosomas
		for c in self.chromosomes:
			print(c.asString(), " f:", c.fitness)


def heuristica(capitalInicial):
	result = Chromosome()
	result.gen.append(capitalInicial)
	while (True):
		result.gen.append(nearestCapital(result.gen))
		if len(result.gen) == 24:
			result.calculateScore()
			break
	return result

def genetico():
	# Obtener número de iteraciones del usuario
	iteraciones = int(input("Ingrese cantidad de iteraciones a ejecutar: "))
	
	# Crear primera instancia de la población
	newPopulation = Population()
	 
	for n in range(iteraciones):
		# Calcular y guardar puntajes y valores fitness de los cromosomas
		newPopulation.calculateTotalScore()
		newPopulation.sortByFitness()
		# Crear nueva población en base a la anterior
		prevPopulation = newPopulation
		newPopulation = Population(prevPopulation)
	 
	resultChrom = prevPopulation.chromosomes[-1]
	
	# Dibujar camino óptimo
	drawChromToFile(resultChrom)

	# Imprimir resultado final en pantalla
	print("Resultado\n Cromosoma: {chrom}\n Objetivo: {score}\n Fitness: {fitness}"
		.format(
		   chrom = resultChrom.asString(),
		   score = resultChrom.score,
		   fitness = resultChrom.fitness))
	input("Presione una tecla para volver al menú...")

def busquedaUnitaria():
	capital = int(input("Ingrese la capital de partida: "))
	resultChrom = heuristica(capital)
	drawChromToFile(resultChrom)
	print("Resultado\n Recorrido: {chrom}\n Objetivo: {score}\n"
		.format(
		   chrom = resultChrom.asString(),
		   score = resultChrom.score))
	input("Presione una tecla para volver al menú...")

def busquedaTotal():
	bestScore = 0
	for i in range(len(number_list)):
		resultChrom = heuristica(i)
		if (resultChrom.score < bestScore) | (bestScore == 0):
			bestScore = resultChrom.score
			best = resultChrom
	drawChromToFile(resultChrom)
	print("Resultado\n Recorrido: {chrom}\n Objetivo: {score}\n"
		.format(
		   chrom = best.asString(),
		   score = best.score))
	input("Presione una tecla para volver al menú...")
	
#################################
# INICIO DEL PROGRAMA PRINCIPAL #
#################################

# Cargar matriz en memoria
loadMatrix()

# Mostrar menú del programa
opcion = 1
while (opcion != 0):
	clearScreen()
	print("Menú de opciones - Problema del viajante")
	print()
	print("1- Búsqueda heurística dada una capital de partida")
	print("2- Búsqueda heurística general")
	print("3- Búsqueda mediante algoritmos genéticos")
	print("0- Salir")
	print()
	opcion = int(input("Ingrese opción: "))
	clearScreen()
	if (opcion == 1):
		busquedaUnitaria()
	elif (opcion == 2):
		busquedaTotal()
	elif (opcion == 3):
		genetico()
