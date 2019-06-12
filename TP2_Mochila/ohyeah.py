def numberToList(number):
	# Convierte un numero decimal en una lista de bits
	result = []
	if number is 1:
		result.append(1)
	else:
		actual = number
		while True:
			result.append(actual%2)
			actual = actual // 2
			if actual == 1:
				result.append(1)
				break
	while len(result) < len(elements):
		result.append(0)
	result.reverse()
	return result

class Bag(object):
	def __init__(self, size, content=None):
		self.size = size
		if content is None:
			self.content = []
		else:
			self.content = content

	def getTotalValue(self):
		total = 0
		for element in self.content:
			total += element.value
		return total

	def isNotOverloaded(self):
		total = 0
		for element in self.content:
			total += element.volume
		return (total<=self.size)

class Element(object):
	def __init__(self, volume, value):
		self.volume = volume
		self.value = value

### PROGRAMA
elements = [
	Element(150, 20), 
	Element(325, 40),
	Element(600, 50),
	Element(805, 36),
	Element(430, 25),
	Element(1200, 64),
	Element(770, 54),
	Element(60, 18),
	Element(930, 46),
	Element(353, 28),]
maxSize = 4200

maxBag=Bag(maxSize)
for i in range(1, 2 ** len(elements)):
	elementList = []
	result = numberToList(i)
	for n in range(len(elements)):
		if result[n] == 1:
			elementList.append(elements[n])
	bag = Bag(maxSize, elementList)
	if bag.isNotOverloaded() & (bag.getTotalValue() > maxBag.getTotalValue()):
		maxBag=bag
print("Valor:", maxBag.getTotalValue())
print("Elementos:")
for n in maxBag.content:
	for i in range(len(elements)):
		if n == elements[i]:
			print("Objeto ",i+1)
		