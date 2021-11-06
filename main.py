import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import ast
from pathlib import Path
from datetime import datetime

def datetime_as_str():
    now = datetime.now() 
    return now.strftime("%Y%m%d%H%M%S%f")

def is_same_attribute (attribute1, attribute2):
    return fuzz.token_sort_ratio(attribute1, attribute2) >= 65

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

csv_path = "C:\\Users\\Bryan\\Downloads\\dependencies-scvjuniorbanking-2021-11-06T02_55_18.126Z.csv"
dependencies_df = pd.read_csv(csv_path)
dependencies_df = dependencies_df.loc[:,["id","copyright"]]
dependencies_attributes_list = list(filter(lambda row: row[1] != "[]", dependencies_df.values.tolist()))


Path(".\\output").mkdir(parents=True, exist_ok=True)

output_filename = "no-duplicate-attributes" + datetime_as_str() + ".txt"
file = open(".\\output\\" + output_filename,"w")
for dependency in dependencies_attributes_list:
    file.write(dependency[0] + "\n")
    attributes_no_duplicates = check_attributes(ast.literal_eval(dependency[1]))
    for attribute in attributes_no_duplicates:
        file.write(attribute + "\n")
    file.write("\n")
file.close()

output_filename2 = "all-attributes" + datetime_as_str() + ".txt"
file2 = open(".\\output\\"  + output_filename2,"w")
for dependency in dependencies_attributes_list:
    file2.write(dependency[0] + "\n")
    attributes = ast.literal_eval(dependency[1])
    for attribute in attributes:
        file2.write(attribute + "\n")
    file2.write("\n")
file2.close()