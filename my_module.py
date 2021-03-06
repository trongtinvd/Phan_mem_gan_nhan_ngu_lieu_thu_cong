import tkinter as tk
import pandas as pd
import re
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
		self.root.bind('<Shift-P>', self.test_dan_nhan_thuc_the)


	def pack(self):
		# pack các thành phần giao diện vào đây
		pass


	def test_chuc_nang_tach_tu(self, event):
		top_level = Toplevel(self.root)
		tach_tu = TestTachTu(top_level, self.disk_db, self.memory_db)
		tach_tu.pack()

		top_level.grab_set()
		top_level.wait_window()
		top_level.grab_release()


	def test_dan_nhan_thuc_the(self, event):
		top_level = Toplevel(self.root)
		dan_nhan_thuc_the = DanNhanThucThe(top_level, self.disk_db, self.memory_db)
		dan_nhan_thuc_the.pack()

		top_level.grab_set()
		top_level.wait_window()
		top_level.grab_release()


class TestTachTu():
	def __init__(self, root, disk_db, memory_db):
		self.root = root
		self.disk_db = disk_db
		self.memory_db = memory_db

		# text box
		self.textbox = CustomText(root)
		self.textbox.bind('<ButtonRelease-1>', func=self.get_selected_text)
		self.textbox.tag_configure('yellow_background', background='#ffff00')

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
		self.submit_button = Button(root, text='Thêm từ', command=self.submit_word_pos)

		# nút sửa từ trong database
		self.change_button = Button(root, text='Sửa từ', command=self.change_word_pos)

		# nút xóa từ trong database
		self.delete_button = Button(root, text='Xóa từ', command=self.delete_word_pos)

		# list các từ trong database
		self.table = ttk.Treeview(root)
		self.table['columns'] = ['pos']
		self.table.heading('#0', text='Từ')
		self.table.heading('pos', text='Nhãn từ')
		self.table.bind('<<TreeviewSelect>>', self.table_select_callback)
		self.table.config(selectmode='browse')
		self.update_table()

		# nút mở file
		self.open_button = Button(root, text='Mở file', command=self.open_file)

		# nút lưu file
		self.save_button = Button(root, text='Lưu file', command=self.save_file)

	
	def pack(self):
		self.textbox.pack()
		self.catch_text.pack()
		self.pos_menu.pack()
		self.submit_button.pack()
		self.change_button.pack()
		self.delete_button.pack()
		self.open_button.pack()
		self.save_button.pack()
		self.table.pack()


	def get_selected_text(self, event):
		if self.textbox.tag_ranges("sel"):
			text = self.textbox.get("sel.first", "sel.last")
			self.catch_text.delete(0, tk.END)
			self.catch_text.insert(0, text)


	def submit_word_pos(self):
		text = self.catch_text.get()
		option = self.pos_var.get()
		pos_index = self.pos_descriptions.index(option)
		pos_name = self.pos_names[pos_index]
		if text == '':
			messagebox.showerror(parent=self.root, title='Lỗi dữ liệu đầu vào', message='Từ thêm vào database không được phép rỗng.')
		else:
			self.memory_db.insert_word_pos(text, pos_name)
			self.update_table()
			self.hightlight_text()
			self.remove_select_text()
			messagebox.showinfo(title='test lấy kết quả', parent=self.root, message=f'lưu từ "{text}" với nhãn "{pos_name}"')


	def update_table(self):
		self.table.delete(*self.table.get_children())
		fetch_data = self.memory_db.get_word_pos()
		for word, pos in fetch_data:
			self.table.insert(parent='', index='end', iid=f'{word}-{pos}', text=word)
			self.table.set(item=f'{word}-{pos}', column='pos', value=pos)

	
	def hightlight_text(self):
		self.textbox.tag_remove('yellow_background', '1.0', tk.END)

		fetch_data = self.memory_db.get_word_pos()
		words = [re.escape(word) for (word, pos) in fetch_data]
		self.textbox.highlight_pattern('|'.join(words), 'yellow_background', regexp=True)


	def remove_select_text(self):
		if self.textbox.tag_ranges('sel'):
			self.textbox.tag_remove(tk.SEL, "1.0", tk.END)


	def table_select_callback(self, event):
		self.table_select = self.table.focus()


	def change_word_pos(self):
		try:
			values = re.compile(r'(\-)(?!.*\-)').split(self.table_select)

			top_level = Toplevel(self.root)
			question_box = MySelectionBox(top_level, values[0], values[2], self.memory_db)
			question_box.pack()

			top_level.grab_set()
			top_level.wait_window()
			top_level.grab_release()
			self.update_table()
			self.hightlight_text()
		except AttributeError:
			messagebox.showerror(parent=self.root, title='Chưa có từ nào được chọn', message='Xin hãy chọn từ cần được sửa')


	def delete_word_pos(self):
		try:
			values = re.compile(r'(\-)(?!.*\-)').split(self.table_select)
			response = messagebox.askokcancel(parent=self.root, title='Xác nhận xóa', message=f'Xác nhận xóa từ "{values[0]}" với nhãn {values[2]}?')
			if response == 1:
				self.memory_db.delete_word_pos(values[0], values[2])
		
				self.update_table()
				self.hightlight_text()
		except AttributeError:
			messagebox.showerror(parent=self.root, title='Chưa có từ nào được chọn', message='Xin hãy chọn từ cần được xóa')


	def open_file(self):
		self.root.filename = filedialog.askopenfilename(parent=self.root, initialdir='./', title='chọn file txt', filetypes=(('text file', '*.txt'),))
		
		if self.root.filename != '':
			with open(self.root.filename, encoding='utf-8') as file:
				filecontent = file.read()
			self.textbox.delete(1.0, tk.END)
			self.textbox.insert(1.0, filecontent)


	def save_file(self):
		filename = filedialog.asksaveasfilename(parent=self.root, confirmoverwrite=False, filetypes=(('csv file', '*.csv'),), defaultextension='.csv')
		
		if filename != '':
			data = self.memory_db.get_word_pos()
			df = pd.DataFrame(data, columns=['từ', 'nhãn'])
			df.to_csv(filename, sep=';')


