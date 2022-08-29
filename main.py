def main(lang,input_type,source_code_path,input_path,search_type):
    from files import log_class,source_code_class,file_class
    from functionality import Python_module,C_CPP_module,Function_table
    from functionality import parse_description,process_desc
    
    SourceCode = source_code_class()
    SourceCode.read_source_code(source_path=source_code_path)
    SourceCode.display_source_code()

    if lang == 'python':
        processor = Python_module()
        processor.get_function_table_python(SourceCode.source_code)

    elif lang == 'cpp' or lang == 'c':
        processor = C_CPP_module()
        processor.get_function_table_C_CPP(SourceCode.source_code)

    else:
        print("Error occured process returned")
        return
    

    if input_type == "log":
        Log = log_class()
        Log.read_log(log_path=input_path)
        processor.parse_log_from_code_flow_python(Log,SourceCode)

    elif input_type == "desc":
        desc = file_class().read_file(file_path=input_path)
        desc = " ".join(line.strip() for line in desc)
        print(desc)
        keywords = parse_description(desc)
        process_desc(SourceCode.source_code,Function_table.function_table,keywords,type = search_type)

        


main(lang = "cpp",input_type = "desc", source_code_path = r"C:\Users\pskir\OneDrive\Desktop\Samsung prism\source_codes\description_test\source_code",input_path = r"C:\Users\pskir\OneDrive\Desktop\Samsung prism\source_codes\description_test\desc.txt",search_type = 'deep')






# from files import log_class,source_code_class
# from functionality import *



# log_path_cpp = r"C:\Users\pskir\OneDrive\Desktop\Samsung prism\log_files\log_cpp.txt"
# log_path_python = r"C:\Users\pskir\OneDrive\Desktop\Samsung prism\log_files\log_python.txt"
# source_code_path_python = r"C:\Users\pskir\OneDrive\Desktop\Samsung prism\source_codes\python"
# source_code_path_cpp = r"C:\Users\pskir\OneDrive\Desktop\Samsung prism\source_codes\cpp"
# source_code_path_desc = r"C:\Users\pskir\OneDrive\Desktop\Samsung prism\source_codes\description_test"

# Log = log_class()
# Log.read_log(log_path=log_path_python)
# #Log.display_log()

# SourceCode = source_code_class()
# SourceCode.read_source_code(source_path=source_code_path_python)
# #SourceCode.display_source_code()

# # SourceCode_desc_test = source_code_class()
# # SourceCode_desc_test.read_source_code(source_path=source_code_path_desc)
# #SourceCode_desc_test.display_source_code()

# processor_python = Python_module()
# # processor_CPP = C_CPP_module()

# # processor_CPP.get_function_table_C_CPP(SourceCode_desc_test.source_code) 
# # processor_CPP.display_func_table()
# # processor_CPP.parse_log_from_code_flow_CPP(Log,SourceCode)

# processor_python.get_function_table_python(SourceCode.source_code)
# processor_python.display_func_table()
# processor_python.parse_log_from_code_flow_python(Log,SourceCode)



# # description = "The application breaks down after trying to open camera"
# # keywords = parse_description(description)
# #print(keywords)

# #process_desc(SourceCode_desc_test.source_code,Function_table.function_table,keywords,type = 'deep')
