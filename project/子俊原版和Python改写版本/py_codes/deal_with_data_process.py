#coding:utf-8
import pandas as pd
import math
import numpy as np

working_space = '/Users/Alas/Documents/TD/iOS_rank_estimate_model/ver_py/'
df_model_data = pd.read_csv(working_space + 'model_data.csv')
#print df_model_data.tail()

df_data_predict = pd.read_csv(working_space + 'data_process.csv', header=None)
df_data_predict.columns = ['Rank', 'New_User',]
#print df_data_predict.head()

# 向下取整应用在排名值一列
ss_rank_new = df_data_predict['Rank'].apply(math.floor)
#print ss_rank_new.head()
# 将取整后的排名值添加到DataFrame最后一列, 取名"Rank_New"
df_data_predict['Rank_New'] = ss_rank_new
#print df_data_predict.head()

# 通过对"Rank_New"去重筛选, 对排名值相同的多个New_User对应值取中位数, 舍弃其他构建新的DataFrame
dict_new_data_predict = []
for r in df_data_predict['Rank_New'].unique():
    df_onerank = df_data_predict[df_data_predict['Rank_New']==r]
    #print df_onerank
    dict_new_data_predict.append((int(r), np.median(df_onerank['New_User'])))
#print dict_new_data_predict
df_new_data_predict = pd.DataFrame(dict_new_data_predict, columns=['Rank', 'New_User',])
#print df_new_data_predict.head()
#print df_new_data_predict.tail()

# 得到经过上述进一步处理后的排名起始终止范围
head_rank = df_new_data_predict[:1]['Rank'].values[0]
tail_rank = df_new_data_predict[-1:]['Rank'].values[0]

# 范围以外的数据用处理异常值后的test_para补充
df_new_data_predict_before = df_model_data[['rank', 'test_para',]][df_model_data['rank']<head_rank]
df_new_data_predict_after = df_model_data[['rank', 'test_para',]][df_model_data['rank']>tail_rank]
df_new_data_predict_before.columns = df_new_data_predict.columns
df_new_data_predict_after.columns = df_new_data_predict.columns

# 将上述三部分轴向连接到一起
df_new_data_predict = pd.concat([df_new_data_predict_before, df_new_data_predict, df_new_data_predict_after])
#print df_new_data_predict

# 输出最终结果
df_new_data_predict.to_csv(working_space + 'final.csv', index=False)



