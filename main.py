'''
IASD - Mini-Project 2 - Constraint Satisfaction Problems - November of 2018
Implemented by:
Group 20
Pedro Valdeira 81227
Guilherme Saraiva 81445
António Matos 81529
'''


import csp

'''The class below 'Input_Data' will not be instantiated, it is an abstract class, but that will allow the reading of the
filestream by other derived classes in a more modular way. '''

class Input_Data():

    def __init__(self,fh):
        self.file = fh
        fh.seek(0,0)
        self.data = self.file.readlines()

    def Find_Line(self,char):                       #Finds the line in the file which contains begins with 'char' character
        for index,line in enumerate(self.data):
            test = line[0]
            if test == char:
                return index

    def Extract_Line(self,line_number):             #Returns a single line of the file as a string, but having already removed
        line = self.data[line_number]               #the indicator character and the EOF character
        return line[2:-1]

'''Class 'TimeSlot' implements the objects which will hold the data pertaining to a certain time slot and so have an
attribute to hold the day of the week in which the timeslot is, and another attribute to save the hour in which the
timeslot is. The two methods implemented (besides __init__) are simple methods to set the attributes to the desired
values and retrieve the information as a string'''

class TimeSlot():

    def __init__(self,Week):
        self.day = -1
        self.day_string = ''
        self.hour = -1
        self.days_of_week = Week                            #All possible weekdays


    def Set_Day_Hour(self,day,hour):                        #Input variable 'day' is a string
        self.day = self.days_of_week.index(day)
        self.day_string = self.days_of_week[self.day]
        self.hour = int(hour)                               #Input variable 'hour' is a string

    def Print_TimeSlot_Struct(self):
        self.string = self.day_string+','+str(self.hour)
        return self.string

'''This next class 'TimeSlots' inherits from the class Input_Data to be able to read the timeslot line from the text file.
Its main purpose is to create a list of TimeSlot objects in order to more easily build the domain of the CSP problem.
This list is the attribute self.converted_timeslots. The method Get_Class_Days needs to run first before running
the method that actually builds the list of TimeSlot objects.'''

class TimeSlots(Input_Data):

    def __init__(self,fh):
        super().__init__(fh)
        self.line_number = self.Find_Line('T')
        self.line = self.Extract_Line(self.line_number)
        self.timeslots = self.line.split(' ')
        self.class_days = []
        self.converted_timeslots = []

    def Get_Class_Days(self):
        for element in self.timeslots:
            y = element.split(',')
            if y[0] in self.class_days:
                continue
            else:
                self.class_days.append(y[0])
        return self.class_days

    def Convert_TimeSlots(self):
        for element in self.timeslots:
            y = element.split(',')
            obj_time_slot = TimeSlot(self.class_days)
            obj_time_slot.Set_Day_Hour(y[0],y[1])
            self.converted_timeslots.append(obj_time_slot)      #LIST OF TIMESLOT OBJECTS
        return self.converted_timeslots

class Rooms(Input_Data):

    def __init__(self,fh):
        super().__init__(fh)
        self.line_number = self.Find_Line('R')
        self.line = self.Extract_Line(self.line_number)
        self.rooms = self.line.split(' ')

    def Show_Rooms(self):
        return self.rooms

class Turmas(Input_Data):

    def __init__(self,fh):
        super().__init__(fh)
        self.line_number = self.Find_Line('S')
        self.line = self.Extract_Line(self.line_number)
        self.turmas = self.line.split(' ')

    def Show_Turmas(self):
        return self.turmas

class Lecture():

    def __init__(self,name,type,count,All_Courses,All_Types):
        self.name = name
        self.courses = All_Courses
        self.type = type
        self.types = All_Types
        self.count = count
        self.strung = ''

    def Print_Lecture(self):
        self.tuple = (self.courses.index(self.name),self.types.index(self.type),self.count)
        self.strung = self.name+'_'+self.type+'_'+str(self.count)
        return self.strung


