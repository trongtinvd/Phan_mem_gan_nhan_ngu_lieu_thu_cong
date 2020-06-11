import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import Toplevel, messagebox, filedialog, ttk
from db_module import MyDatabase

class MyApp:
	def __init__(self, root):
		self.root = root
		self.disk_db = MyDatabase('./database.db')		
		self.memory_db = MyDatabase(':memory:')
		self.disk_db.create_table()
		self.disk_db.insert_basic_pos_and_ne()
		self.memory_db.create_table()
		self.memory_db.insert_basic_pos_and_ne()
		# init các thành phần giao diện vào đây
		self.root.bind('<Shift-L>', self.test_chuc_nang_tach_tu)

	def pack(self):
		# pack các thành phần giao diện vào đây
		pass

	def test_chuc_nang_tach_tu(self, event):
		self.top_tach_tu = Toplevel(self.root)
		self.test_tach_tu = TestTachTu(self.top_tach_tu, self.disk_db, self.memory_db)
		self.test_tach_tu.pack()


class TestTachTu():
	def __init__(self, root, disk_db, memory_db):
		self.root = root
		self.disk_db = disk_db
		self.memory_db = memory_db

		# text box
		self.textbox = Text(root)
		self.textbox.bind('<ButtonRelease-1>', func=self.get_selected_text)

		# từ được chọn
		self.catch_text = Entry(root)

		# dropdown menu các từ loại
		pos_list = self.memory_db.get_pos()
		self.pos_names = [name for name, description in pos_list]
		self.pos_descriptions = [description for name, description in pos_list]

		self.pos_var = StringVar(root)
		self.pos_var.set(self.pos_descriptions[0])
		self.pos_menu = OptionMenu(root, self.pos_var, *self.pos_descriptions)

		# nút thêm từ vào database
		self.submit_button = Button(root, text='thêm từ', command=self.save_word_pos)

		# nút sửa từ trong database
		self.change_button = Button(root, text='sửa từ', command=self.change_word_pos)

		# nút xóa từ trong database

		# list các từ trong database
		self.tv = ttk.Treeview(root)
		self.tv['columns'] = ['pos']
		self.tv.heading('#0', text='từ')
		self.tv.heading('pos', text='nhãn từ')
		self.tv.bind('<<TreeviewSelect>>', self.tv_select_callback)
		self.tv.config(selectmode='browse')

		# nút tải file
		self.open_button = Button(root, text='mở file', command=self.open_file)

		# nút lưu file
		self.save_button = Button(root, text='lưu file', command=self.save_file)
	
	def pack(self):
		self.textbox.pack()
		self.catch_text.pack()
		self.pos_menu.pack()
		self.submit_button.pack()
		self.change_button.pack()
		self.open_button.pack()
		self.save_button.pack()
		self.tv.pack()

	def get_selected_text(self, event):
		if self.textbox.tag_ranges("sel"):
			text = self.textbox.get("sel.first", "sel.last")
			self.catch_text.delete(0, tk.END)
			self.catch_text.insert(0, text)

	def save_word_pos(self):
		text = self.catch_text.get()
		option = self.pos_var.get()
		pos_index = self.pos_descriptions.index(option)
		pos_name = self.pos_names[pos_index]
		self.memory_db.insert_word_pos(text, pos_name)
		self.tv.insert('', 'end', f'{text}-{pos_name}', text=text)
		self.tv.set(f'{text}-{pos_name}', 'pos', pos_name)

		messagebox.showinfo(title='test lấy kết quả', message=f'lưu từ "{text}" với nhãn "{pos_name}"')

	def tv_select_callback(self, event):
		self.tv_select = self.tv.selection()

	def change_word_pos(self):
		messagebox.showinfo(message=self.tv_select[0])

	def open_file(self):
		self.root.filename = filedialog.askopenfilename(initialdir='./', title='chọn file txt', filetypes=(('text file', '*.txt'),))
		with open(self.root.filename, encoding='utf-8') as file:
			filecontent = file.read()
		self.textbox.delete(1.0, tk.END)
		self.textbox.insert(1.0, filecontent)

	def save_file(self):
		filename = filedialog.asksaveasfilename(confirmoverwrite=False, filetypes=(('csv file', '*.csv'),), defaultextension='.csv')
		data = self.memory_db.get_word_pos()
		df = pd.DataFrame(data, columns=['từ', 'nhãn'])
		df.to_csv(filename, sep=';')
