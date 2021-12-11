"""
Nama	: Aziizah Oki Shofrina
NIM		: 2109106004
Kelas	: Informatika A'21
"""

import sqlite3

# con = sqlite3.connect("database.db")
# cur = con.cursor()

# employees_table = '''CREATE TABLE employees (no integer, level text, nama_karyawan text)'''
# cur.execute(employees_table)

# achievement_table = '''CREATE TABLE achievements (no integer, bulan_tahun text, A integer, B integer, C integer)'''
# cur.execute(achievement_table)

# con.commit()
# con.close()

candies = ('Permen Cokelat', 'Permen Strawberry', 'Permen Kacang')


def employees():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    selected_data = "SELECT level, nama_karyawan FROM employees"
    employees_data = cur.execute(selected_data)
    employees_list = list(employees_data)

    con.commit()
    con.close()
    return employees_list

