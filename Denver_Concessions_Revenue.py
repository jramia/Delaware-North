from tabula import convert_into
import csv
import sys

year, month, filename = sys.argv[1:]

url = f'https://www.flydenver.com/sites/default/files/downloads/{filename}'
out = f'Concessions_Revenue_{year}_{month}.csv'

convert_into(url,
             out,
             output_format="csv",
             pages='all',
             lattice=True)

with open(out, 'r') as readFile:
    data = list(csv.reader(readFile))

newdata = []
for row in data:
    row = [string.replace('\n',' ') for string in row]
    if len(row) > 1:
        if row[1] != '' and row[0] == '':
            row = row[1:]
        newdata.append(row)

with open(out, 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(newdata)