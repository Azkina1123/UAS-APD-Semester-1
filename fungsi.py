"""
Nama	: Aziizah Oki Shofrina
NIM		: 2109106004
Kelas	: Informatika A'21
"""

# ||||||||||||||||||||||||||||||||||||||||||||||| FUNCTION |||||||||||||||||||||||||||||||||||||||||||||||
from os import system
from typing import List
from colorama import Fore
import datetime as dt
from data import * 
import sqlite3

# bersihkan layar
def clear_the_screen():
	system('cls')

# bulan ini
def this_month():
	date = dt.date.today()
	month = date.strftime('%B')
	year = date.strftime('%Y')

	return f'{month}, {year}'

# penanda halaman
on_the_page = []
def on_the_new_page():
	if len(on_the_page) == 0:
		return True
	else:
		return False
def on_the_same_page():
	on_the_page.append(1)
def close_the_page():
	on_the_page.clear()
	
# cek karyawan terdaftar
def name_is_available(name):
	nameList = []
	for data in employees():
		level, employee = data
		nameList.append(employee.casefold())
	
	if name.casefold() in nameList:
		return True
	else:
		return False

# menyamakan nama yg diinput dengan data
def same_name(name):
	for data in employees():
		level, employee = data
		if name.casefold() == employee.casefold():
			return employee

# cek karyawan sesuai dgn level
def name_in_levels(name, level):
	name_test = []
	for data in employees():
		level_, employee = data
		name_test.append(employee)
	level_test = []
	for data in employees():
		level_, employee = data
		level_test.append(level_)

	name_index = name_test.index(same_name(name))
	level_index = name_index
	if same_name(name) in name_test:
		return level_test[level_index].casefold() == level.casefold()

# print warning
def print_warning(warning):
	print()
	print(Fore.LIGHTRED_EX + warning.center(50) + Fore.RESET)
	print()

# tambahan gaji
def extra_salary(candy, amount, level):
	extra = 0
	if 5000 < amount <= 6000:
		if candy == 'Permen Cokelat':
			if level == 'A':
				extra += 7000 * 35/100
			elif level == 'B':
				extra += 5000 * 25/100
			else:
				extra += 3000 * 15/100
		else:
			if level == 'A':
				extra += 7000 * 40/100
			elif level == 'B':
				extra += 5000 * 30/100
			else:
				extra += 3000 * 20/100
	elif 4000 <= amount <= 5000:
		if candy == 'Permen Cokelat':
			if level == 'A':
				extra += 7000 * 30/100
			elif level == 'B':
				extra += 5000 * 20/100
			else:
				extra += 3000 * 10/100
		else:
			if level == 'A':
				extra += 7000 * 30/100
			elif level == 'B':
				extra += 5000 * 20/100
			else:
				extra += 3000 * 10/100
	elif 3000 <= amount < 4000:
		if candy == 'Permen Cokelat':
			if level == 'A':
				extra += 7000 * 25/100
			elif level == 'B':
				extra += 5000 * 15/100
			else:
				extra += 3000 * 5/100
		else:
			if level == 'A':
				extra += 7000 * 15/100
			elif level == 'B':
				extra += 5000 * 7/100
			else:
				extra += 3000 * 5/100
	else:
			pass
	return extra

# gaji akhir karyawan
def salary_now(level, extra):
	salary = 0
	if level == 'A':
		salary += (7000 + extra)
	elif level == 'B':
		salary += (5000 + extra)
	else:
		salary += (3000 + extra)
	return salary

# cek pencapaian karyawan sudah diinput
def inputted(name):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	column = '_'.join(this_month().split(', '))
	selected_data = f"SELECT {column} FROM employees WHERE nama_karyawan = '{name}'"
	
	saved_salary = []
	for salary in cur.execute(selected_data):
		for x in salary:
			saved_salary.append(x)

	con.commit()
	con.close()

	if saved_salary[0] == None:
		return False
	else:
		return True

# cek hanya huruf dan spasi
def string_checker(string):
	check = []
	for x in string:
		try:
			convert = int(x)
		except ValueError:
			check.append(x)

	if len(check) == len(string):
		return True
	else:
		return False

# judul halaman
def title(string):
	print("\n\n\n")
	print("-------------------------".center(50))
	print("\033[01m"+ string.center(50) + "\033[0m ")
	print("-------------------------".center(50))

