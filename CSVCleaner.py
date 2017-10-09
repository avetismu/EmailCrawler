import csv

emails = []

def Clean():
    print 'Cleaning CSV email mine'
    f_write = open('email_mine_clean.csv', 'w')
    with open('email_mine.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            entry =  str(row)[2:len(str(row))-3]
            if entry not in emails:
                emails.append(entry)
                f_write.write(entry + ',\n')
        f_write.close()
