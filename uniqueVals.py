import pandas as pd
import time
from helperFunctions import clearTerminal, printElapsedTime

start = time.time()

clearTerminal()

print('Start')

df = pd.read_csv('train.csv')
# df = pd.read_csv('validation.csv')

columns = df.columns.values

print('*** TOTAL ROWS ***\n{}\n'.format(len(df)))
print('*** COLUMNS ***\n{}\n'.format(columns))
print('*** UNIQUE VALUES ***\n')

for column in columns:
    uniqueVals = sorted(list(set(df[column])))
    if len(uniqueVals) < 500:
        print('{}: {}\n'.format(column, uniqueVals))
    else:
        print('{}: {} unique values\n'.format(column, len(uniqueVals)))

end = time.time()
printElapsedTime(start, end)

print('Finish')