class MySelectionBox():
	def __init__(self, root, word, pos, db):
		self.root = root
		self.root.geometry('250x100')
		self.root.title('Sửa nhãn từ')

		self.word = word
		self.pos = pos
		self.db = db
		self.entry = Entry(root)
		self.entry.insert(0, word)
		self.pos_names = [name for name, description in db.pos]
		self.pos_descriptions = [description for name, description in db.pos]
		self.var = StringVar()
		self.var.set(self.pos_descriptions[self.pos_names.index(pos)])
		self.menu = OptionMenu(root, self.var, *self.pos_descriptions)
		self.button = Button(root, text='sửa', command=self.change)


	def pack(self):
		self.entry.pack()
		self.menu.pack()
		self.button.pack()


	def change(self):
		new_word = self.entry.get()
		new_pos = self.pos_names[self.pos_descriptions.index(self.var.get())]
		if new_word == '':
			messagebox.showerror(parent=self.root, title='Lỗi dữ liệu đầu vào', message='Phần từ không được phép trống.')
		elif self.word == new_word and self.pos == new_pos:
			messagebox.showerror(parent=self.root, title='Lỗi dữ liệu đầu vào', message='Nội dung thay đổi phải khác với nội dung ban đầu')
		else:
			self.db.update_word_pos(self.word, self.pos, new_word, new_pos)
			messagebox.showinfo(parent=self.root, title='Chỉnh sửa thành công', message=f'Từ "{self.word}" với nhãn "{self.pos}" đã được thay bằng từ "{new_word}" với nhãn "{new_pos}"')
			self.word, self.pos = new_word, new_pos


