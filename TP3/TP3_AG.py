import datetime
import random as rnd
import os
 
# Inicializar parámetros de ejecución
nombresCapital = [
	"Ciudad de Buenos Aires",
	"Córdoba",
	"Corrientes",
	"Formosa",
	"La Plata",
	"La Rioja",
	"Mendoza",
	"Neuquen",
	"Paraná",
	"Posadas",
	"Rawson",
	"Resistencia",
	"Río Gallegos",
	"San Fernando del Valle de Catamarca",
	"San Miguel de Tucumán",
	"San Salvador de Jujuy",
	"Salta",
	"San Juan",
	"San Luis",
	"Santa Fe",
	"Santa Rosa",
	"Santiago del Estero",
	"Ushuaia",
	"Viedma" ]
popSize = 50
chromSize = len(nombresCapital) # Son 24 capitales
probCrossover = 0.75
probMutacionFinal = 0.4
number_list = list(range(chromSize))

def clearScreen():
	# Limpia la terminal
	os.system('cls' if os.name == 'nt' else 'clear')
 
def decision(probability):
	# Toma una decision aleatoria en base a una probabilidad
	return rnd.random() < probability
 
def distance(capital1, capital2):
	# Calcula distancia entre dos capitales
	pass
 
class Chromosome(object):

	def __init__(self, size, madre=None, padre=None, punto=None):
		# Constructor del cromosoma
		self.gen = []
		if madre == None:
			self.gen = rnd.sample(number_list, len(number_list))
			self.calculateScore()
		elif padre != None:
			index = 0
			while(True):
				self.gen[index] = madre.gen[index]
				index = madre.index(padre.gen[index])
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
		return ",".join(self.gen)
 
	def calculateScore(self):
		# Calcula y guarda el puntaje, que representa la distancia recorrida
		self.score = 0
		for i in range(len(self.gen)-1):
			self.score += distance(self.gen[i], self.gen[i+1])
		self.score += distance(self.gen[-1], self.gen[0])
 
	def calculateFitness(self, totalScore):
		# Calcula y guarda el valor fitness
		self.fitness = self.score/totalScore
 
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
				if decision(probMutacionActual):
					hijo1.mutate()
				elif isNew:
					hijo1.calculateScore()
				if decision(probMutacionActual):
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
 
#################################
# INICIO DEL PROGRAMA PRINCIPAL #
#################################
 
clearScreen()
 
# Obtener número de iteraciones del usuario
iteraciones = int(input("Ingrese cantidad de iteraciones a ejecutar: "))
 
# Crear primera instancia de la población
newPopulation = Population()
for n in range(iteraciones):
	# Calcular y guardar puntajes y valores fitness de los cromosomas
	probMutacionActual=probMutacionFinal*n/iteraciones
	newPopulation.calculateTotalScore()
	newPopulation.sortByFitness()
	# Crear nueva población en base a la anterior
	prevPopulation = newPopulation
	newPopulation = Population(prevPopulation)
 
resultChrom = prevPopulation.chromosomes[-1]
 
# Imprimir resultado final en pantalla
print("Resultado\n Cromosoma: {chrom}\n Objetivo: {score}\n Fitness: {fitness}"
	.format(
	   chrom = resultChrom.asString(),
	   score = resultChrom.score,
	   fitness = resultChrom.fitness))
input("Presione una tecla para cerrar...")
