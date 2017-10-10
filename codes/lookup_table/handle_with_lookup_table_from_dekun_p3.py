#coding:utf-8
import pandas as pd

# 以此从筛选出的两张表中按packagename和productid
# 在原始对照表中查看, 核对是否是唯一对应
working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/lookup_table_from_dekun/'

df_lt_pk_pid = pd.read_csv(working_space + 'lt_pk_pid.txt',)
df_lt_pid_pk = pd.read_csv(working_space + 'lt_pid_pk.txt',)
#print df_lt_pk_pid.head()
#print df_lt_pid_pk.head()

# 限制在ta线, 只用到 pacakgename and productid 两个字段
# df_lt_sf == df_lookup_table_source_file
df_lt_sf = pd.read_csv(working_space + 'appkey_packagename.csv',)
df_lt_sf = df_lt_sf[df_lt_sf['source']=='ta'][['packagename', 'productid']]
#print df_lt_sf.head()

#print len(df_lt_pk_pid['packagename']), len(df_lt_pk_pid['packagename'].unique())
#print len(df_lt_pk_pid['productid']), len(df_lt_pk_pid['productid'].unique())
#print len(df_lt_pid_pk['packagename']), len(df_lt_pid_pk['packagename'].unique())
#print len(df_lt_pid_pk['productid']), len(df_lt_pid_pk['productid'].unique())

"""
# 跟原始表核对是否唯一对应
for pk in df_lt_pk_pid['packagename']:
    if len(df_lt_sf[df_lt_sf['packagename']==pk])>1:
        print 'lt_pk_pid: ', pk
for pid in df_lt_pk_pid['productid']:
    if len(df_lt_sf[df_lt_sf['productid']==pid])>1:
        print 'lt_pk_pid: ', pid
for pk in df_lt_pid_pk['packagename']:
    if len(df_lt_sf[df_lt_sf['packagename']==pk])>1:
        print 'lt_pid_pk: ', pk
for pid in df_lt_pid_pk['productid']:
    if len(df_lt_sf[df_lt_sf['productid']==pid])>1:
        print 'lt_pid_pk: ', pid
"""


# 将筛选出的两张表合并, 求并集并看重复率
df_lt = pd.concat([df_lt_pk_pid, df_lt_pid_pk])
#print df_lt.head()
#print len(df_lt_pk_pid), len(df_lt_pid_pk), len(df_lt)
df_lt.drop_duplicates(inplace=True)
#print len(df_lt_pk_pid), len(df_lt_pid_pk), len(df_lt)
# 重排index
#print df_lt.ix[18]
df_lt.index = range(len(df_lt))
#print df_lt.ix[18]

with open(working_space + 'lt.txt', 'wb') as f1:
    f1.write('packagename,productid\n')
    for i in range(len(df_lt)):
#        print df_lt.ix[i]
        pk, pid = df_lt.ix[i].values
#        print [pk, pid,]
        if (len(df_lt_sf[df_lt_sf['packagename']==pk])==1 and\
                len(df_lt_sf[df_lt_sf['productid']==pid])==1):
            f1.write(pk + ',' + str(pid) + '\n')
        else:
            print [pk, pid,]


