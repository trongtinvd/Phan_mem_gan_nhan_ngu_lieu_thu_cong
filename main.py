from tkinter import *
from my_module import MyApp

# nhập tổ hợp phím Shift+L để sử dụng tính năng tách từ với giao diện tạm thời

def main():	
	root = Tk()

	myApp = MyApp(root)
	myApp.pack()

	root.mainloop()


if __name__ == '__main__':
	main()