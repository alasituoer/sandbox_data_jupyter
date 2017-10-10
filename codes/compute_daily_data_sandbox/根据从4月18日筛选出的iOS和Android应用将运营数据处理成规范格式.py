#coding:utf-8
import pandas as pd

working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/'
path_sdk_ios_apps_cat = working_space + 'lookup_table_from_dawei/' 
path_sdk_android_apps_cat = working_space + 'lookup_table_from_dawei/'

df_sdk_ios_apps_cat = pd.read_table(path_sdk_ios_apps_cat + 'SDK_iOS_Apps_CAT.txt')
df_sdk_android_apps_cat = pd.read_table(path_sdk_android_apps_cat + 'SDK_Android_Apps_CAT.txt')
#print df_sdk_ios_apps_cat.head()
#print df_sdk_android_apps_cat.head()

# 分平台将所有Apps的日活跃数据导入TXT或Excel文件中
path_computed_daily_data_active_ios = working_space + 'computed_daily_data/active_ios/'
for pid in df_sdk_ios_apps_cat['Productid'][:1]:
    pname = df_sdk_ios_apps_cat[df_sdk_ios_apps_cat['Productid']==pid]['Chinese Name'].values[0]
    df_active_ios_daily_data_onepid = pd.read_csv(path_computed_daily_data_active_ios +\
            str(pid) + '_active_ios.csv')
    print pid, pname




# 不用程序计算各月的平均值
# 采用输出原始数据到Excel文件中再另行计算的方法
"""
    # 先截取2017年2月以后的月活跃
    df_after201702 = df_active_ios_daily_data_onepid[df_active_ios_daily_data_onepid['date']>'2017-02-00']
    df_after201702 = df_after201702[['date', 'active']]
    # 再分别计算2、3、4月份的月活跃平均值
    df_201702 = df_after201702[df_after201702['date']<'2017-03-00']
    df_201703 = df_after201702[df_after201702['date']>'2017-03-00']
    df_201703 = df_201703[df_201703['date']<'2017-04-00']
    df_201704 = df_after201702[df_after201702['date']>'2017-04-00']
    print df_201702['active'].mean(), df_201703['active'].mean(), df_201704['active'].mean()

path_computed_daily_data_active_android = working_space + 'computed_daily_data/active_android/'
for pid in df_sdk_android_apps_cat['Productid']:
    pname = df_sdk_android_apps_cat[df_sdk_android_apps_cat['Productid']==pid]['Chinese Name'].values[0]
    df_active_android_daily_data_onepid = pd.read_csv(path_computed_daily_data_active_android +\
            str(pid) + '_active_android.csv')
    #print pid, pname
    #print df_active_android_daily_data_onepid.head()
    #print '\n'

"""





