# import re
# ss = "hi"
# s = "func (v);"
# s1 = "int function_name_1(int *a)"
# p1 = "(cout|cerr) *<< *[\"\']*"+ss+"[\"\']* *<< *endl *; *"
# #print(re.search(p1,s))
# p2 = r"\w *((<?\w+>?)?|\w) *\([\w ,=]*\)"
# p3 = r"(\w+) *\([(\w+),= ]*\)"
# #print(re.split(r"[ /(]",s1))
# print(re.search(p3,s))
import os

def read_file(file_path):
    with open(file_path) as file:
        file_lines = file.readlines()
    return file_lines

source_path = r"C:\Users\pskir\OneDrive\Desktop\Samsung prism\source_codes\description_test"
source_code = dict()
def read_source_code(source_code,source_path):
    os.chdir(source_path)
    for file_name in os.listdir():
        if '.' not in file_name:
            read_source_code(source_code,source_path = f"{source_path}\{file_name}")
        
        else:
            try:
                source_code[file_name] = read_file(f"{source_path}\{file_name}")
            except:
                print("\nError in Reading the File or File ignored ; Name :",file_name)
    

read_source_code(source_code=source_code,source_path=source_path)
for x in source_code.keys():
    print(x,source_code[x])