def creating_test_file(name_of_file):

    days_of_week = []
    having_input = 1

    while(having_input == 1):
        day_of_week = input('When finished write END \nName of the day of the week with class:')
        if day_of_week == 'END':
            having_input = 0
        days_of_week.append(day_of_week)

    valid_hours = []
    having_input = 1

    while(having_input == 1):
        time_slot = input('When finished write END \nTimeslot that can have a class:')
        if time_slot == 'END':
            having_input = 0
        valid_hours.append(time_slot)



    fh = open(name_of_file,'w')
    fh.write('')



