import pandas as pd
import csv

path='team ranking_2020_2023.csv'
df=pd.read_csv(path)
print(df)

lotte_df=df[df['팀명']=='한화']

print(lotte_df)

lotte_df.to_csv('lotte_team_rankings_2020_2023.csv', index=False)