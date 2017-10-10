#coding:utf-8
import pandas as pd
import numpy as np
import calendar

working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/project/' +\
        '任意一天日活跃量或日新增量与日排名的趋势一致程度/'

# 输入'2017-06' 输出['2017-06-01', '2017-06-02', ..., '2017-06-30',]
def GetAllDaysOfOneMonth(curmonth):
    year, month = curmonth.split('-')
    days_curmonth = calendar.monthrange(int(year), int(month))[1]
    return [curmonth + '-0' + str(i) for i in range(1, 10)] +\
            [curmonth + '-' + str(i) for i in range(10, days_curmonth+1)]
#print GetAllDaysOfOneMonth('2017-06')


# 读取排名数据
df_rank = pd.read_excel(working_space + '4月份96款应用的日排名.xlsx', sheetname=0)
df_rank.fillna(0, inplace=True)
#print df_rank.columns
# 从Excel文件读取的时间格式是datetime.datetime的对象
# 需要将其转换为'2017-05-26'的格式, 与排名数据的时间格式一致
list_new_columns = list(df_rank.columns[:3])
for col in df_rank.columns[3:]:
    #print [col.strftime('%Y-%m-%d')]
    list_new_columns.append(col.strftime('%Y-%m-%d'))
#print list_new_columns
df_rank.columns = list_new_columns
#print df_rank.head()



# 选中某一天, 得到该天中排名与新增值环比一致的个数占总个数的比例
# 我们称之为该天新增值和排名间的趋势一致程度
#for day in ['2017-04-01', '2017-04-02',]:
for day in GetAllDaysOfOneMonth('2017-04'):
    path_newuser_ios_in_sandbox =\
            '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/' +\
            'daily_data_from_interface/' + day[:7] + '/'
    # 得到该天iOS平台所有应用的活跃量
    df_newuser_ios_oneday = pd.read_csv(path_newuser_ios_in_sandbox + day + '_newuser_iOS.txt')
    #print df_newuser_ios_oneday.head()
    # 得到该天待分析应用的畅销排名
    df_rank_oneday = df_rank[['ProductId', day]]
    #print df_rank_oneday.head()
    # 去掉排名为0即缺失的
    df_rank_oneday = df_rank_oneday[df_rank_oneday[day]!=0.0]
    #print df_rank_oneday.head()
    
    #87 print len(df_rank_oneday)
    list_rank = []
    list_newuser = []
    for pid in df_rank_oneday['ProductId']:
        rank = df_rank_oneday[df_rank_oneday['ProductId']==pid][day].values[0]
        # 排名有的APP可能在当天的新增量为0缺失
        try:
            newuser = df_newuser_ios_oneday[df_newuser_ios_oneday['productid']==pid]['newuser'].values[0]
        except Exception, e:
#            print 'missing productid: ', pid
            continue
        list_rank.append(rank)
        list_newuser.append(newuser)
    #print len(list_rank)
    #print len(list_newuser)
    
    list_momc_rank = []
    list_momc_newuser_ios = []
    for i in range(len(list_rank)-1):
        list_momc_rank.append(list_rank[i]/list_rank[i+1]-1)
        list_momc_newuser_ios.append(list_newuser[i+1]*1.0/list_newuser[i]-1)
    #print list_momc_rank
    #print list_momc_newuser_ios
    
    
    list_flag_momc = [i*j for i,j in zip(list_momc_rank, list_momc_newuser_ios)]
#    print list_flag_momc
    counts_pos = 0
    for i in list_flag_momc:
        if i > 0:
            counts_pos += 1
    print day, counts_pos, len(list_flag_momc), counts_pos*1.0/len(list_flag_momc)
    
    
    
