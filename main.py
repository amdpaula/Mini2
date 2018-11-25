import csp

class Input_Data():

    def __init__(self,fh):
        self.file = fh
        fh.seek(0,0)
        self.data = self.file.readlines()

    def Find_Line(self,char):
        for index,line in enumerate(self.data):
            test = line[0]
            if test == char:
                return index

    def Extract_Line(self,line_number):
        line = self.data[line_number]
        return line[2:-1]

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
        self.tuple = (self.day,self.hour)

    def Print_TimeSlot_Tuple(self):
        return self.tuple

    def Print_TimeSlot_Struct(self):
        self.string = self.day_string+','+str(self.hour)
        return self.string

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

    def Show_TimeSlots(self):
        for element in self.converted_timeslots:
            element.Print_TimeSlot_Tuple()

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

class Turmas_to_Attend():

    def __init__(self,course,All_Courses,All_Turmas):                  #THESE INPUT VARIABLES ARE THE LISTS OF ALL COURSES
        self.all_courses = All_Courses
        self.all_turmas = All_Turmas
        self.course = course                   #AND TURMAS
        self.turmas_set = set()

    def add_turma(self,turma):
        self.turmas_set.add(turma)



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

class Domain_Value():

    def __init__(self,day,hour,room):
        self.day = day      #string
        self.hour = hour    #int
        self.room = room    #string

    def Print(self):
        return self.day+str(self.hour)+self.room





class Problem(csp.CSP):

    def __init__(self, fh):
        
        data1 = TimeSlots(fh)
        class_days = data1.Get_Class_Days()
        time_slots = data1.Convert_TimeSlots()              #Returns a list of timeslot objects

        data2 = Rooms(fh)
        rooms = data2.Show_Rooms()

        data3 = Turmas(fh)
        turmas = data3.Show_Turmas()

        data4 = Courses(fh)

        self.class_names = data4.Get_Class_Names()
        self.class_types = data4.Get_Class_Types()
        converted_classes = data4.Convert_Classes()

        data5 = Associations(fh, self.class_names, turmas)
        self.associations = data5.Create_Association_List()

        '''We have chosen as variables strings that are composed of the concatenation of various information
         for each lecture (e.g. Var1 = 'IASD_T_1') and so can be easily converted again into structured data
         using the Lecture class (this is useful to improve readability in the constraints function'''

        variables = [element.Print_Lecture() for element in converted_classes]

        list_of_possible_values = []

        '''We have the same domain for every variable, and so, it is better to define our list of possible values first
        and then apply that domain for every variable'''

        for element in time_slots:
            for var in rooms:
                list_of_possible_values.append(Domain_Value(element.day_string, element.hour, var))

        '''We can utilize the class defined in the csp.py module as all our variables are going to have the same domain
        to create an universal dictionary'''

        domains = csp.UniversalDict(list_of_possible_values)

        '''The graph variable is a dictionary where each key is a CSP variable and the value associated with the key is
        a list of the other CSP variables that are involved in constraints with the key variable. When including all 
        possible rooms in the domain for a possible CSP variable assignment, one can infer that all variables are
        involved in constraints with other variables - any two lecture cannot occur at the same time in the same room.'''


        graph = {}

        for var in variables:
            graph[var] = []
            for element in variables:
                if element == var:
                    continue
                else:
                    graph[var].append(element)


        '''All previous work was done to simplify the following constraint function, and to improve its readibility as
        to make it easier to implement the constraints inherent in a schedule making problem.'''

        def constraints_function(A, a, B, b):  # Há necessidade de recursividade?
            aux = A.split('_')
            A = Lecture(aux[0], aux[1], aux[2],self.class_names,self.class_types)
            aux = B.split('_')
            B = Lecture(aux[0], aux[1], aux[2],self.class_names,self.class_types)

            for x in self.associations:
                if x.course == A.name:
                    Aa = x
                if x.course == B.name:
                    Bb = x

            if a.hour == b.hour and a.day == b.day:  # same room occupied at the same time
                return a.room != b.room
            if A.name == B.name and A.type == B.type:
                return b.day != a.day  # teóricas não podem ser no mesmo dia assim
            if a.day == b.day and a.hour == b.hour:
                return Aa.turma_set.intersection(Bb.turma_set) != Aa.turma_set  # CONFIRMAR ESTA PARTE    #different classes    MUDAR ESTA PARTE
            #raise Exception('error')
            return True





        super().__init__(variables, domains, graph, constraints_function)


    def dump_solution(self, fh):

        return True
        #TODO  Place here your code to write solution to opened file object fh

def solve(input_file, output_file):
    p = Problem(input_file)
    test = csp.backtracking_search(p)
    print(test)
    p.dump_solution(output_file)


fh = open('Input.txt','r')
ft = open('Output.txt','w')


solve(fh,ft)