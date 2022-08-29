import os

class file_class:
    def read_file(self,file_path):
        with open(file_path) as file:
            file_lines = file.readlines()
        return file_lines

class log_class:
    def __init__(self):
        self.log = """"""

    def read_log(self,log_path):
        self.log = file_class().read_file(file_path = log_path)

    def display_log(self):
        for x in self.log:
            print(x)

class source_code_class:
    def __init__(self):
        self.source_code = dict()
    
    def read_source_code(self,source_path):
        # os.chdir(source_path)
        # for file_name in os.listdir():
        #     if '.' not in file_name:
        #         self.read_source_code(f"{source_path}\{file_name}")
        #     else:
        #         try:
        #             self.source_code[file_name] = file_class().read_file(f"{source_path}\{file_name}")
        #         except:
        #             print("\nError in Reading the File or File ignored ; Name :",file_name)
        os.chdir(source_path)
        for file_name in os.listdir():
            if '.' not in file_name:
                self.read_source_code(source_path = f"{source_path}\{file_name}")
            
            else:
                try:
                    self.source_code[file_name] = file_class().read_file(f"{source_path}\{file_name}")
                except:
                    print("\nError in Reading the File or File ignored ; Name :",file_name)
        
    def display_source_code(self):
        for key,value in self.source_code.items():
            print(key,value)