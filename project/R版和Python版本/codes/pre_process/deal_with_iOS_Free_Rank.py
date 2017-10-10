#coding:utf-8
import numpy as np
import pandas as pd
from openpyxl import Workbook, load_workbook 

df_iOS_Rank = pd.read_csv('iOS_Free_Rank/iOS_Free_Rank.csv')
df_iOS_Rank.fillna(0, inplace=True)
#print list(df_iOS_Rank[:1].values[0])
#print list(df_iOS_Rank[1036:1037].values[0])

file_name = 'iOS_New_User'

df_iOS_Billing = pd.read_csv('iOS_Free_Rank/' + file_name + '.csv')
df_iOS_Billing.fillna('', inplace=True)
#print df_iOS_Billing[:10]

#df_game_billing = df_iOS_Billing[['Date', '《神仙道》高清重制版']]
#print df_iOS_Billing[df_iOS_Billing['Date']=='11/30/16']['《神仙道》高清重制版'].values[0]


wb = Workbook()
ws = wb.active
ws.title = file_name
ws.append([''] + range(1, 1501))

for d in df_iOS_Rank['Date'].values:
    # 初始化某天的排名列表
    list_rank_someday = []
    # 改正字符形式的排名值
    for v in list(df_iOS_Rank[df_iOS_Rank['Date']==d].values[0][1:]):
	try:
	    list_rank_someday.append(eval(v))
	except:
	    list_rank_someday.append(v)
    #print list_rank_someday
    # 将列表中的缺失值和nan用0代替
    list_revised_rank_someday = [0 if x == ' ' else int(x) for x in list_rank_someday]
    # 将游戏名与排名关连成字典形式
    dict_rank_someday = dict(zip(list_revised_rank_someday, list(df_iOS_Rank.columns[1:])))
    
    # 将字典中排名是0的记录删除
    #print dict_rank_someday.keys()
    if 0 in dict_rank_someday.keys():
	del dict_rank_someday[0]
    #print dict_rank_someday.keys()

    # 构造一个空白列表, 用上述排名位置替换成排名
    # 字典的键列表可能为空
    try:
	list_to_write = [d] + [''] * max(dict_rank_someday.keys())
    except:
	list_to_write = [d]
    #print list_to_write

    for k in dict_rank_someday.keys():
	#list_to_write[k] = dict_rank_someday[k]
	list_to_write[k] = df_iOS_Billing[df_iOS_Billing['Date']==d][dict_rank_someday[k]].values[0]
    #print list_to_write

    ws.append(list_to_write)

wb.save(file_name + '.xlsx')








