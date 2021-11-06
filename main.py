import pandas as pd
from fuzzywuzzy import fuzz, process
import ast
from pathlib import Path
from datetime import datetime

# Generate unique datetime string for filename
def datetime_as_str():
    now = datetime.now() 
    return now.strftime("%Y%m%d%H%M%S%f")

# Checks if two strings are similar. Returns boolean
def is_same_attribute (attribute1, attribute2):
    return fuzz.token_sort_ratio(attribute1, attribute2) >= 65

# Takes in a list of copyright attributes, returns a list with duplicate attributes removed
def check_attributes (attribute_list):
    copy_attribute_list  = attribute_list.copy()
    for i in range(len(attribute_list)-1):
        for j in range(i+1,len(attribute_list)):
            if is_same_attribute(attribute_list[i],attribute_list[j]):
                if len(attribute_list[i])>len(attribute_list[j]):
                    try:
                        copy_attribute_list.remove(attribute_list[j])
                    except:
                        pass
                else:
                    try:
                        copy_attribute_list.remove(attribute_list[i])
                    except:
                        pass
                    
    return copy_attribute_list

# This is the path to your CSV file (Snyk Dependencies report)
csv_path = input("Provide the path to you Snyk 'Dependencies' report CSV file: ")
dependencies_df = pd.read_csv(csv_path)
dependencies_df = dependencies_df.loc[:,["id","copyright"]]

# Some of the rows have no copyright information (because dependencies are not licensed). This will filter those rows out
dependencies_attributes_list = list(filter(lambda row: row[1] != "[]", dependencies_df.values.tolist()))

#Create output folder
output_folder_name = "output"
Path(f'.\\{output_folder_name}').mkdir(parents=True, exist_ok=True)

#Create output file (Duplicate attributes removed)
output_filename = f'no-duplicate-attributes-{datetime_as_str()}.txt'
file = open(f'.\\{output_folder_name}\\{output_filename}',"w")
for dependency in dependencies_attributes_list:
    file.write(dependency[0] + "\n")
    attributes_no_duplicates = check_attributes(ast.literal_eval(dependency[1]))
    for attribute in attributes_no_duplicates:
        file.write(attribute + "\n")
    file.write("\n")
file.close()

#Create output file (Original list of sopyright attributions)
output_filename2 = f'all-attributes-{datetime_as_str()}.txt'
file2 = open(f'.\\{output_folder_name}\\{output_filename2}',"w")
for dependency in dependencies_attributes_list:
    file2.write(dependency[0] + "\n")
    attributes = ast.literal_eval(dependency[1])
    for attribute in attributes:
        file2.write(attribute + "\n")
    file2.write("\n")
file2.close()