#coding:utf-8
import os
import calendar
import pandas as pd

# 将每天的沙箱数(新增或者活跃量排名)纵向连接
# 根据ProductID或者某一应用的历史新增值或者活跃值

working_space = '/Users/Alas/Documents/TD_handover/sandbox_data_jupyter/'
path_dir_month = working_space + 'daily_data_from_interface/'
path_to_write = working_space + 'computed_daily_data/'

list_dir_month = os.listdir(path_dir_month)
# 根据'.'是否在列表项目中, 去除'.DS_Store', '*.zip'等
list_dir_month = [item for item in list_dir_month if '.' not in item]
#print list_dir_month

df_newuser_ios_allmonths = pd.DataFrame([], columns = ['date', 'productid', 'newuser',])
df_active_ios_allmonths = pd.DataFrame([], columns = ['date', 'productid', 'active',])
df_newuser_android_allmonths = pd.DataFrame([], columns = ['date', 'productid', 'newuser',])
df_active_android_allmonths = pd.DataFrame([], columns = ['date', 'productid', 'active',])

# 得到读入的月份列表范围内指定连接有限或全部月份的数据
for onemonth in list_dir_month[:1]:
#for onemonth in list_dir_month:
    #print onemonth
    list_dailyfile_onemonth = os.listdir(path_dir_month + onemonth)
    list_dailyfile_onemonth = [item for item in list_dailyfile_onemonth if '.DS' not in item]
    #print list_dailyfile_onemonth

    year, month = onemonth.split('-')
    days_onemonth = calendar.monthrange(int(year), int(month))[1]
    #print days_onemonth

    list_day = [onemonth + '-0' + str(i) for i in range(1, 10)] +\
            [onemonth + '-' + str(i) for i in range(10, days_onemonth+1)]
    #print list_day

    df_newuser_ios_alldays = pd.DataFrame([], columns = ['date', 'productid', 'newuser',])
    df_active_ios_alldays = pd.DataFrame([], columns = ['date', 'productid', 'active',])
    df_newuser_android_alldays = pd.DataFrame([], columns = ['date', 'productid', 'newuser',])
    df_active_android_alldays = pd.DataFrame([], columns = ['date', 'productid', 'active',])
    #print df_newuser_ios_alldays
    #print df_active_ios_alldays
    #print df_newuser_android_alldays
    #print df_newuser_android_alldays

    # 得到当前月份所有天日期的数据(2平台2维度数据)
    for day in list_day[:5]:
#    for day in list_day:
        #print day

        path_newuser_ios_oneday = path_dir_month + onemonth + '/' +\
                day + '_newuser_ios.txt'
        df_newuser_ios_oneday = pd.read_csv(path_newuser_ios_oneday)
        df_newuser_ios_oneday['date'] = pd.Series([day]*len(df_newuser_ios_oneday))
        df_newuser_ios_oneday = df_newuser_ios_oneday[[2, 0, 1,]]
        #print 'newuser_ios: \n', df_newuser_ios_oneday.head()
        #print len(df_newuser_ios_oneday['productid'])
        #df_t1 = df_newuser_ios_oneday['productid'].drop_duplicates()
        #print len(df_t1)
        # 将每天的iOS新增轴向连接到一起
        df_newuser_ios_alldays = pd.concat([df_newuser_ios_alldays, df_newuser_ios_oneday])

        path_active_ios_oneday = path_dir_month + onemonth + '/' +\
                day + '_active_ios.txt'
        df_active_ios_oneday = pd.read_csv(path_active_ios_oneday)
        df_active_ios_oneday['date'] = pd.Series([day]*len(df_active_ios_oneday))
        df_active_ios_oneday = df_active_ios_oneday[[2, 0, 1,]]
        #print 'active_ios: \n', df_active_ios_oneday.head()
        # 将每天的iOS活跃轴向连接到一起
        df_active_ios_alldays = pd.concat([df_active_ios_alldays, df_active_ios_oneday])

        path_newuser_android_oneday = path_dir_month + onemonth + '/' +\
                day + '_newuser_android.txt'
        df_newuser_android_oneday = pd.read_csv(path_newuser_android_oneday)
        df_newuser_android_oneday['date'] = pd.Series([day]*len(df_newuser_android_oneday))
        df_newuser_android_oneday = df_newuser_android_oneday[[2, 0, 1,]]
        #print 'newuser_android: \n', df_newuser_android_oneday.head()
        #print len(df_newuser_android_oneday['productid'])
        #df_t1 = df_newuser_android_oneday['productid'].drop_duplicates()
        #print len(df_t1)
        # 将每天的Android新增轴向连接到一起
        df_newuser_android_alldays = pd.concat([df_newuser_android_alldays, df_newuser_android_oneday])
        
        path_active_android_oneday = path_dir_month + onemonth + '/' +\
                day + '_active_android.txt'
        df_active_android_oneday = pd.read_csv(path_active_android_oneday)
        df_active_android_oneday['date'] = pd.Series([day]*len(df_active_android_oneday))
        df_active_android_oneday = df_active_android_oneday[[2, 0, 1,]]
        #print 'active_android: \n', df_active_android_oneday.head()
        # 将每天的android活跃轴向连接到一起
        df_active_android_alldays = pd.concat([df_active_android_alldays, df_active_android_oneday])

    df_newuser_ios_alldays.index = range(len(df_newuser_ios_alldays))
    df_active_ios_alldays.index = range(len(df_active_ios_alldays))
    df_newuser_android_alldays.index = range(len(df_newuser_android_alldays))
    df_active_android_alldays.index = range(len(df_active_android_alldays))
    #print df_newuser_ios_alldays
    #print df_active_ios_alldays
    #print df_newuser_android_alldays
    #print df_active_android_alldays

    # 得到了轴向链接指定月份所有天数据的DataFrame
    df_newuser_ios_allmonths = pd.concat([df_newuser_ios_allmonths, df_newuser_ios_alldays])
    df_active_ios_allmonths = pd.concat([df_active_ios_allmonths, df_active_ios_alldays])
    df_newuser_android_allmonths = pd.concat([df_newuser_android_allmonths, df_newuser_android_alldays])
    df_active_android_allmonths = pd.concat([df_active_android_allmonths, df_active_android_alldays])

# 重更新序号
df_newuser_ios_allmonths.index = range(len(df_newuser_ios_allmonths))
df_active_ios_allmonths.index = range(len(df_active_ios_allmonths))
df_newuser_android_allmonths.index = range(len(df_newuser_android_allmonths))
df_active_android_allmonths.index = range(len(df_active_android_allmonths))

#print "newuser_ios_allmonths"
#print df_newuser_ios_allmonths
#print "active_ios_allmonths"
#print df_active_ios_allmonths
#print "newuser_android_allmonths"
#print df_newuser_android_allmonths
#print "active_android_allmonths"
#print df_active_android_allmonths

# 按应用得到其历史上每一天的新增值
for onepid in df_newuser_ios_allmonths['productid'].unique():
    df_newuser_ios_onepid_allmonths =\
            df_newuser_ios_allmonths[df_newuser_ios_allmonths['productid']==onepid]
    df_active_ios_onepid_allmonths =\
            df_active_ios_allmonths[df_active_ios_allmonths['productid']==onepid]

    df_newuser_ios_onepid_allmonths.to_csv(path_to_write + 'newuser_ios/' +\
            str(int(onepid)) + '_newuser_ios.csv', index=None)
    df_active_ios_onepid_allmonths.to_csv(path_to_write + 'active_ios/' +\
            str(int(onepid)) + '_active_ios.csv', index=None)

# 按应用得到其历史上每一天的活跃量
for onepid in df_newuser_android_allmonths['productid'].unique():
    df_newuser_android_onepid_allmonths =\
            df_newuser_android_allmonths[df_newuser_android_allmonths['productid']==onepid]
    df_active_android_onepid_allmonths =\
            df_active_android_allmonths[df_active_android_allmonths['productid']==onepid]

    df_newuser_android_onepid_allmonths.to_csv(path_to_write + 'newuser_android/' +\
            str(int(onepid)) + '_newuser_android.csv', index=None)
    df_active_android_onepid_allmonths.to_csv(path_to_write + 'active_android/' +\
            str(int(onepid)) + '_active_android.csv', index=None)






