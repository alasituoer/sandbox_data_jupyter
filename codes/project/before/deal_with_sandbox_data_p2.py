#coding:utf-8
import pandas as pd

working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/project/model/'

path_file = working_space + 'df_sort_by_newuser_revised_alldays.xlsx'

df_alldays = pd.read_excel(path_file, header=None, names=['date', 'rank', 'newuser_ios',])
df_alldays.dropna(inplace=True)
df_alldays = df_alldays[1<=df_alldays['rank']]
df_alldays = df_alldays[df_alldays['rank']<=1500]
df_alldays.sort_values(by='rank', ascending=True, inplace=True)
print df_alldays.head()
print df_alldays.tail()

#df_alldays.to_excel(working_space + 're.xlsx', index=False)

"""
list_rank_unique = df_alldays['rank'].unique()
list_rank_unique.sort()
print len(list_rank_unique)
#print list_rank_unique

for r in list_rank_unique[:10]:
    print df_alldays[df_alldays['rank']==r]
"""

