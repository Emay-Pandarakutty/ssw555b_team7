"""
#===========================================================================================#
Subject         : SSW -555(Agile Methods for Software Development) 
Assignment      : P03: Continue programming, create version control repository
Script Author   : Team#7
Date            : 02/20/2021
Script Name     : SSW555-Porject.py
#===========================================================================================#

Purpose:
--------
After reading all of the data, print the unique identifiers and names of each of
 the individuals in order by their unique identifiers. Then, for each family,
 print the unique identifiers and names of the husbands and wives, in order
 by unique family identifiers.
---------------------------------------------------------------------------------------------

"""

import sys
from prettytable import PrettyTable
from datetime import datetime
import validity_test
from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement

print('Enter file name with extension when prompted  e.g : test.ged \n')

# Dictionary  from Project file
Tag_Level = {
    'INDI': 0,
    'NAME': 1,
    'SEX': 1,
    'BIRT': 1,
    'DEAT': 1,
    'FAMC': 1,
    'FAMS': 1,
    'FAM': 0,
    'MARR': 1,
    'HUSB': 1,
    'WIFE': 1,
    'CHIL': 1,
    'DIV': 1,
    'DATE': 2,
    'HEAD': 0,
    'TRLR': 0,
    'NOTE': 0}


Ind = PrettyTable(["ID", "NAME"])
Fam = PrettyTable(["ID", "Husband Name", "Wife Name"])
ind = []
fam = []
ind_list = []
individuals = []
families = []
read_dates = []

class Individual:
    def __init__(self, ind_id):
        self.ind_id = ind_id
        self.name = None
        self.sex = None
        self.birth_d = None
        self.death_d = None
        self.spouse_id = None
        self.child_id = None

class Family:
    def __init__(self, fam_id):
        self.fam_id = fam_id
        self.marriage_d = None
        self.hus_id = None
        self.wife_id = None
        self.children = []
        self.divorce_d = None

def date_before(dates):

    valid = False
    try:
        for date in dates:
            if date != None:
                f_date = datetime.strptime(date.rstrip(), '%d %b %Y').date()
                c_date = datetime.now().date()
                if f_date > c_date:
                    valid = True
    except: valid = None

    return valid

def data_match(splitline):
    data_found = False
    index = 1  # default value
    for key, val in Tag_Level.items():
        if key in splitline:
            index = splitline.index(key)
        if key == splitline[index] and val == int(splitline[0]):
            data_found = True
            break
    return data_found, index

def strip_valid_line(line):
    splitline = []
    line = line.strip()  # Return a copy of the sequence with specified leading and trailing bytes removed (spaces)
    if len(line) > 1:  # ignored any data without 2 parameters.
        splitline = line.split(' ', 2)
        found, index = data_match(splitline)
        if index != 1:  # swapping 2 and 3 index if the tag is present in 3 element
            splitline[1], splitline[2] = splitline[2], splitline[1]
        if len(splitline) > 2:
            if '@' in splitline[2]:
                splitline[2] = splitline[2].replace("@", "")
    return splitline

def extract_ind_date (instance, day, splitline):
    if day == 'BIRT':
        instance.birth_d = splitline[2]
    if day == 'DEAT':
        instance.death_d = splitline[2]

def extract_mar_date(instance, day, splitline):
    if day == 'MARR':
        instance.marriage_d = splitline[2]
    if day == 'DIV':
        instance.divorce_d = splitline[2]

def extract_individual_info(read_lines, line_no, individual):
    line_no +=1
    splitline = strip_valid_line(read_lines[line_no])
    while splitline[0] != "0" and line_no < len(read_lines):
        if splitline[1] == 'NAME':
            individual.name = splitline[2]

        if splitline[1] == 'SEX':
            individual.sex = splitline[2]

        if splitline[1] == 'BIRT' or splitline[1] == 'DEAT':
            extract_ind_date(individual, splitline[1], strip_valid_line(read_lines[line_no+1]))

        if splitline[1] == 'FAMC':
            individual.child_id = splitline[2]

        if splitline[1] == 'FAMS':
            individual.spouse_id = splitline[2]

        line_no +=1
        splitline = strip_valid_line(read_lines[line_no])
    individuals.append(individual)

def extract_family_info(read_lines, line_no, family):
    line_no +=1
    splitline = strip_valid_line(read_lines[line_no])
    while splitline[0] != "0" and line_no < len(read_lines):

        if splitline[1] == 'MARR' or splitline[1] == 'DIV':
            extract_mar_date(family, splitline[1], strip_valid_line(read_lines[line_no+1]))

        if splitline[1] == 'HUSB':
            family.hus_id = splitline[2]

        if splitline[1] == 'WIFE':
            family.wife_id = splitline[2]

        if splitline[1] == 'CHIL':
            family.children = splitline[2]

        line_no +=1
        splitline = strip_valid_line(read_lines[line_no])

    families.append(family)

def find_str(read_lines):
    """
    To extract the valve and update the variable value only if more than 2 parameters are there to check with the provided dict
    """
    line_no = 0
    while line_no < len(read_lines):
        splitline = strip_valid_line(read_lines[line_no])

        if splitline[0] == '0' and splitline[1] == 'INDI':
            extract_individual_info(read_lines, line_no, Individual(splitline[2]))

        if splitline[0] == '0' and splitline[1] == 'FAM':
            extract_family_info(read_lines, line_no, Family(splitline[2]))
        line_no += 1


    for ind in individuals:
        Ind.add_row([ind.ind_id, ind.name])
        ind_list.append((ind.ind_id, ind.name))
        read_dates.append(ind.birth_d)
        read_dates.append(ind.death_d)
    Ind.sortby = 'ID'

    print("Individual ID and Name \n", Ind)

    for f in families:
        f_id = f.fam_id
        read_dates.append(f.marriage_d)
        read_dates.append(f.divorce_d)

        hus_name = '' #default
        wif_name = '' #default
        for i in range(len(ind_list)):
            if ind_list[i][0] == f.hus_id:
                hus_name = ind_list[i][1]
            if ind_list[i][0] == f.wife_id:
                wif_name = ind_list[i][1]

        Fam.add_row([f_id, hus_name, wif_name])

    Fam.sortby = 'ID'

    print(" Family info \n", Fam)

    date_before(read_dates)


fname = input('Enter the file name: ')
try:
    fhand = open(fname)  # open File
    read_lines = fhand.readlines()
except:
    print('File cannot be opened:', fname)
    sys.exit()

sys.stdout = open('OutputFile.txt', 'w')


try:
    find_str(read_lines)
    fhand.close()  # Close the file
except:
    print('Processing failure')

try:
    gedcom_parser = Parser()
    gedcom_parser.parse_file(fname)
    elements = gedcom_parser.get_element_list()
    for element in elements:
        if isinstance(element, IndividualElement):
            error_text = validity_test.check_valid_individual(element)
            for error in error_text:
                print(error)
except Exception as exception:
    print(exception)

try:
    find_str(fhand)
    fhand.close()  # Close the file
except:
    print('Processing failure')


