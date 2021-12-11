"""
Nama	: Aziizah Oki Shofrina
NIM		: 2109106004
Kelas	: Informatika A'21
"""

# ||| PAGES ||| ----------------------------------------------------------
from colorama import Fore
import matplotlib.pyplot as plt
from fungsi import *
from data import *


# Tampilan Awal
def homeScreen(warning):
	try :
		add_salary_per_month_column()
		add_achievement_per_month()
	except sqlite3.OperationalError:
		pass
	
	clear_the_screen()
	title(" || Perusahaan Permen || ")
	print_warning(warning)
	print(f"\t{' '*3}(1) Data Individu Karyawan\n\t{' '*3}(2) Daftarkan Karyawan Baru\n\t{' '*3}(3) Diagram Perusahaan Bulan Ini")
	guide_color("('0' untuk keluar dari program)")

	input_opsi = input("\n\t\t>>> ")

	if input_opsi == '1':
		findEmployee('')
	elif input_opsi == '2':
		addEmployee('')
	elif input_opsi == '3':
		showAchievements()
	elif input_opsi == '0':
		end('')
	else:
		homeScreen("Opsi tidak tersedia!")

# Pilih Karyawan
def findEmployee(warning):
	clear_the_screen()
	title("Karyawan Perusahaan")
	guide_color("(Ketik '0' untuk kembali)")
	print_warning(warning)

	if on_the_new_page() is True:
		global show_name
		show_name = []

	try:
		print(f"\t{' '*3}{'Nama Karyawan'.ljust(15)}: {show_name[0]}")
	except IndexError:
		input_name = input(f"\t{' '*3}{'Nama Karyawan'.ljust(15)}: ")
		if input_name == '0':
			close_the_page()
			homeScreen('')
		elif name_is_available(input_name) is True:
			show_name.append(input_name)
		else:
			on_the_same_page()
			findEmployee("Karyawan tidak terdaftar!")

	level = input(f"\t{' '*3}{'Level'.ljust(15)}: ")
	level = level.upper()
	if level == '0':
		close_the_page()
		homeScreen('')
	elif name_in_levels(show_name[0], level) is True:
		close_the_page()
		employeeMenu(show_name[0], level, "")
	else:
		on_the_same_page()
		findEmployee(f"Karyawan bukan level {level}!")
		
# Menu Karyawan
def employeeMenu(name, level, warning):
	clear_the_screen()
	title("Data Karyawan")
	employee = same_name(name)
	print(f"\n\t{'Nama Karyawan'.ljust(15)}: {employee}\n\t{'Level'.ljust(15)}: {level}")
	print_warning(warning)

	print(f"\t{' '*3}(1) Input Bungkusan Bulanan\n\t{' '*3}(2) Tampilkan Riwayat Kerja\n\t{' '*3}(3) Edit Data Karyawan")
	print(Fore.LIGHTBLACK_EX + "--- ['0' untuk keluar] ---".center(50) + Fore.RESET)
	
	input_opsi = input("\n\t>>> ")

	if input_opsi == '1':
		employeeIncome(employee, level, "")
	elif input_opsi == '2':
		showHistory(employee, level)
	elif input_opsi =='3':
		editEmployee(employee, level, "")
	elif input_opsi == '0':
		homeScreen('')
	else:
		employeeMenu(name, level, "Opsi tidak tersedia!")

# Isi Capaian Karyawan
def employeeIncome(name, level, warning):
	clear_the_screen()
	side_title("Pencapaian Karyawan")
	guide_color("(Ketik '--' untuk membatalkan pengisian)")
	print_warning(warning)
	print(f"\t{this_month()}")
	print(f"\t{'Nama Karyawan'.ljust(15)}: {name}\n\t{'Level'.ljust(15)}: {level}")

	if on_the_new_page() is True:
		global show_amount
		show_amount = []

	if inputted(name) is False:
		index = 0
		total_amount = 0
		slot = 6000
		salary = salary_now(level, 0)
		for candy in candies:
			
			print("\n\t\033[04m" + candy + "\033[0m")
			
			try:
				print(f"\tJumlah bungkus bulan ini : {show_amount[index]}")
			except IndexError:
				try:
					input_amount = input("\tJumlah bungkus bulan ini : ")
					if input_amount == '--':
						close_the_page()
						employeeMenu(name, level, "")

					input_amount = int(input_amount)
					if input_amount < 0:
						on_the_same_page()
						employeeIncome(name, level, "Jumlah bungkusan salah!")
					
					show_amount.append(input_amount)
				except ValueError:
					on_the_same_page()
					employeeIncome(name, level, "Masukkan angka!")
			
			total_amount += show_amount[index]
			amount = 0
			if show_amount[index] < 3000:
				pass
			else:
				if slot == 6000:
					amount += show_amount[index]
					slot -= show_amount[index]
				elif slot > 0:
					amount += slot
				else:
					pass
				
			extra = extra_salary(candy, amount, level)
			if extra > 0:
				print(Fore.LIGHTGREEN_EX + f"\t+ Rp{extra}" + Fore.RESET)
			
			index += 1
			salary += extra

		add_employee_salary(name, salary)
		add_achievement(level, total_amount)


		print(f"\n\tGaji bulan ini adalah " + Fore.LIGHTCYAN_EX + "\033[04mRp" + str(salary) + Fore.RESET + "\033[0m")
	else:
		print(Fore.LIGHTYELLOW_EX + f'\n\tPencapaian bulan ini telah diinput.'+ Fore.RESET)

	input("\n\tKembali => ")

	close_the_page()
	employeeMenu(name, level, '')

