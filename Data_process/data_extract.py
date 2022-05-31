from bs4.element import NavigableString
import requests
from bs4 import BeautifulSoup
from functools import lru_cache
import time
import unicodedata
import json

from requests.api import get

memoize = lru_cache(None)

degree_url='http://guide.berkeley.edu/undergraduate/degree-programs/' # degree_programs website
degree_response = requests.get(degree_url)
degree_soup = BeautifulSoup(degree_response.text, 'html.parser') # all information about the website in the format of html
dict_degree_pair = {"major":"filter_6","minor":"filter_7","simultaneous":"filter_69"}
# three filters of checkboxes for three types of degress

@memoize
def get_programs_list(degree_type):
    # a function that returns a list of program names in String if degree_type in the keys of dict, otherwise print it doesn't exist
    if degree_type in dict_degree_pair.keys():
        degree_tag = dict_degree_pair[degree_type]
        # get the filter tag
        degree_divison = degree_soup.findAll("li",class_=degree_tag)
        # find all classes containing the tag
        program_list = [each.a.span.string for each in degree_divison]
        # create a list whose element is the name of each program
        program_url_list = [degree_url+each.a.get("href") for each in degree_divison]
        # create a list whose element is the url of each program
        return {program_list[i]:program_url_list[i] for i in range(len(program_list))}
        #create a one-to one dict represents the name of the program to its url
    else:
        print(degree_type+" doesn't exists in", dict_degree_pair.keys())
        # print it doesn't exist

major_dict = get_programs_list("major") ### length is 113
major_names_list = list(major_dict.keys()) ###convert the key of major dict to list
minor_dict = get_programs_list("minor")### length is 108
simultaneous_dict = get_programs_list("simultaneous")### length is 7

def remove_repeats(info_list):
    # a function that removes the repeated element for a given list
    res = []
    for i in info_list:
        if i not in res:
            res.append(i)
    return res

def major_requirement(major):
    # a function that returns a list of soup object correpsonding to each major
    # NOTE!!! The list of Chemistry soups has two elements: one is bachelor of science degree and the other is bachelor of art degree
    # for non-major paths but in major_name_list, this function returns [None] for them
    major_url = major_dict[major]
    major_response = requests.get(major_url)
    major_soup = BeautifulSoup(major_response.text,"html.parser")
    id_tag = ["majorrequirementstextcontainer","majorrequirementsbsdegreetextcontainer",
    "majorrequirementsbadegreetextcontainer","majorrequirementsbstextcontainer"]
    non_major_list = ["Pre-Med / Pre-Health","Prelaw Information","East European/Eurasian Languages and/or Cultures"]
    if major == "Global Studies":
        return [major_soup.find("div",id="newitemtextcontainer")]
    elif major in non_major_list:
        return [None]
    else:
        result = []
        for each in id_tag:
            contents = major_soup.find("div",id=each)
            if contents:
                result.append(contents)
        return result

def url_test(url):
    # a functions to test the connection given a url
    contents = requests.get(url)
    # if connected successfully, it should return code 200
    return contents


def create_divsion(soup):
    # a function that takes a soup of certain major and returns a list of tables
    # NOTE!!! Therefore, if major = Chemistry, it will return a nested list which contains two lists of table
    if len(soup)>1:
        return [create_divsion([each]) for each in soup]
    elif len(soup) ==1 and soup == None:
        return [None]
    elif len(soup) ==1:
        info = soup[0]
        table_list = info.find_all("table",class_="sc_courselist")
        # sort all the table into a list
        return table_list

def all_courses(x):
    # a function that takes in several tables for a specific major and returns a list of courses
    if type(x) != list:
        contents = x.find_all("a")
        courses = [each.next_element.string for each in contents]
        return courses

def row_sort(row):
    # a function that takes in a row and returns a list of courses it contains
    contents = row.find_all("a")
    courses = [each.next_element for each in contents]
    formatted_courses = [unicodedata.normalize("NFKD", course) for course in courses]
    return formatted_courses

@memoize
def process_table(x):
    # a function that takes in a table and returns all courses in it
    row_list = list(iter(x.find_all("tr")))
    # format the table into a list of rows
    result = []
    i = 0
    while(i<len(row_list)):
        # iterate over the rows
        division = []
        # create a list container for the courses or alternatives in the current row
        row_i = row_list[i]
        # get the current row
        attr_i = row_i["class"]
        #get the attribute of current row
        if row_i.td and row_i.td.find("a"):
        # check whether it contains "td" and a under "td" tag
        # NOTE!!! This is used to check whether this row is a row of courses
            courses_i = row_sort(row_i)
            # get the courses in the current row
            division.append(courses_i)
            # append it to the list for the current row
            if "even" in attr_i:
            # check which attribute it contains, even or odd 
                attr = "even"
            else:
                attr = "odd"
            for j in range(i+1,len(row_list)):
                # Note!!! iterate over the rest of the rows to get alternatives
                row_j = row_list[j]
                tag_j = row_j["class"]
                if attr in tag_j and "orclass" in tag_j:
                # check whether the given attr is in the new row and whether this row is an alternative-course row
                    courses_j  = row_sort(row_j)
                    #get the courses in the new row
                    division.append(courses_j)
                    #append it to the list as alternative courses
                else:
                # that is being said that it's not an alternative-course row
                # therefore, examine this new row as the current row
                    i = j-1
                    # note we add 1 to i in the outer loop
                    break
                    # quit the alternatives check
            result.append(division)
            # append the list of courses and their alternatives into the list        
        elif row_i.td and row_i.td.find("span"):
        # check whether it is courselistcomment row
            contents = row_i.td.span.next_element
            # get the information
            result.append(contents)
            # append to the list
        i += 1
    return result

def get_all():
    courses_dict = {}
    ###test each major soup whether it contains proper information and return the dict with all the information
    for each in major_names_list:
        print("The required courses for",each,"major is shown a following")
        if not (None in major_requirement(each)):
            tables_lists = create_divsion(major_requirement(each))
            lst = []
            if each == "Chemistry":
                for tables in tables_lists:
                    inner_lst = []
                    for table in tables:
                        courses = process_table(table)
                        inner_lst.append(courses)
                        for course in courses:
                            print(course)
                    lst.append(inner_lst)
                courses_dict["Chemistry BS"] = lst[0]
                courses_dict["Chemistry BA"] = lst[1]
                        
            else: 
                for table in tables_lists:
                    courses = process_table(table)
                    lst.append(courses)
                    for course in courses:
                        print(course)
                courses_dict[each] = lst
    return courses_dict

def extract_data():
    # get all the data and save as data.json
    courses_dict = get_all()
    with open('data.json', 'w') as fp:
        json.dump(courses_dict, fp)
    
extract_data()