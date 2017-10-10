#coding:utf-8
import pandas as pd
import matplotlib.pyplot as plt

working_space = '/Users/Alas/Documents/TD/iOS_rank_estimate_model/estimate_project/new_user_cat_apps_ios_free_rank/source_file/'

df_rank_newuser = pd.read_csv(working_space + 'new_user_rank_from_model.csv')
print df_rank_newuser.head()

list_rank = list(df_rank_newuser['rank_total'].values)
list_data = list(df_rank_newuser['predict_vector'].values)
print list_rank[:10]
print list_data[:10]

plt.plot(list_rank[:100], list_data[:100], label='model_from_zijun')
plt.show()
