import csv

with open('dates.csv', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
##    #next(csv_reader, None)
##    #data = list(csv_reader)
##    #for x in range(len(data[0])):
##    #    print(data[x][1])
##    #for row in csv_reader:
##    #    print(row['FirstName'])
    for row in csv_reader:
##        print(row['First Name'])
##        print(row['Last Name'])
##        print(row['Month'])
##        print(row['Day'])
##        print(row['Year'])
##        print(row['Occasion'])
##        print()
        bday_message = "Happy Birthday {} {}".format(row['First Name'], row['Last Name'])
        anniversary_message = "Happy Anniversary to Mr. and Mrs. {} {}".format(row['First Name'], row['Last Name'])
        passing_message = "We Honor the Passing of {} {}".format(row['First Name'], row['Last Name'])
        
        with open('test.txt', 'a') as f:
            f.write("{} - {} - {}".format(row['Month'], row['Day'], row['Year']))
            f.write('\n')
            if row['Occasion'] == 'Birthday':
                f.write(bday_message)
            elif row['Occasion'] == 'Anniversary':
                f.write(anniversary_message)
            elif row['Occasion'] == 'Passing':
                f.write(passing_message)
            f.write('\n')
            
