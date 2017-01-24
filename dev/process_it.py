import re

input_file = open('IT.txt','r')
output_file = file('IT.txt','a+')

for line in input_file:
     # output_file.write(re.findall(r'\d{6}',line)[0])
     # output_file.write('\n')
     output_file.writelines([item+' ' for item in line.split()[:3]])
     output_file.write('\n')

input_file.close()
output_file.close()