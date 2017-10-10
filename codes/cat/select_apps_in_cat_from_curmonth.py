#coding:utf-8
import pandas as pd
import calendar

# 读入某一个月的active_ios and active_android 两个文件
# 通过查找中文名得到属于CAT iOS and Android 两个平台的应用(活跃量)数据
working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/get_daily_data_from_interface/'


# 读入iOS与Android的productid对照表
path_lookup_table = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/lookup_table_from_dawei/'
# Input the lookup table of Productid and Chinese Name defined by the developer
df_prod_info = pd.read_csv(path_lookup_table + 'product_basic_info_revised.txt')
df_prod_info.columns =\
        ['Product Id', 'Product Name', 'Product Type', 'Platform Id',]
#print df_prod_info.head()

# 将对照表分为Android平台
df_product_info_android = df_prod_info[df_prod_info['Platform Id']==1]
df_lookup_table_android = df_prod_info_android[['Product Id', 'Product Name',]]
df_lookup_table_android.index = df_lookup_table_android['Product Id']
del df_lookup_table_android['Product Id']
#print df_lookup_table_android.head()
# 和iOS平台的
df_product_info_ios = df_prod_info[df_prod_info['Platform Id']==2]
df_lookup_table_ios = df_prod_info_ios[['Product Id', 'Product Name',]]
df_lookup_table_ios.index = df_lookup_table_ios['Product Id']
del df_lookup_table_ios['Product Id']
#print df_lookup_table_ios.head()


curmonth = '2017-04'
year, month = [int(i) for i in curmonth.split('-')]
days_curmonth = calendar.monthrange(year, month)[1]
list_day = [curmonth + '-0' + str(i) for i in range(1, 10)] +\
        [curmonth + '-' + str(i) for i in range(10, days_curmonth+1)]
#print list_day
path_to_write_all_curmonth_ios = 


for day in list_day:
    #df_newuser_ios = pd.read_csv(working_space + day + '_newuser_iOS.txt')
    df_active_ios = pd.read_csv(working_space + day + '_active_iOS.txt')
    #df_newuser_android = pd.read_csv(working_space + day + '_newuser_android.txt')
    df_active_android = pd.read_csv(working_space + day + '_active_android.txt')
    # sort by newuser/active
    #df_newuser_ios.sort_values(by='newuser', ascending=False, inplace=True)
    df_active_ios.sort_values(by='active', ascending=False, inplace=True)
    #df_newuser_android.sort_values(by='newuser', ascending=False, inplace=True)
    df_active_android.sort_values(by='active', ascending=False, inplace=True)
    #print df_newuser_ios
    #print df_active_ios
    #print df_newuser_android
    #print df_active_android

    # 从某天的iOS或Android活跃排名来看
    with open('/Users/Alas/Desktop/top_active_ios_sdk_201704.txt', 'ab') as f1:
        for pid in df_active_ios['productid']:
            try:
                pname = df_lookup_table_ios.ix[pid].values[0]
            except Exception, e:
                pname = ''
                print e, pid
                continue
            #print pid, pname, df_active_ios[df_active_ios['productid']==pid]['active'].values[0]
            to_write_strings = day + ',' + str(pid) + ',' + pname + ',' +\
                    str(df_active_ios[df_active_ios['productid']==pid]['active'].values[0]) + '\n'
            f1.write(to_write_strings)


    with open('/Users/Alas/Desktop/top_active_android_sdk_201704.txt', 'ab') as f1:
        for pid in df_active_android['productid']:
            try:
                pname = df_lookup_table_android.ix[pid].values[0]
            except Exception, e:
                pname = ''
                print e, pid
                continue
            #print pid, pname, df_active_android[df_active_android['productid']==pid]['active'].values[0]
            to_write_strings = day + ',' + str(pid) + ',' + pname + ',' +\
                    str(df_active_android[df_active_android['productid']==pid]['active'].values[0]) + '\n'
            f1.write(to_write_strings)
"""


