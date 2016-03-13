import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num

data = [(DT.datetime.strptime('2010-02-05', "%Y-%m-%d"), 123),
        (DT.datetime.strptime('2010-02-19', "%Y-%m-%d"), 678),
        (DT.datetime.strptime('2010-03-05', "%Y-%m-%d"), 987),
        (DT.datetime.strptime('2010-03-19', "%Y-%m-%d"), 345)]

x = [date2num(date) for (date, value) in data]
y = [value for (date, value) in data]

fig = plt.figure()

graph = fig.add_subplot(111)

# Plot the data as a red line with round markers
graph.plot(x,y,'r-o')

# Set the xtick locations to correspond to just the dates you entered.
graph.set_xticks(x)

# Set the xtick labels to correspond to just the dates you entered.
graph.set_xticklabels(
        [date.strftime("%Y-%m-%d") for (date, value) in data]
        )

plt.show()