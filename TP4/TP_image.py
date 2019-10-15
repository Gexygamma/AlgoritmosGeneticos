import datetime
from PIL import Image, ImageDraw
from math import log, ceil, floor

y_offset = 6 # Distancia vertical entre iteraciones de líneas
padding = 12 # Margen de la imagen
line_width = 3 # Grosor de las líneas
line_color = 128 # Color de las líneas
limit = 1 # Limite de recursion para la funcion de cantor (mínimo 1)

long_init = int(input("Ingrese longitud inicial en pixeles: "))

iterations = int(ceil(log(long_init, 3)))
im_width = int(padding*2 + long_init)
im_height = int(padding*2 + line_width + (y_offset+line_width)*iterations)
image = Image.new("RGB", (im_width, im_height), color='white')
draw = ImageDraw.Draw(image)

def cantor(x, y, size):
	if (size >= max(limit, 1)):
		draw.line((x, y)+(x+size-1, y), fill=line_color, width=line_width)
		y_new = y + y_offset + line_width
		size_new = size / 3
		cantor(x, y_new, size_new)
		cantor(x+size_new*2, y_new, size_new)

cantor(padding, padding+floor(line_width/2), long_init)

filename = "Cantor_L{lon}_{date}.png".format(
	lon=long_init, 
	date=datetime.datetime.now().strftime("%d-%m-%Y_%H%M%S"))
image.save(filename, "PNG")

print("Imagen creada con el nombre '{file}'.".format(file=filename))

input("Presione una tecla para finalizar...")