class Courses(Input_Data):

    def __init__(self,fh):
        super().__init__(fh)
        self.line_number = self.Find_Line('W')
        self.line = self.Extract_Line(self.line_number)
        self.class_names = []
        self.class_types = []
        self.converted_classes = []

    def Get_Class_Names(self):                              #THIS IS WORKING FINE
        classes = self.line.split(' ')
        for element in classes:
            y = element.split(',')
            if y[0] in self.class_names:
                continue
            else:
                self.class_names.append(y[0])
        return self.class_names

    def Get_Class_Types(self):                              #THIS IS WORKING FINE
        classes = self.line.split(' ')
        for element in classes:
            y = element.split(',')
            if y[1] in self.class_types:
                continue
            else:
                self.class_types.append(y[1])
        return self.class_types

    def Convert_Classes(self):
        classes = self.line.split(' ')
        for element in classes:
            y = element.split(',')
            obj_class = Lecture(y[0],y[1],int(y[2]),self.class_names,self.class_types)
            self.converted_classes.append(obj_class)
        return self.converted_classes                   #THIS IS A LIST OF LECTURE OBJECTS


'''This object is very important in the implementation of the constraints function. To implement the constraint that two
 lectures that a student class needs to attend cannot occur at the same time, we have to keep information about which courses are
 attended by which student classes. And so we implemented this object, where an attribute defines the course for which the
 object is referring to, and a set of student classes that need to attend the lectures of the given course.'''

class Turmas_to_Attend():

    def __init__(self,course,All_Courses,All_Turmas):                  #THESE INPUT VARIABLES ARE THE LISTS OF ALL COURSES AND ALL TURMAS
        self.all_courses = All_Courses
        self.all_turmas = All_Turmas
        self.course = course
        self.turmas_set = set()

    def add_turma(self,turma):
        self.turmas_set.add(turma)


'''Associations Class inherits from the 'Input_Data' class as to be able to also find and extract the desired line from 
the filestream that it receives when instantiated. Its main purpose is to build a list of objects of the class above
'Turmas_to_Attend' and have so a list that makes available in a structured form, a list of the student classes (turmas)
that need to attend a given course'''

class Associations(Input_Data):

    def __init__(self,fh,Courses,Turmas):
        super().__init__(fh)
        self.line_number = self.Find_Line('A')
        self.line = self.Extract_Line(self.line_number)
        self.associations = self.line.split(' ')
        self.all_courses = Courses
        self.all_turmas = Turmas
        self.list = []
        for element in self.all_courses:
            self.list.append(Turmas_to_Attend(element,Courses,Turmas))


    def Create_Association_List(self):              #TENHO LISTA DE TURMAS
        for element in self.associations:
            y = element.split(',')
            index_course = self.all_courses.index(y[1])
            course = y[0]
            self.list[index_course].add_turma(course)
        return self.list

'''This next class 'Domain_Value' was created in order to hold the data pertaining to the possible assignments for each
variable (the lecture to be placed in the schedule) and so must have an attribute for the day of the lecture, an attribute
for the hour at which the lecture occurs, and an attribute for the room where the lecture occurs. A simple 'Print' method
was implemented for testing and debugging purposes'''

class Domain_Value():

    def __init__(self,day,hour,room):
        self.day = day      #string
        self.hour = hour    #int
        self.room = room    #string

    def Print(self):
        return self.day+str(self.hour)+self.room


