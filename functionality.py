import re
import spacy
from collections import Counter
from string import punctuation
from polyfuzz import PolyFuzz

def parse_description(description):
    
    nlp = spacy.load("en_core_web_sm")
    def get_hotwords(text):
        result = []
        pos_tag = ['NOUN','ADV'] 
        doc = nlp(text.lower()) 
        for token in doc:
            if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
                continue
            if(token.pos_ in pos_tag):
                result.append(token.text)
        return result
    new_text = description
    output = set(get_hotwords(new_text))
    
    most_common_list = Counter(output).most_common(10)
    return [x[0] for x in most_common_list]

def process_desc(source_code,func_table,key_words,type = 'quick'):    

    keywords_list = key_words
    model = PolyFuzz("EditDistance")
    li = []
    for x in func_table.keys():
        li.extend(list(func_table[x].keys()))

    model.match(li,keywords_list)
    df = model.get_matches()
    from_list = df["From"].to_list()
    #print(from_list)
    df.drop('To',axis = 1,inplace = True)
    similarity_list = list(df.to_records(index = False))
    similarity_list.sort(reverse=True,key=lambda x: x[1])
    #print(similarity_list)

    
    if type == 'deep':
        result_list = []
        for key,val in source_code.items():
            for i in range(len(val)):
                for word in val[i].strip().split():
                    if any(re.search(r"\b" + re.escape(x) + r"\b", word) for x in from_list):
                        result_list.append((key,i+1))
        print(result_list)
    
    else:
        print(similarity_list)


class Function_table:
    function_table = dict()

    def display_func_table(self):
        for key,value in self.function_table.items():
            print(key,value)
            
class Python_module(Function_table):
    indent = 0
    def __init__(self):
        self.indent = 0
        
    def get_function_table_python(self,source_code_dict):
        
        for key,value in source_code_dict.items():
            source_code = value

            self.indent = 0
            func_stack = []
            function_table_temp = dict()

            for i in range(len(source_code)-1):
                if source_code[i].strip() == '':
                    continue

                if re.search(r"if[ ]*__name__[ ]*==[ ]*[\'\"]__main__[\'\"][ ]*:",source_code[i]) != None:
                    function_table_temp["main"] = [i+1,len(source_code)]

                if re.search("def .*(.*):",source_code[i]) != None:
                    line = re.split(r"[ /(]",source_code[i].strip())
                    func_name = line[1]
                    function_table_temp[func_name] = [i+1]
                    self.indent += 4
                    func_stack.append(func_name)
                
                    
                space = 0
                while(not source_code[i+1][space].isalnum()) and source_code[i+1].strip() != '':
                    space += 1
                

                if self.indent > space :
                    while self.indent != space and len(func_stack) != 0:
                        function_table_temp[func_stack.pop(-1)].append(i+1)
                        self.indent -= 4
            if func_stack:
                function_table_temp[func_stack.pop(-1)].append(i+1)

            Function_table.function_table[key] = function_table_temp
        return Function_table.function_table

    def parse_log_from_code_flow_python(self,Log,SourceCode):
        log = Log.log
        source_code = SourceCode.source_code
        func_table = Function_table.function_table
        
        code_flow = []
        file_flow = ["main.py"]

        driver_code_line = func_table["main.py"]["main"][0]
        end_line = func_table["main.py"]["main"][1]
        log_line = 0
        filename = "main.py"

        def check_function(filename,function_name,log_line,start_line,end_line):

            i = start_line
            file_flow.append(filename)

            while i < end_line and log_line<len(log):

                source_line = source_code[filename][i].strip()
                print_pattern = "print\([\"\']" + log[log_line].strip()+ "[\"\']\)"
                
                search_result = re.search(print_pattern,source_line)
                if search_result != None and log_line < len(log):
                    print(log_line+1,log[log_line].strip()," -> ",filename,function_name,i+1)
                    log_line += 1
        
                else:
                    if re.search("(^def )",source_line) != None:
                        f_name = source_line[4:source_line.index('(')]

                        i = func_table[filename][f_name][1]-1
                    else:
                        flag_search = 0
                        search_result = re.search(r"(\w+)\.(\w+)\([(\w+),=]*\)",source_line)
                        if search_result == None:
                            search_result = re.search("(\w+)\([(\w+),=]*\)",source_line)
                            flag_search = 1 
                        
                        if search_result != None:
                            if flag_search == 0:
                                filename = source_line[search_result.span()[0]:source_line.index(".")]+".py"
                                f_name = source_line[source_line.index(".")+1:source_line.index('(')]
                            else:    
                                f_name = source_line[:source_line.index('(')]
                            f_name = f_name.strip()
                            code_flow.append(f_name)

                            s_ind = func_table[filename][f_name][0]
                            e_ind = func_table[filename][f_name][1]

                            filename,log_line,f_name = check_function(filename,f_name,log_line,s_ind,e_ind)
                            
                i = i+1

            try:
                file_flow.pop(-1)
                filename = file_flow[-1]

            except:
                pass

            return filename,log_line,function_name
                    

        filename,log_line,function_name = check_function(filename,"main",log_line,driver_code_line,end_line)

