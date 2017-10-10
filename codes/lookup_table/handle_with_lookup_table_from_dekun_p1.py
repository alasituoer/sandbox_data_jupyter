#coding:utf-8
import pandas as pd

#找出ta线中应用 productid 与 package name 间的对应关系

working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/lookup_table_from_dekun/'

df_lt_pk_pid = pd.read_csv(working_space + 'appkey_packagename.csv')
df_lt_pk_pid = df_lt_pk_pid[df_lt_pk_pid['source']=='ta']
df_lt_pk_pid = df_lt_pk_pid[['packagename', 'productid']]
df_lt_pk_pid.fillna('0', inplace=True)
#print df_lt_pk_pid.head()

#print len(df_lt_pk_pid['packagename']), len(df_lt_pk_pid['packagename'].unique())
#print len(df_lt_pk_pid['productid']), len(df_lt_pk_pid['productid'].unique())


flag = 0
with open(working_space + 'dif_pk_onepid.txt', 'wb') as f1:
    f1.write('packagename,productid\n')
    for pkname in df_lt_pk_pid['packagename'].unique():
        list_pid_onepk =\
                df_lt_pk_pid[df_lt_pk_pid['packagename']==pkname]['productid'].values
        if len(list_pid_onepk)==1:
#            print pkname, list_pid_onepk[0]
#            flag += 1
            f1.write(pkname + ',' + str(int(list_pid_onepk[0])) + '\n')
#        if flag%1000==0:
#            print flag
#    print flag


with open(working_space + 'dif_pid_onepk.txt', 'wb') as f2:
    f2.write('packagename,productid\n')
    for pid in df_lt_pk_pid['productid'].unique():
        list_pk_onepid =\
                df_lt_pk_pid[df_lt_pk_pid['productid']==pid]['packagename'].values
        if len(list_pk_onepid)==1:
#            print list_pk_onepid[0], pid
            f2.write(list_pk_onepid[0] + ',' + str(int(pid)) + '\n')








