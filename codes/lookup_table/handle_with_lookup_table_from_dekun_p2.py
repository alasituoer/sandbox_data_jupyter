#coding:utf-8
import pandas as pd

# 按照 packagename and productid 筛选得到的两张表
# 再按照 productid and packagename 筛选
working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/lookup_table_from_dekun/'

df_dif_pk_onepid = pd.read_csv(working_space + 'dif_pk_onepid.txt', )
df_dif_pid_onepk = pd.read_csv(working_space + 'dif_pid_onepk.txt', )
#print df_dif_pk_onepid.head()
#print df_dif_pid_onepk.head()

#print len(df_dif_pk_onepid['productid']), len(df_dif_pk_onepid['productid'].unique())
#print len(df_dif_pid_onepk['packagename']), len(df_dif_pid_onepk['packagename'].unique())

with open(working_space + 'lt_pk_pid.txt', 'wb') as f1:
    f1.write('packagename,productid\n')
    for pid in df_dif_pk_onepid['productid'].unique():
        list_pk_onepid =\
                df_dif_pk_onepid[df_dif_pk_onepid['productid']==pid]['packagename'].values
        if len(list_pk_onepid)==1:
#            print list_pk_onepid[0], pid
            f1.write(list_pk_onepid[0] + ',' + str(int(pid)) + '\n')

with open(working_space + 'lt_pid_pk.txt', 'wb') as f2:
    f2.write('packagename,productid\n')
    for pk in df_dif_pid_onepk['packagename'].unique():
        list_pid_onepk =\
                df_dif_pid_onepk[df_dif_pid_onepk['packagename']==pk]['productid'].values
        if len(list_pid_onepk)==1:
#            print pk, list_pid_onepk[0]
            f2.write(pk + ',' + str(int(list_pid_onepk[0])) + '\n')