class C_CPP_module(Function_table):
    paren_stack = [] #parentheses stack
    def __init__(self):
        self.paren_stack = list()
    
    def get_function_table_C_CPP(self,source_code_dict):
        main_flag = 0
        temp = 0
        for key,value in source_code_dict.items():
            source_code = value

            func_stack = []
            function_table_temp = dict()

            for i in range(len(source_code)-1):
                if source_code[i].strip() == '':
                    continue

                if re.search(r"(int|void)[ ]+main[ ]*\([\w+ ,=]*\)",source_code[i]) != None:
                    function_table_temp["main"] = [i+1]
                    main_flag = 1
                    func_stack.append("main")

                elif re.search(r"(int|void|char|float|double|bool|vector <\w+>)[ ]+\w*[ ]*\(.*\)",source_code[i]) != None:
                    line = re.split(r"[ /(]",source_code[i].strip())
                    func_name = line[1]
                    function_table_temp[func_name] = [i+1]
                    temp = len(self.paren_stack)
                    func_stack.append(func_name)
                    #print(func_stack)

                for x in source_code[i]:
                    if x == '{':
                        self.paren_stack.append("{")
                    if x == '}':
                        self.paren_stack.pop(-1)
                        if main_flag == 1 and len(self.paren_stack) == 0:
                            function_table_temp["main"].append(i+1)
                            main_flag = 0
                        elif(len(self.paren_stack) == temp):
                            function_table_temp[func_stack.pop(-1)].append(i+1)
                            temp = 0

            
            if func_stack:
                function_table_temp[func_stack.pop(-1)].append(i+1)
            

            Function_table.function_table[key] = function_table_temp
        return Function_table.function_table

    def parse_log_from_code_flow_CPP(self,Log,SourceCode):
        log = Log.log
        source_code = SourceCode.source_code
        func_table = Function_table.function_table
        
        code_flow = []
        file_flow = ["main.cpp"]

        driver_code_line = func_table["main.cpp"]["main"][0]
        end_line = func_table["main.cpp"]["main"][1]
        log_line = 0
        filename = "main.cpp"

        def check_function(filename,function_name,log_line,start_line,end_line):

            i = start_line
            file_flow.append(filename)

            while i < end_line and log_line<len(log):

                source_line = source_code[filename][i].strip()
                #print(source_line)
                print_pattern = "(cout|cerr) *<< *[\"\']*"+log[log_line].strip()+"[\"\']* *<< *endl *; *"
                
                search_result = re.search(print_pattern,source_line)
                if search_result != None and log_line < len(log):
                    print(log_line+1,log[log_line].strip()," -> ",filename,function_name,i+1)
                    log_line += 1
        
                else:
                    if re.search(r"(int|void|char|float|double|bool|vector <\w+>)[ ]+\w*[ ]*\(.*\)",source_line) != None:
                        if '<' in source_line:
                            temp = source_line.index('>') + 1
                        else:
                            temp = len(source_line.split()[0])
                        f_name = source_line[temp:source_line.index('(')].strip()

                        i = func_table[filename][f_name][1]-1
                    else:
                        flag_search = 0
                        search_result = re.search(r"(\w+) *\. *(\w+) *\([(\w+),= ]*\)",source_line)
                        if search_result == None:
                            search_result = re.search(r"(\w+)\([(\w+),=]*\)",source_line)
                            flag_search = 1 
                        
                        if search_result != None:
                            if flag_search == 0:
                                filename = source_line[search_result.span()[0]:source_line.index(".")]+".py"
                                f_name = source_line[source_line.index(".")+1:source_line.index('(')]
                            else:    
                                f_name = source_line[:source_line.index('(')]
                            f_name = f_name.strip()
                            code_flow.append(f_name)

                            s_ind = func_table[filename][f_name][0]
                            e_ind = func_table[filename][f_name][1]

                            filename,log_line,f_name = check_function(filename,f_name,log_line,s_ind,e_ind)
                            
                i = i+1

            try:
                file_flow.pop(-1)
                filename = file_flow[-1]

            except:
                pass

            return filename,log_line,function_name
                    

        filename,log_line,function_name = check_function(filename,"main",log_line,driver_code_line,end_line)


                