# https://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget
class CustomText(tk.Text):
	'''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
	def __init__(self, *args, **kwargs):
		tk.Text.__init__(self, *args, **kwargs)

	def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
		'''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

		start = self.index(start)
		end = self.index(end)
		self.mark_set("matchStart", start)
		self.mark_set("matchEnd", start)
		self.mark_set("searchLimit", end)

		count = tk.IntVar()
		while True:
			index = self.search(pattern, "matchEnd","searchLimit", count=count, regexp=regexp)
			if index == "": break
			if count.get() == 0: break # degenerate pattern which matches zero-length strings
			self.mark_set("matchStart", index)
			self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
			self.tag_add(tag, "matchStart", "matchEnd")


class DanNhanThucThe():
	def __init__(self, root, disk_db, memory_db):
		self.root = root
		self.disk_db = disk_db
		self.memory_db = memory_db

		# text box
		self.textbox = CustomText(self.root)
		self.textbox.bind('<ButtonRelease-1>', func=self.get_selected_text)
		self.textbox.tag_configure('yellow_background', background='#ffff00')

		# từ được chọn
		self.catch_text = Entry(self.root)

		# menu thực thể
		ne_list = self.memory_db.get_ne() 
		self.ne_names = [name for name, description in ne_list]
		self.ne_descriptions = [description for name, description in ne_list]

		self.ne_var = StringVar(self.root)
		self.ne_var.set(self.ne_descriptions[0])
		self.ne_menu = OptionMenu(self.root, self.ne_var, *self.ne_descriptions)

		# nút thêm thực thể vào database
		self.submit_button = Button(self.root, text='Thêm thực thể', command=self.submit_word_ne)

		# nút sửa thực thể trong database
		self.change_button = Button(self.root, text='Sửa thực thể', command=self.change_word_ne)

		# nút xóa thực thể trong database
		self.delete_button = Button(self.root, text='Xóa thực thể', command=self.delete_word_ne)

		# list các thực thể trong database
		self.table = ttk.Treeview(self.root)
		self.table['columns'] = ['ne']
		self.table.heading('#0', text='Từ')
		self.table.heading('ne', text='Thực thể')
		self.table.bind('<<TreeviewSelect>>', self.table_select_callback)
		self.table.config(selectmode='browse')
		self.update_table()

		# nút mở file
		self.open_button = Button(self.root, text='Mở file', command=self.open_file)

		# nút lưu file
		self.save_button = Button(self.root, text='Lưu file', command=self.save_file)


	def pack(self):
		self.textbox.pack()
		self.catch_text.pack()
		self.ne_menu.pack()
		self.submit_button.pack()
		self.change_button.pack()
		self.delete_button.pack()
		self.open_button.pack()
		self.save_button.pack()
		self.table.pack()


	def get_selected_text(self, event):
		if self.textbox.tag_ranges("sel"):
			text = self.textbox.get("sel.first", "sel.last")
			self.catch_text.delete(0, tk.END)
			self.catch_text.insert(0, text)


	def submit_word_ne(self):
		text = self.catch_text.get()
		option = self.ne_var.get()
		ne_index = self.ne_descriptions.index(option)
		ne_name = self.ne_names[ne_index]
		if text == '':
			messagebox.showerror(parent=self.root, title='Lỗi dữ liệu đầu vào', message='Từ thêm vào database không được phép rỗng.')
		else:
			self.memory_db.insert_word_ne(text, ne_name)
			self.update_table()
			self.hightlight_text()
			self.remove_select_text()
			messagebox.showinfo(title='Lưu thành công', parent=self.root, message=f'Thêm từ "{text}" với nhãn "{ne_name}"')


	def update_table(self):
		self.table.delete(*self.table.get_children())
		fetch_data = self.memory_db.get_word_ne()
		for word, ne in fetch_data:
			self.table.insert(parent='', index='end', iid=f'{word}-{ne}', text=word)
			self.table.set(item=f'{word}-{ne}', column='ne', value=ne)

	
	def hightlight_text(self):
		self.textbox.tag_remove('yellow_background', '1.0', tk.END)

		fetch_data = self.memory_db.get_word_ne()
		words = [re.escape(word) for (word, ne) in fetch_data]
		self.textbox.highlight_pattern('|'.join(words), 'yellow_background', regexp=True)


	def remove_select_text(self):
		if self.textbox.tag_ranges('sel'):
			self.textbox.tag_remove(tk.SEL, "1.0", tk.END)


	def table_select_callback(self, event):
		self.table_select = self.table.focus()


	def change_word_ne(self):
		try:
			values = re.compile(r'(\-)(?!.*\-)').split(self.table_select)

			top_level = Toplevel(self.root)
			question_box = ChangeNeWindow(top_level, values[0], values[2], self.memory_db)
			question_box.pack()

			top_level.grab_set()
			top_level.wait_window()
			top_level.grab_release()
			self.update_table()
			self.hightlight_text()
		except AttributeError:
			messagebox.showerror(parent=self.root, title='Chưa có từ nào được chọn', message='Xin hãy chọn từ cần được sửa')


	def delete_word_ne(self):
		try:
			values = re.compile(r'(\-)(?!.*\-)').split(self.table_select)
			response = messagebox.askokcancel(parent=self.root, title='Xác nhận xóa', message=f'Xác nhận xóa từ "{values[0]}" với thực thể {values[2]}?')
			if response == 1:
				self.memory_db.delete_word_ne(values[0], values[2])
		
				self.update_table()
				self.hightlight_text()
		except AttributeError:
			messagebox.showerror(parent=self.root, title='Chưa có từ nào được chọn', message='Xin hãy chọn từ cần được xóa')


	def open_file(self):
		self.root.filename = filedialog.askopenfilename(parent=self.root, initialdir='./', title='chọn file txt', filetypes=(('text file', '*.txt'),))
		
		if self.root.filename != '':
			with open(self.root.filename, encoding='utf-8') as file:
				filecontent = file.read()
			self.textbox.delete(1.0, tk.END)
			self.textbox.insert(1.0, filecontent)


	def save_file(self):
		filename = filedialog.asksaveasfilename(parent=self.root, confirmoverwrite=False, filetypes=(('csv file', '*.csv'),), defaultextension='.csv')
		
		if filename != '':
			data = self.memory_db.get_word_ne()
			df = pd.DataFrame(data, columns=['từ', 'thực thể'])
			df.to_csv(filename, sep=';')


