import csv
import os

os.chdir("/home/ec2-user/environment/sample/")
data=[]
with open('urls.csv','rb') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

print(data)