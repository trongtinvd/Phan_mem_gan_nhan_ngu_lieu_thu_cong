import sqlite3


class MyDatabase:
	def __init__(self, database):
		self.conn = sqlite3.connect(database)
		self.c = self.conn.cursor()
		# các loại từ
		self.pos = [
		('Aa', 'Quality Adjectives'),
		('An', 'Quantity Adjectives'),
		('Cm', 'Prepositions'),
		('Cp', 'Parallel Conjunctions'),
		('Cs', 'Subordinating Conjunctions'),
		('D', 'Directional co-verb'),
		('E', 'Emotion Words'),
		('FW', 'Foreign Words'),
		('ID', 'Idioms'),
		('M', 'Modifiers'),
		('Nc', 'Countable Nouns'),
		('Nn', 'Common Nouns'),
		('Nq', 'Numerals'),
		('Nr', 'Proper Nouns'),
		('Nt', 'Temporal Nouns'),
		('Nu', 'Concrete Nouns'),
		('ON', 'Onomatopoeia'),
		('Pd', 'Demonstrative Pronouns'),
		('Pp', 'Personal Pronouns'),
		('R', 'Adverbs'),
		('Vc', 'Comparative Verbs'),
		('Vd', 'Directional Verbs'),
		('Ve', 'State Verbs'),
		('Vv', 'Volatile Verbs')
		]
		# các thực thể
		self.ne = [
		('NUM', 'Number'),
		('PER', 'Person'),
		('LOC', 'Location'),
		('DTM', 'Date time'),
		('ORG', 'Organization'),
		('MEA', 'Measurement'),
		('TTL', 'Title'),
		('DES', 'Designation'),
		('BRN', 'Brand'),
		('ABB', 'Abbreviation'),
		('TRM', 'Terminology')
		]


	def __del__(self):
		self.conn.close()

	def create_table(self):
		with self.conn:
			self.c.executescript('''
				CREATE TABLE IF NOT EXISTS pos (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				pos_name TEXT NOT NULL UNIQUE,
				pos_description TEXT NOT NULL
				);

				CREATE TABLE IF NOT EXISTS ne (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				ne_name TEXT NOT NULL UNIQUE,
				ne_description TEXT NOT NULL
				);

				CREATE TABLE IF NOT EXISTS word_pos (
				word TEXT NOT NULL,
				pos_id INTEGER NOT NULL,
				PRIMARY KEY(word, pos_id),
				FOREIGN KEY(pos_id) REFERENCES pos(id) ON DELETE CASCADE ON UPDATE NO ACTION
				);

				CREATE TABLE IF NOT EXISTS word_ne (
				word TEXT NOT NULL,
				ne_id INTEGER NOT NULL,
				PRIMARY KEY(word, ne_id),
				FOREIGN KEY(ne_id) REFERENCES ne(id) ON DELETE CASCADE ON UPDATE NO ACTION
				);
				''')

	def insert_basic_pos_and_ne(self):
		with self.conn:
			for pos in self.pos:
				self.c.execute('INSERT OR IGNORE INTO pos(pos_name, pos_description) VALUES(:name, :description)', {'name': pos[0], 'description': pos[1]})
			for ne in self.ne:
				self.c.execute('INSERT OR IGNORE INTO ne(ne_name, ne_description) VALUES(:name, :description)', {'name': ne[0], 'description': ne[1]})

	def print_table(self):
		self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
		print(*self.c.fetchall(), sep='\n')

	def print_pos(self):
		self.c.execute('SELECT * FROM pos')
		print(*self.c.fetchall(), sep='\n')

	def print_ne(self):
		self.c.execute('SELECT * FROM ne')
		print(*self.c.fetchall(), sep='\n')

	def insert_word_pos(self, word, pos):
		with self.conn:
			self.c.execute("SELECT id FROM pos WHERE pos_name = :a_pos", {'a_pos': pos})
			pos_id = self.c.fetchone()[0]
			self.c.execute("INSERT INTO word_pos(word, pos_id) VALUES(:word, :pos_id)", {'word': word, 'pos_id': pos_id})

	def insert_word_ne(self, word, ne):
		with self.conn:
			self.c.execute("SELECT id from ne WHERE ne_name = :a_ne", {'a_ne': ne})
			ne_id = self.c.fetchone()[0]
			self.c.execute("INSERT INTO word_ne(word, ne_id) VALUES(:word, :ne_id)", {'word': word, 'ne_id': ne_id})

	def print_word_pos(self):
		self.c.execute('SELECT * FROM word_pos')
		print(*self.c.fetchall(), sep='\n')

	def print_word_ne(self):
		self.c.execute('SELECT * FROM word_ne')
		print(*self.c.fetchall(), sep='\n')

	def merge_db(self, similar_db):
		similar_db.c.execute('SELECT * FROM word_pos')
		for row in similar_db.c.fetchall():
			self.c.execute('INSERT OR IGNORE INTO word_pos(word, pos_id) VALUES(:word, :pos_id)', {'word': row[0], 'pos_id': row[1]})

		similar_db.c.execute('SELECT * FROM word_ne')
		for row in similar_db.c.fetchall():
			self.c.execute('INSERT OR IGNORE INTO word_ne(word, ne_id) VALUES(:word, :ne_id)', {'word': row[0], 'ne_id': row[1]})




def main():
	db_1 = MyDatabase(':memory:')
	db_1.create_table()
	db_1.insert_basic_pos_and_ne()

	db_2 = MyDatabase(':memory:')
	db_2.create_table()
	db_2.insert_basic_pos_and_ne()

	db_1.insert_word_pos('con mèo', 'Nc')
	db_1.insert_word_pos('con chó', 'Nc')
	db_1.insert_word_ne('hà nội', 'LOC')

	db_2.insert_word_pos('con chó', 'Nc')
	db_2.insert_word_pos('smartphone', 'FW')
	db_2.insert_word_ne('chí phèo', 'PER')


	print('--------------------------------')
	db_1.print_table()
	print('--------------------------------')
	db_1.print_ne()
	print('--------------------------------')
	db_1.print_pos()

	print('--------------------------------')
	db_1.print_word_pos()
	db_1.print_word_ne()
	print('--------------------------------')
	db_2.print_word_pos()
	db_2.print_word_ne()

	print('--------------------------------')
	db_1.merge_db(db_2)
	db_1.print_word_pos()
	db_1.print_word_ne()


if __name__ == '__main__':
	main()