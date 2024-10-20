import sys
import math
import re

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

    return angles_at_atom

def validate_angle_line_list(angle_line_list):
    if len(angle_line_list) == 6:
        return angle_line_list
    return None

def explain_angle_list_issue(angle_line_list, central_atom):
    l = len(angle_line_list)
    pluraliser = 0
    if 6 > l > 0:
        if l > 1:
            pluraliser = 1
        return f"Only {l} angle{pluraliser*'s'} found at {central_atom}.\nFor a four-coordinate atom there should be six.\nMake sure the correct central atom was provided!"
    elif l == 0:
        return f"No angles were found at {central_atom}."
    else:
        return f"Too many angles ({l}) were found at {central_atom}.\nFor a four-coordinate atom there should be six.\nMake sure the correct central atom was provided!"

def get_angle_values(angle_line_list):
    res = []
    for i in angle_line_list:
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

def get_tau4(cif_file, central_atom):
    try:
        with open(cif_file,"r") as f:    
            angles_lines = get_angle_lines(f.read(), central_atom)
            f.close()
    
    except FileNotFoundError:
        return None

    if validate_angle_line_list(angles_lines) is not None:
        angle_values = get_angle_values(angles_lines)
        largest_2_angles = get_largest_2_angles(angle_values)
        tau4 = calc_tau4(largest_2_angles[0], largest_2_angles[1])

    else:
        explain_angle_list_issue(angles_lines, central_atom)
        return None

    return tau4

try:
    cif = sys.argv[1]
    if (re.search(".cif", cif)):
        pass
    else:
        print(f"File path \'{cif}\' does not contain a valid .cif file")
        print("Exiting the program")
        exit()
except IndexError:
    print("No file or central atom provided")
    exit()

try:
    central_atom = sys.argv[2]
except IndexError:
    print(f"Cannot calculate Tau4 for CIF \"{cif}\" because no central atom has been specificed")
    exit()

tau4 = get_tau4(cif, central_atom)

if tau4 is not None:
    print(tau4)
else:
    print("Something went wrong")