class Problem(csp.CSP):

    def __init__(self, fh, b = None):

        self.solution = dict()                              #Empty dictionary that will hold the solution to the CSP problem
        self.cost_of_solution = b
        List_of_TimeSlots = TimeSlots(fh)
        self.class_days = List_of_TimeSlots.Get_Class_Days()
        self.time_slots = List_of_TimeSlots.Convert_TimeSlots()              #Returns a list of timeslot objects

        List_of_Rooms_obj = Rooms(fh)
        self.rooms = List_of_Rooms_obj.Show_Rooms()

        List_of_Turmas_obj = Turmas(fh)
        turmas = List_of_Turmas_obj.Show_Turmas()

        List_of_Courses_objs = Courses(fh)

        self.class_names = List_of_Courses_objs.Get_Class_Names()
        self.class_types = List_of_Courses_objs.Get_Class_Types()
        converted_classes = List_of_Courses_objs.Convert_Classes()      #'converted_classes' is a list of Lecture objects

        List_of_Associations = Associations(fh, self.class_names, turmas)
        self.associations = List_of_Associations.Create_Association_List()

        '''We have chosen as variables strings that are composed of the concatenation of various information
         for each lecture (e.g. Var1 = 'IASD_T_1') and so can be easily converted again into structured data
         using the Lecture class (this is useful to improve readability in the constraints function)'''

        self.variables = [element.Print_Lecture() for element in converted_classes]

        self.list_of_possible_values = []

        '''We have the same domain for every variable, and so, it is better to define our list of possible values first
        and then apply that domain for every variable'''

        for element in self.time_slots:
            for var in self.rooms:
                self.list_of_possible_values.append(Domain_Value(element.day_string, element.hour, var))

        '''We can utilize the class defined in the csp.py module as all our variables are going to have the same domain
        to create an universal dictionary (maps all the keys to the same value, in this case the list above)'''

        self.domains = csp.UniversalDict(self.list_of_possible_values)

        '''The graph variable is a dictionary where each key is a CSP variable and the value associated with the key is
        a list of the other CSP variables that are involved in constraints with the key variable. When including all 
        possible rooms in the domain for a possible CSP variable assignment, one can infer that all variables are
        involved in constraints with all other variables as any two lectures cannot occur at the same time in the same room.'''


        self.graph = {}

        for var in self.variables:
            self.graph[var] = []
            for element in self.variables:
                if element == var:
                    continue
                else:
                    self.graph[var].append(element)


        '''All previous work was done to simplify the following constraint function, and to improve its readability as to
        make it easier to implement the constraints inherent in a schedule making problem.'''

        def constraints_function(Var1, a, Var2, b):
            aux = Var1.split('_')
            Var1 = Lecture(aux[0], aux[1], aux[2], self.class_names, self.class_types) #Place information in Lecture object
            aux = Var2.split('_')
            Var2 = Lecture(aux[0], aux[1], aux[2], self.class_names, self.class_types) #Place information in Lecture object

            for x in self.associations:

                if x.course == Var1.name:
                    Turmas_Var1 = x                                                     #An instance of the Turmas_to_attend object
                if x.course == Var2.name:
                    Turmas_Var2 = x                                                     #Another instance of the Turmas_to_attend_object but for the second CSP var

            if a.hour == b.hour and a.day == b.day and a.room == b.room:                #Cannot have the same room occupied at the same time
                return False
            if Var1.name == Var2.name and Var1.type == Var2.type and b.day == a.day:    #Cannot have the same type of class for a course repeated in a single day
                return False
            if a.day == b.day and a.hour == b.hour and (Turmas_Var1.turmas_set & Turmas_Var2.turmas_set != set()):
                return False  # CONFIRMAR ESTA PARTE    #different classes    MUDAR ESTA PARTE
            if self.cost_of_solution is None:               #Implementation without optimization
                return True
            else:
                if (a.hour or b.hour)>self.cost_of_solution:
                    return False
                else:
                    return True



        super().__init__(self.variables, self.domains, self.graph, constraints_function)


    def dump_solution(self, fh):

        fh.truncate(0)                      #Clean File
        fh.seek(0,0)                        #Place pointer in the beginning of the file

        for element in self.solution:       #The solution attribute of the problem object is a dictionary containing the assignment that satisfies the CSP
            aux = element
            aux = aux.replace('_',',')
            fh.write(aux+' ')
            fh.write(self.solution[element].day+',')
            fh.write(str(self.solution[element].hour)+' ')
            fh.write(self.solution[element].room+'\n')


def solve(input_file, output_file):
    p = Problem(input_file)
    p.solution = csp.backtracking_search(p) #if there is no solution p.solution=NoneType object.
                                            #If a solution exists, p.solution is a dictionary where the values, are domain objects.
    if p.solution is not None:              #Verification that solution is possible
        p.dump_solution(output_file)
    else:
        return print('No solution was found')

    #Optimization:
    latest_timeslot = max(p.solution[element].hour for element in p.solution)

    print(latest_timeslot)

    p.cost_of_solution = latest_timeslot

    while p.solution is not None:
        aux = p.solution
        b = p.cost_of_solution - 1
        p.cost_of_solution = b
        p.curr_domains = None
        p.nassigns = 0
        p.solution = csp.backtracking_search(p, select_unassigned_variable = csp.mrv, inference = csp.forward_checking)



        print(p.solution)

    p.solution = aux
    p.dump_solution(output_file)

fh = open('Input.txt','r') #For testing purposes
ft = open('Output.txt','w')
fo = open('Output_with_Optimization.txt','w')

solve(fh,ft)