# Tampilkan Riwayat Karyawan
def showHistory(name, level):
	clear_the_screen()
	side_title("Riwayat Kerja Karyawan")
	print(f"\n\t{'Nama Karyawan'.ljust(15)}: {name}\n\t{'Level'.ljust(15)}: {level}")

	data = show_employee_salary(name)

	if len(data) == 0:
		print(Fore.LIGHTYELLOW_EX + "\n\tBelum ada pencapaian pada karyawan ini." + Fore.RESET)
	else:
		print()
		for per_month in data:
			print(f"\t{per_month[0]}. {per_month[1]} : {per_month[2]}")
				
	input("\n\tKembali => ")
	employeeMenu(name, level, '')

# Edit Data Karyawan
def editEmployee(name, level, warning):
	clear_the_screen()
	side_title("Edit Data Karyawan")
	employee = same_name(name)
	print(f"\n\t{'Nama Karyawan'.ljust(15)}: {employee}\n\t{'Level'.ljust(15)}: {level}")
	print_warning(warning)

	print(f"\t{' '*3}(1) Ubah Nama Karyawan\n\t{' '*3}(2) Ubah Level Karyawan\n\t{' '*3}(3) Hapus Seluruh Data")
	print(Fore.LIGHTBLACK_EX + f"\t{' '*3}    ('0' untuk keluar)    " + Fore.RESET)

	input_opsi = input("\n\t>>> ")

	if input_opsi == '1':
		change_name(name, level, "")
	elif input_opsi == '2':
		change_level(name, level, "")
	elif input_opsi == '3':
		delete_data(name, level)
	elif input_opsi == '0':
		employeeMenu(name, level, "")
	else:
		editEmployee(name, level, "Opsi tidak tersedia!")

# ubah nama
def change_name(name, level, warning):
	clear_the_screen()
	print("\n\n\n")
	guide_color("[Ketik '--' untuk membatalkan pengisian]")
	print_warning(warning)
	print("\t\033[04mUbah Nama Karyawan\033[0m")
	new_name = input(f"\n\t□ {name} --> ")
	if new_name == "--":
		editEmployee(name, level, "Ubah nama dibatalkan.")
	elif name_is_available(new_name) is True:
		change_name(name, level, "Nama karyawan telah terdaftar!")
	elif string_checker(new_name) is False or new_name.isspace() is True or new_name == "":
		change_name(name, level, "Harap isi nama dengan alfabet!")
	else:
		change_the_name(name, new_name)
		print(Fore.LIGHTGREEN_EX + "\n\tUbah nama berhasil!" + Fore.RESET)
		input("\n\tKembali => ")
		editEmployee(new_name, level,"")
# ubah level
def change_level(name, level, warning):
	clear_the_screen()
	print("\n\n\n")
	guide_color("[Ketik '--' untuk membatalkan pengisian]")
	print_warning(warning)
	print("\t\033[04mUbah Level Karyawan\033[0m")
	# print(Fore.LIGHTYELLOW_EX + f"\tCatatan:\
	# 	\n{' '*5}a. Jika karyawan memiliki potensi kerja\n{' '*5}   yang baik, level dapat ditingkatkan.\
	# 	\n{' '*5}b. Jika pencapaian kerja karyawan memburuk\n{' '*5}   tanpa alasan jelas, level dapat diturunkan.\
	# 	\n{' '*5}c. Diharapkan Anda bersikap profesional." + Fore.RESET)
	new_level = input(f"\n\t□ {level} --> ")
	new_level = new_level.upper()

	if new_level == "--":
		editEmployee(name, level, "Ubah level dibatalkan.")
	if new_level not in ("A", "B", "C"):
		change_level(name, level, "Level (A / B / C)!")
	else:
		change_the_level(name, new_level)
		print(Fore.LIGHTGREEN_EX + "\n\tUbah level berhasil!" + Fore.RESET)
		input("\n\tKembali => ")
		editEmployee(name, new_level, "")
