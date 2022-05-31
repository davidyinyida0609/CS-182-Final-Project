import json,os,time
from pathlib import Path


with open("abbreviation.json") as a:
        abbreviation = json.load(a)
with open("C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\data\\catalog\\courses_long.json") as c:
    raw1 = json.load(c)
courses1 = [each["abbreviation"]+" "+each["course_number"] for each in raw1["courses"]]
with open("C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\data\\catalog\\courses.json") as d:
    raw2 = json.load(d)
courses2 = [each["abbreviation"]+" "+each["course_number"] for each in raw2["courses"]]
courses = courses1+courses2

def flatten(lst):
    #a function that flatten the nested list into normal list
    flatten_lst = []
    for item in lst:
        if not type(item) == list:
            flatten_lst += [item]
        else:
            flatten_lst += flatten(item)
    return flatten_lst

def process(table):
    #flatten down all the indepdent courses in the given table
    flatten_table = flatten(table)
    result = []
    i = 0
    j = 0
    while (i <len(flatten_table)):
        current = flatten_table[i]
        if [[current]] == table[j]:
            result.append(current)
        else:
            flat = flatten(table[j])
            while ((i <len(flatten_table)) and (flatten_table[i] in flat)):
                i+=1
            result.append(table[j])
            i-= 1
        i+=1
        j+=1
        
    return result

def make_copy():
    #create copy of data
    directory = "C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\Data_process\\Data"
    path = "C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\Data_process\\Data"
    for filename in os.listdir(directory):
    #iterate through the folder
        if not ("Keys" in filename):
            with open(os.path.join(directory,filename)) as f:
                data = json.load(f)
            result = []
            for table in data:
                print(table)
                result.append(process(table))
            with open(os.path.join(path,filename),'w') as b:
                json.dump(result,b)

def test(path):
    #test whether keys and data files match
    for filename in os.listdir(path):
        with open(os.path.join(path,filename)) as a:
            data = json.load(a)
            if not ("Keys" in filename):
                counter = 0
                for each in data:
                    if type(each) is list:
                        counter += 1
                print(f"{filename} has a list of {counter}")
            else:   
                print(f"{filename} has a list of {len(data)}")
    


def show_info():
    #could change path to any major
    with open("Data\Environmental Earth Science\Environmental Earth Science.json") as a:
        data = json.load(a)
    with open("Data\Environmental Earth Science\Environmental Earth Science Keys.json") as b:
        keys = json.load(b)
    for each in data:
        if type(each) is str:
            #read each directly
            if "Consult" in each:
                print(f"{each} should be done with advisors")
            else:
                print(f"read {each} as a normal course")
        else:
        #that's being said it's a list type
            key = keys.pop(0)
            if type(key) is str:
                print(f"choose several courses from {each} up to {int(key)} units")
            elif type(key) is int:
                print(f"the number of courses that should be chosen from {each} is {key}")
            else:
                #that's being said the type of key is list type
                #and each is a nested list [[list1],[list2]]
                key = key[0]
                #remove the nested structure
                print(type(key) is int) #this should be True
                print(f"the number of list that should be chosen from {each} is {key}")
#show_info()
def test_all_major():
    #test the courses for all the majors existent in the abbreivaiton or course catalog
    path_global = "Data"
    for each in os.listdir(path_global):
        each_path = os.path.join(path_global,each)
        if Path(each_path).is_dir():
            Flag = False
            for jsn in os.listdir(each_path):
                if "Prerequisites" in jsn and "Prerequisites Keys" in jsn:
                    Flag = True
                    break
                if not("Keys" in jsn):
                    path = os.path.join(each_path, jsn)
                    with open(path) as b:
                        data = json.load(b)
                        data = flatten(data)
                    for each in data:
                        if ("consult" in each) or ("Consult" in each):
                            print(f"{each} needs to be consulted")
                        elif each in abbreviation:
                            print(f"{each} is a list of courses")
                        elif each in courses:
                            print(f"{each} is correct")
                        elif (each in "RA") or (each in "RB") or (each in "Freshman Seminar") or (each in "Ethics Requirement"):
                            print("reading and composition")
                        else:
                            raise NameError(f"In {jsn}, {each} is not found in catalog")
            if not Flag:
                raise StopIteration("Detect Prerequisites\Prerequisites Keys wrong spell in {each}")

def test_each_major(path):
    #test whether the courses for the given major all exist in the abbreviation or course catalog
    for jsn in os.listdir(path):
        if not("Keys" in jsn):
            file_path = os.path.join(path, jsn)
            with open(file_path) as b:
                data = json.load(b)
                data = flatten(data)
            for each in data:
                if ("consult" in each) or ("Consult" in each):
                    print(f"{each} needs to be consulted")
                elif each in abbreviation:
                    print(f"{each} is a list of courses")
                elif each in courses:
                    print(f"{each} is correct")
                elif (each in "RA") or (each in "RB") or (each in "Freshman Seminar") or (each in "Ethics Requirement"):
                    print("reading and composition")
                else:
                    raise NameError(f"In {jsn}, {each} is not found in catalog")


def get_abbreviation_data(abbreviation,major):
    path = f"C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\data\\courses\\{abbreviation}.json"
    with open(path) as f:
        data= json.load(f)
    courses = [each["abbreviation"]+" "+each["course_number"] for each in data["courses"]]
    with open(f"Data\{major}\data.json","w") as a:
        json.dump(courses, a)

#test("Data\\Urban Studies")
test_all_major()
#a = test_each_major("Data\\Urban Studies")
#get_abbreviation_data("SLAVIC", "Slavic Languages and Literatures")
