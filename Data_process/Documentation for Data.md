Now, I have finished all the majors. Their required courses information is saved by each major in each directory. Please use them to test algorithm and generate schedule.

Mostly, there are four files in each folder whose name is the major name.

Directory:
  Pair:
  
  Most of directories only have two pairs of data. That is "Major.json" + "Major Prerequisites.json" and "Major Prerequisites.json" + "Major Prerequisites Keys.json". 

  Concentration:

  However, some majors may have concentration so we break "Major.json" + "Major Prerequisites.json" into "Major A Concentration.json" + "Major A Concentration Keys.json", "Major B Concentration.json" + "Major B Concentration Keys.json", and so on.
  
  Track:

  Again, some majors may have multiple sub concentration so we break each concentration. Let's say "Major A Concentration.json" + "Major A Concentration Keys.json" have two sub groups "Track 1" and " Track 2". We break that it again into "Major A Concentration Track 1.json" + "Major A Concentration Track 1 Keys.json" and "Major A Concentration Track 2.json" + "Major A Concentration Track 2 Keys.json". Note this is pretty rare case. If I remember correctly, there are only one major that has this kind of complicated tree strucutres.


After knowing the relationship of files in each directory, we need then check the type of each element by iterating thorugh each json file.

Element in json files:

  If each is a string, it represents a course, a class of course, or comment. 
  
  Course:

    A course is formatted as Abbrieviation+Course Number, such as "MATH 54". 

  A Class of Course:

    However, a class of course is a course that only has abbrieviaiton, doesn't have speicific Course Number, such as "COMPSCI". That simply means any upper division course whose course number starts at 100 and ends at 190. In other words, if you see "COMPSCI" in a list, it means you can satisfy that requriment by taking "COMPSCI 189", "COMPSCI 188", or "COMPSCI 186." In addition to usual abbrieviation, we also have "RA", "RB", "Ethics Requirement", and "Freshman Seminar", meaning Reading and Composition Part A, Reading and Composition Part B, Ethics Requirement, and Freshman Seminar, respectively. These could be treated simliarly to "COMPSCI".

  Comment:

  Lastly, we have comment, which is a list starting with "Consult." Although these information might be useless when we generate the four year plan, we still need to inform students that the schedule they receive is not exactly valid to obtain a degree. Some "Consultation" needs to be done. 

  Anway regardless of the type of each string, you can use it as a required one.
  For example, data = [COMPSCI 61A, COMPSCI 61B, COMPSCI 61C]. Each in data is a string and should be used as a required course.

  List:
  
  If each is a list, it represents a list of courses that you can choose. 
  The corresponding key in the key. json specifies how to use that list as following:

    Key:
     
      If key is a string, then you can choose several courses from each up to "keys" units.
  
      E.g.Suppose we have data = [MATH 53, [MATH 54, EECS 16A], MATH 55] and keys = ["4"]. Our first data is MATH 53, which is a required one. The second data is a list. This is the first list we encounter, so we look into the first corresponding key,keys[0] in the key files, that is "4";. It is a string, so we know that we can choose MATH 54 or EECS 16A because either counts as a 4-unit course.
    
      If key is an int, then you can choose int numbers of courses from each.
  
      E.g.Again, we have data = [MATH 53, [MATH 54, EECS 16A], MATH 55] and keys = [1]. Our first data is MATH 53, which is a required one. The second data is a list. This is the first list we encounter, so we look into the first corresponding key,keys[0], in the key files, that is 1. It is an int type, so we know that we can choose MATH 54 or EECS 16A because either counts as one number.
    
      If key is a list, then key[0] must be int type. In this situation, each should be a nested list, like [[list1],[list2], course3, course 4]. So you can choose key[0] cluster(s) from each. 
  
      E.g. if we have data = [MATH 53, [MATH 54, [EECS 16A, EECS16B], PHYSICS 89]] and keys = [[1]]. The first we encounter is a string, no need to worry. The second element of data is a list and we look to correpsonding key value. Our keys[0] is also a list. So, We just need to go into keys. Since key = keys[0]=[1], our key[0] is 1, meaning that we need to choose 1 cluster from each. We can either choose MATH 54, [EECS 16A, EECS 16B], or PHYSICS 89.

To better get an idea of what I mean, you can run the method show_info in the process.py under Data_Process. It will print out all the information structure correctly.

Note you need open one data file and its corresponding keys file as a and b respectively. Path might change.
