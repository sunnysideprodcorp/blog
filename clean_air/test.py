from pandas import DataFrame, read_csv

nums = [[i, i+1] for i in range(20)]
letters = 'a-z'[:20]

df = DataFrame({'nums' : nums, 'letters' : letters})
print(df)

print df.iloc[2][1][1]
print type(df.iloc[2][1])
