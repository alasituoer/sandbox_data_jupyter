#coding:utf-8
import pandas as pd

working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/computed_daily_data/'

df_active_ios_sdk = pd.read_csv(working_space + 'top_active_ios_sdk_201704.txt', header=None)
df_active_android_sdk = pd.read_csv(working_space + 'top_active_android_sdk_201704.txt', header=None)
df_active_ios_sdk.columns = ['Date', 'Productid', 'Chinese Name', 'Active_iOS',]
df_active_android_sdk.columns = ['Date', 'Productid', 'Chinese Name', 'Active_android',]
#print df_active_ios_sdk.head()
#print df_active_android_sdk.head()
#print len(df_active_ios_sdk['Chinese Name'].unique())
#print len(df_active_android_sdk['Chinese Name'].unique())
list_allapps_active_ios = df_active_ios_sdk['Chinese Name'].unique()
list_allapps_active_android = df_active_android_sdk['Chinese Name'].unique()

# 不属于CAT的应用中文名
df_cname = pd.read_excel('/Users/Alas/Downloads/downloads/others/Chengwen/20170510-招聘类应用的处理方法/招聘类应用_工具表_201704.xlsx', sheetname=1)
#print df_cname.head()

for cname_check in df_cname['Chinese']:
    #print cname_check
    with open(working_space + 'top300_names_active_ios.txt', 'ab') as f1:
        for cname_sdk in list_allapps_active_ios:
            if cname_check in cname_sdk:
                #print cname_sdk
                productid = df_active_ios_sdk[df_active_ios_sdk['Chinese Name']==cname_sdk]['Productid'].values[0]
                to_write_strings = cname_check + '\t' + cname_sdk + '\t' + str(productid) + '\n'
                f1.write(to_write_strings)

    with open(working_space + 'top300_names_active_android.txt', 'ab') as f2:
        for cname_sdk in list_allapps_active_android:
            if cname_check in cname_sdk:
                #print cname_sdk
                productid = df_active_android_sdk[df_active_android_sdk['Chinese Name']==cname_sdk]['Productid'].values[0]
                to_write_strings = cname_check + '\t' + cname_sdk + '\t' + str(productid) + '\n'
                f2.write(to_write_strings)



