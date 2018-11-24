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

class Courses_to_Attend():

    def __init__(self,turma,Courses,All_Turmas):                  #THESE INPUT VARIABLES ARE THE LISTS OF ALL COURSES
        self.turma = turma
        self.all_courses = Courses
        self.turmas = All_Turmas                                           #AND TURMAS
        self.courses = []

    def add_Course(self,course):
        self.courses.append(course)

    def Transform_To_Tuple(self):
        self.tuple = (self.turmas.index(self.turma),[self.all_courses.index(element) for element in self.courses])


class Associations(Input_Data):

    def __init__(self,fh,Courses,Turmas):
        super().__init__(fh)
        self.line_number = self.Find_Line('A')
        self.line = self.Extract_Line(self.line_number)
        self.associations = self.line.split(' ')
        self.courses = Courses
        self.turmas = Turmas
        self.list = []
        for element in self.turmas:
            self.list.append(Courses_to_Attend(element,Courses,Turmas))


    def Create_Association_List(self):
        for element in self.associations:
            y = element.split(',')
            index_turma = self.turmas.index(y[0])
            course = y[1]
            self.list[index_turma].add_Course(course)
        return self.list

fh = open('Input.txt','r')

data1 = TimeSlots(fh)
class_days = data1.Get_Class_Days()
time_slots = data1.Convert_TimeSlots()

# print(class_days)                                 #THIS IS STILL WORKING FINE!
# for element in time_slots:
#     print(element.Print_TimeSlot_Struct())
#     print(element.Print_TimeSlot_Tuple())

data2 = Rooms(fh)
rooms = data2.Show_Rooms()

#print(rooms)                                       #THIS IS WORKING FINE!

data3 = Turmas(fh)
turmas = data3.Show_Turmas()

print(turmas)                                      #THIS IS WORKING FINE!

data4 = Courses(fh)
class_names = data4.Get_Class_Names()
class_types = data4.Get_Class_Types()
converted_classes = data4.Convert_Classes()

print(class_names)                                 #THIS IS WORKING FINE!
# print(class_types)

# for element in converted_classes:
#     print(element.Print_Lecture())

data5 = Associations(fh,class_names,turmas)
associations = data5.Create_Association_List()
print(associations)
