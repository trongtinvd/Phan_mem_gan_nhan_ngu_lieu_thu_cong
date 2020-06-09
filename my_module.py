from tkinter import *
from db_module import MyDatabase

class MyApp:
	def __init__(self, root):
		self.root = root
		disk_db = MyDatabase('./database.db')		
		memory_db = MyDatabase(':memory:')
		disk_db.create_table()
		memory_db.create_table()
		# init các thành phần giao diện vào đây

	def pack(self):
		# pack các thành phần giao diện vào đây

		pass