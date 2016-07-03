import pandas as pd

data = {'names':['John Doe', 'Zoe McCarty', 'Pam Ferris'],
       'scores': [76, 98, 90]}
table = pd.DataFrame(data)

writer = pd.ExcelWriter('Scores.xls')
table.to_excel(writer, 'Scores 1')
writer.save()