# judul sub halaman
def side_title(string):
	print("\n\n\n")
	print("- - - - - - - - - - - - -".center(50))
	print(string.center(50))
	print("- - - - - - - - - - - - -".center(50))

# petunjuk pengisian
def guide_color(string):
	print(Fore.LIGHTBLACK_EX + string.center(50) + Fore.RESET)

# tambah kolom bulan
def add_salary_per_month_column():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	column_name = '_'.join(this_month().split(', '))
	new_column = f'''ALTER TABLE employees ADD {column_name} integer'''
	cur.execute(new_column)
	con.commit()
	con.close()
# tambah baris bulan
def add_achievement_per_month():
	con = sqlite3.connect("database.db")
	cur = con.cursor()

	saved_data = "SELECT * FROM achievements"
	achievements_data = list(cur.execute(saved_data))

	new_month = f"INSERT INTO achievements VALUES ({len(achievements_data)+1}, '{this_month()}', 0, 0, 0)"
	cur.execute(new_month)

	con.commit()
	con.close()

# tambah data karyawan baru
def add_employee_data(name, level):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	saved_data = "SELECT * FROM employees"
	employees_data = list(cur.execute(saved_data))

	new_data = f"INSERT INTO employees (no, nama_karyawan, level) VALUES ({len(employees_data)+1}, '{name}', '{level}')"
	cur.execute(new_data)
	con.commit()
	con.close()

# tambah data gaji karyawan
def add_employee_salary(name, salary):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	column = '_'.join(this_month().split(', '))
	new_data = f"UPDATE employees SET {column} = {salary} WHERE nama_karyawan = '{name}'"
	cur.execute(new_data)
	con.commit()
	con.close()
# tambah pencapaian perusahaan
def add_achievement(level, value):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	selected_data = f"SELECT {level} FROM achievements WHERE bulan_tahun = '{this_month()}'"
	data = list(cur.execute(selected_data))[0]
	amount = data[0]

	# if amount == None:
	# 	new_achievement = f"UPDATE achievements SET {level} = {value} WHERE bulan_tahun = '{this_month()}'"
	# 	cur.execute(new_achievement)
	# else:
	new_value = amount + value
	new_achievement = f"UPDATE achievements SET {level} = {new_value} WHERE bulan_tahun = '{this_month()}'"
	cur.execute(new_achievement)

	con.commit()
	con.close()

# tampilkan gaji karyawan
def show_employee_salary(name):
	con = sqlite3.connect("database.db")
	cur = con.cursor()

	selected_data1 = "SELECT bulan_tahun FROM achievements"
	months = list(cur.execute(selected_data1))

	selected_data2 = f"SELECT * FROM employees WHERE nama_karyawan = '{name}'"
	data = list(cur.execute(selected_data2))
	data = data[0][3:]

	salaries = []
	num = 1
	for i in range(len(data)):
		salary_per_month = []
		salary_per_month.append(num)
		salary_per_month.append(months[num-1][0])
		if data[i] == None:
			salary_per_month.append("\033[93mBelum diinput.\033[0m")
		else:
			salary_per_month.append(f"Rp{data[i]}")
		salaries.append(salary_per_month)
		num+=1
	return salaries

# tampilkan pencpaian perusahaan
def show_achievements():
	con = sqlite3.connect("database.db")
	cur = con.cursor()

	selected_data = "SELECT * FROM achievements"
	data = list(cur.execute(selected_data))

	con.commit()
	con.close()

	return data

# ubah nama karyawan
def change_the_name(name, new_name):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	change_name = f"UPDATE employees SET nama_karyawan = '{new_name}' WHERE nama_karyawan = '{name}'"
	cur.execute(change_name)
	con.commit()
	con.close()

# ubah level karyawan
def change_the_level(name, new_level):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	change_level = f"UPDATE employees SET level = '{new_level}' WHERE nama_karyawan = '{name}'"
	cur.execute(change_level)
	con.commit()
	con.close()

# hapus data karyawan
def delete_the_employee(name):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	delete_employee = f"DELETE FROM employees WHERE nama_karyawan = '{name}'"
	cur.execute(delete_employee)
	con.commit()
	con.close()

# hitung banyak karyawan
def count_employees():
	a = []
	b = []
	c = []
	for data in employees():
		if data[0] == "A":
			a.append(data)
		elif data[0] == "B":
			b.append(data)
		else:
			c.append(data)

	return len(a), len(b), len(c)
