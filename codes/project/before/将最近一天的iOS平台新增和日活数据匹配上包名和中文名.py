#coding:utf-8
import pandas as pd

# 利用筛选出的唯一对照表匹配上最近一天新增或活跃数据中应用的包名

working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/'

# 导入productid与packagename的一对一表lt.txt
# 'lt_pk_prodid' == 'lookup table of package name and productid of apps'
path_lt_pk_pid = working_space + 'lookup_table_from_dekun/'
df_lt = pd.read_csv(path_lt_pk_pid + 'lt.txt')
#print df_lt.head()

# 读入最近一天的数据
date = '2017-05-21'
path_oneday = working_space + 'get_daily_data_from_interface/2017-05/'
df_newuser_ios_oneday = pd.read_csv(path_oneday + date + '_newuser_iOS.txt')
df_active_ios_oneday = pd.read_csv(path_oneday + date + '_active_iOS.txt')
df_newuser_ios_oneday.sort_values(by='newuser', inplace=True, ascending=False)
df_active_ios_oneday.sort_values(by='active', inplace=True, ascending=False)
#print df_newuser_ios_oneday.head()
#print df_active_ios_oneday.head()

# 读入大伟给出的productid与中文对照表作为参考(中文名未标准化)
df_pid_cname = pd.read_csv(working_space + 'lookup_table_from_dawei/product_basic_info_revised.txt')
# 只取platform=2即iOS平台的对应数据
df_pid_cname = df_pid_cname[df_pid_cname['platformid']==2][['productid', 'product_name', 'platformid']]
#print df_pid_cname.head()


# 数据存放路径
path_to_write = working_space + '/project/将最近一天的iOS平台新增和日活数据匹配上包名和中文名/'

with open(path_to_write + 'newuser_ios_including_package_name_' + date+ '.txt', 'wb') as f1:
    f1.write('ProductId,NewUser,PackageName,AppName\n')
    for pid in df_newuser_ios_oneday['productid']:
        data = df_newuser_ios_oneday[df_newuser_ios_oneday['productid']==pid]['newuser'].values[0]
        try:
            pkname = df_lt[df_lt['productid']==pid]['packagename'].values[0]
        except Exception, e:
            print e, '\t', pid
            pkname = 'N/A'
        try:
            appname = df_pid_cname[df_pid_cname['productid']==pid]['product_name'].values[0]
        except Exception, e:
            print e, '\t', pid
            appname = 'N/A'
        f1.write(str(pid) + ',' + str(data) + ',' + pkname + ',' + appname + '\n')


with open(path_to_write + 'active_ios_including_package_name_' + date+ '.txt', 'wb') as f2:
    f2.write('ProductId,Active,PackageName,AppName\n')
    for pid in df_active_ios_oneday['productid']:
        data = df_active_ios_oneday[df_active_ios_oneday['productid']==pid]['active'].values[0]
        try:
            pkname = df_lt[df_lt['productid']==pid]['packagename'].values[0]
        except Exception, e:
            print e, '\t', pid
            pkname = 'N/A'
        try:
            appname = df_pid_cname[df_pid_cname['productid']==pid]['product_name'].values[0]
        except Exception, e:
            print e, '\t', pid
            appname = 'N/A'
        f2.write(str(pid) + ',' + str(data) + ',' + pkname + ',' + appname + '\n')


    

"""
# 读入原始对照表, 只取ta线的 packagename and productid 字段
df_lt_sf = pd.read_csv(path_lt_pk_pid + 'appkey_packagename.csv',)
df_lt_sf = df_lt_sf[df_lt_sf['source']=='ta'][['packagename', 'productid']]
#print df_lt_sf.head()
for pid in df_newuser_ios_oneday['productid']:
#for pid in df_active_ios_oneday['productid']:
    #print len(df_lt_sf[df_lt_sf['productid']==pid])
    if len(df_lt_sf[df_lt_sf['productid']==pid])==1:
        print pid
"""