class ChangeNeWindow():
	def __init__(self, root, word, ne, db):
		self.root = root
		self.root.geometry('250x100')
		self.root.title('Sửa thực thể')

		self.word = word
		self.ne = ne
		self.db = db
		self.entry = Entry(self.root)
		self.entry.insert(0, word)
		self.ne_names = [name for name, description in db.ne]
		self.ne_descriptions = [description for name, description in db.ne]
		self.var = StringVar()
		self.var.set(self.ne_descriptions[self.ne_names.index(ne)])
		self.menu = OptionMenu(root, self.var, *self.ne_descriptions)
		self.button = Button(root, text='sửa', command=self.change)


	def pack(self):
		self.entry.pack()
		self.menu.pack()
		self.button.pack()


	def change(self):
		new_word = self.entry.get()
		new_ne = self.ne_names[self.ne_descriptions.index(self.var.get())]
		if new_word == '':
			messagebox.showerror(parent=self.root, title='Lỗi dữ liệu đầu vào', message='Phần từ không được phép trống.')
		elif self.word == new_word and self.ne == new_ne:
			messagebox.showerror(parent=self.root, title='Lỗi dữ liệu đầu vào', message='Nội dung thay đổi phải khác với nội dung ban đầu')
		else:
			self.db.update_word_ne(self.word, self.ne, new_word, new_ne)
			messagebox.showinfo(parent=self.root, title='Chỉnh sửa thành công', message=f'Từ "{self.word}" với thực thể "{self.ne}" đã được thay bằng từ "{new_word}" với thực thể "{new_ne}"')
			self.word, self.ne = new_word, new_ne