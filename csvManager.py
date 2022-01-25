import csv

def getHeader():
    file = open('SS_100lines.csv')
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    file.close()
    return header

def getValueByHead(head):
    with open('SS_100lines.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        i = 0
        for row in reader:
            data.append(row[head])
            i+=1
            #if i == 3: break
    return data
