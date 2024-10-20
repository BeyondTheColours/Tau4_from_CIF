import sys
import math

def get_angle_lines(cif_file_text, atom):

	angles_text = cif_file_text.split("_geom_angle_publ_flag\n")[1].split("loop_")[0]
	angles_text_list = angles_text.split("\n")

	angles_text_list_cleaned = []
	for i in angles_text_list:
		temp = ""
		if i.split(" ")[0] == "":
			for j in i.split(" "):
				if j != "":
					temp += j + " "
			angles_text_list_cleaned.append(temp)
		else:
			angles_text_list_cleaned.append(i)

	angles_at_atom = []
	for i in angles_text_list_cleaned:
		temp = i.split(" ")
		try:
			if temp[1] == atom:
				angles_at_atom.append(temp)
		except IndexError:
			pass

	if len(angles_at_atom) > 6:
		return f"\nError - more than six angles found around {atom}. Cannot compute Tau4."
	if 6 > len(angles_at_atom) > 0:
		pluraliser = 0
		if len(angles_at_atom) > 1:
			pluraliser = 1
		return f"\nError - only {len(angles_at_atom)} angle{pluraliser*'s'} found around \"{atom}\". Cannot compute Tau4."
	if len(angles_at_atom) == 0:
		return f"\nError - No angles around \"{atom}\" were found."
		
	return angles_at_atom

def get_angle_values(angles_line_list):
	res = []
	for i in angles_line_list:
		temp = i[3].split("(")
		val = float(temp[0])
		res.append(val)

	return res


def get_largest_2_angles(angles_list):
	largest = 0
	second_largest = 0
	for i in angles_list:
		if i >= second_largest:
			if i <= largest:
				second_largest = i
			else:
				second_largest = largest
				largest = i

	return [largest, second_largest]
			
def calc_tau4(a,b):
	theta = math.acos(-1/3)*(180/math.pi)
	top = (360-a-b)
	bottom = 360-(2*theta)
	return top/bottom

def get_tau4(cif_file):

	try:
		with open(cif_file,"r") as f:	
			angles_lines = get_angle_lines(f.read(),central_atom)

			f.close()
	except FileNotFoundError:
		return f"\nFile \"{cif_file}\" could not be found.\nCheck the spelling of the file name and path is all correct."

	if type(angles_lines) != list:

		return angles_lines
	else:
		angle_values = get_angle_values(angles_lines)
		largest_2_angles = get_largest_2_angles(angle_values)

		tau4 = calc_tau4(largest_2_angles[0], largest_2_angles[1])
		return tau4

try:
	cif = sys.argv[1]
except IndexError:
	print("No file or central atom provided")
	exit()

try:
	central_atom = sys.argv[2]
except: IndexError:
	print(f"Cannot calculate Tau4 for CIF \"{cif}\" because no central atom has been specificed")
	exit()

try:
	print(f"Tau4 calculated at {central_atom} is {round(get_tau4(cif),2)}\n(To 2 decimal places)")
except TypeError:
	print(get_tau4(cif))