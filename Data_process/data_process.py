import json
import os,copy
path = "C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\Data_process\\data.json"
# Note!! The path might need to be changed
with open(path) as f:
    data = json.load(f)
keys = list(data.keys())
values = list(data.values())

def read_data():
    # iterate through the data.json
    for i in range(len(keys)):
        major_info = values[i]
        major_name = keys[i]
        print(f"The required courses for major {major_name} are shown as following:")
        for j in range(len(major_info)):
            table = major_info[j]
            print(f"Table{j} is shown as following:")
            for row in table:
                print(row)

def save_by_major():
    #convert a large data.json file into a list of json files divided by major
    for i in range(len(keys)):
        key = keys[i]
        key = key.replace("/","")
        key = key.replace(":","")
        key = key.replace("  "," ")
        value = values[i]
        path = f"C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\Data_process\\Data\{str(key)}.json"
        with open(path,'w') as f:
            json.dump(value,f)

def get_abbreviation():
    #save all the courses abbreviations from catalog and also return the list
    path = "C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\data\\catalog\\courses_long.json"
    with open(path) as f:
        data = json.load(f)
    values = list(data.values())[0]
    abbreviation = []
    for value in values:
        abbre = value.get("abbreviation")
        if not (abbre in abbreviation): 
            abbreviation.append(abbre)
    with open("C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\Data_process\\abbreviation.json","w") as f:
        json.dump(abbreviation,f)
    return abbreviation

def load_abbreviation():
    #load the abbreviaiton lists in the data
    with open("C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\Data_process\\abbreviation.json") as f:
        data = json.load(f)
    return data

abbre_list = load_abbreviation()
#static list of abbreviations

def seperate_contents():
    directory = "C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\Data_process\\Data"
    for filename in os.listdir(directory):
    #iterate through the folder
        with open(os.path.join(directory,filename)) as f:
            data = json.load(f)
        courses = [[] for i in range(len(data))]
        keys = copy.deepcopy(courses)
        for j in range(len(data)):
        #iterate through each table
            table = data[j]
            cou_table = courses[j]
            keys_table = keys[j]
            for k in range(len(table)):
                if isinstance(table[k],list):
                #check whether the row is coursecomment or list type(course inside)
                    cou_table.append(table[k])
                else:
                    keys_table.append(table[k])
        course_name = filename
        key_name = filename.replace(".json"," Keys.json")
        p = "C:\\Users\\david\\OneDrive\\Documents\\GitHub\\calcourses\\Data_process\\Data2"
        helper = lambda x: x
        courses = list(filter(helper,courses))
        keys = list(filter(helper,keys))
        with open(os.path.join(p,course_name),"w") as x:      
            json.dump(courses,x)
        with open(os.path.join(p,key_name),"w") as y: 
            json.dump(keys,y)



