import pandas as pd

df = pd.read_excel("../data/07-01result.xls")
stock = df['positive'].tolist()
print stock