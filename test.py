import csv
data = []
rate = [] 
with open('config.csv') as File:  
    reader = csv.reader(File, delimiter=',')
    next(reader, None)
    for row in reader:
        data = row[0]
        rate = row[1]


print (data)
print (rate)

