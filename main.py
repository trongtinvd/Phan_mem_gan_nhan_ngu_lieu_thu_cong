from tkinter import *
from my_module import MyApp

def main():	
	root = Tk()

	myApp = MyApp(root)
	myApp.pack()

	root.mainloop()


if __name__ == '__main__':
	main()