# hapus data
def delete_data(name, level):
	print()
	print(Fore.LIGHTMAGENTA_EX + "Aktivitas ini akan menghapus".center(50))
	print("seluruh data tersimpan,".center(50))
	print("mulai dari identitas karyawan".center(50))
	print("hingga pencapaian tiap bulannya.".center(50) + Fore.RESET)
	guide_color(f"(Ketik '{name}/{level}' untuk hapus)")
	delete = input("\n\t>>> ")
	if delete == f"{name}/{level}":
		delete_the_employee(name)
		homeScreen(f"Data karyawan {name} level {level} telah dihapus.")
	else:
		editEmployee(name, level, "Hapus data dibatalkan.")

# Tambahkan Karyawan Baru	
def addEmployee(warning):
	clear_the_screen()
	title("Daftarkan Karyawan Baru")
	guide_color("(Ketik '--' untuk membatalkan pendaftaran)")
	print_warning(warning)

	if on_the_new_page() is True:
		global show_input_name
		show_input_name = []

	try:
		print(f"\t{'Nama Karyawan'.ljust(15)}: {show_input_name[0]}")
	except IndexError:
		input_name = input(f"\t{'Nama Karyawan'.ljust(15)}: ")
		if input_name == '--':
			close_the_page()
			homeScreen('')
		elif name_is_available(input_name) is True:
			on_the_new_page()
			addEmployee("Nama karyawan telah terdaftar!")
		elif string_checker(input_name) is False or input_name.isspace() is True or input_name == "":
			on_the_same_page()
			addEmployee("Harap isi nama dengan alfabet!")
		show_input_name.append(input_name)

	input_level = input(f"\t{'Level'.ljust(15)}: ")
	input_level = input_level.upper()
	
	if input_level == '--':
		close_the_page()
		homeScreen('')
	elif input_level not in ('A', 'B', 'C'):
		on_the_same_page()
		addEmployee('Level karyawan (A / B / C)!')
		
	add_employee_data(show_input_name[0], input_level)

	close_the_page()
	print(Fore.LIGHTGREEN_EX + "\n\tKaryawan baru berhasil ditambahkan!" + Fore.RESET)
	input('\n\tKembali => ')
	homeScreen('')

# Tampilkan Pencapaian Perusahaan
def showAchievements():
	clear_the_screen()
	print("\n\n\n\n\n\n\n\n\n\n")
	input("\t\tTampilkan diagram => ")
	plt.subplot(1, 2, 1)

	data = show_achievements()
	month = data[len(data)-1]
	amount = month[2:]
	levels = ["A", "B", "C"]
	
	plt.title("Permen Terbungkus\n" + month[1], size=10)
	plt.axis([-1, len(levels), 0, max(amount)+5000])
	plt.yticks(amount)
	index = 0
	for level in levels:
		plt.bar(level, amount[index], color='#8564d3')
		index+=1
	del data
	
	plt.subplot(1, 2, 2)

	data = employees()
	a, b, c = count_employees()
	
	plt.title("Karyawan Saat Ini", size=10)
	plt.axis([-1, len(levels), 0, len(data)+5])
	plt.yticks([a, b, c])

	plt.bar("A", a, color='#c00071')
	plt.bar("B", b, color='#c00071')
	plt.bar("C", c, color='#c00071')

	plt.show()
	print()
	print(Fore.LIGHTCYAN_EX + "Diagram telah ditampilkan".center(50) + Fore.RESET)
	input(f"\n\tKembali => ")
	homeScreen("")

# Keluar dari Program
def end(warning):
	clear_the_screen()
	print("\n\n\n")
	print_warning(warning)

	print ("Apakah Anda yakin ingin keluar?".center(50))
	guide_color("('0' untuk Tidak, '1' untuk Ya)")
	keluar = input("\n\t>>> ")
	if keluar == '0':
		clear_the_screen()
		input('\n\n\n\n\n\n\n\n\n\n\n\tKembali ke lobi => ')
		homeScreen('')
	elif keluar == '1':
		clear_the_screen()
		print("\n\n\n\n\n\n\n\n\n")
		print("Terima kasih telah menggunakan program ~".center(50))
		input('\n\tKeluar => ')
		exit()
	else:
		end("Ketik '0' atau '1'!")

