import ctypes
from ctypes import * 
STD_OUTPUT_HANDLE = -11
 
class COORD(Structure):
    pass
 
COORD._fields_ = [("X", c_short), ("Y", c_short)]
 
def print_at(c, r, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
 
    c = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)

def cantor(x,y,size):
	if (size>=1):
		for i in range(size):
			print_at(x+i,y,"_")
		newY=y+1
		newSize=size//3
		cantor(x,newY,newSize)
		cantor(x+newSize*2,newY,newSize)

cantor(0,0,81)
print()
input("Presione una tecla para cerrar...")