#coding:utf-8
import pandas as pd
import numpy as np

working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/project/'

# 指定Apps的免费榜排名数据
path_top_free_rank = working_space + 'apps_in_top_free_rank_with_sdk_201404-201704.xlsx'
# 指定Apps的沙箱iOS新增数据
path_newuser_ios = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/computed_daily_data/newuser_ios/'

df_rank = pd.read_excel(path_top_free_rank, sheetname=0)
df_rank.fillna(0, inplace=True)
#print df_rank.columns
# 从Excel文件读取的时间格式是datetime.datetime的对象
# 需要将其转换为'2017-05-26'的格式, 与排名数据的时间格式一致
list_new_columns = list(df_rank.columns[:4])
for col in df_rank.columns[4:]:
    #print [col.strftime('%Y-%m-%d')]
    list_new_columns.append(col.strftime('%Y-%m-%d'))
#print list_new_columns
df_rank.columns = list_new_columns
#print df_rank.head()

for i in range(len(df_rank)):
    #print df_rank.ix[i]['Product Id']
    onepid = df_rank.ix[i]['Product Id']
    try:
        df_newuser_ios_onepid = pd.read_csv(path_newuser_ios +\
                str(onepid) + '_newuser_ios.csv')
    except Exception, e:
        print e
        continue
#    print df_newuser_ios_onepid.head()

    # 得到某一个productid对应appid的历史排名值'2014-04-01'到'2017-05-26'
    ss_rank_onepid = df_rank.ix[i].T[4:]
    # 得到某一个productid对应的有监测活跃量(时间段不固定)
    df_newuser_ios_onepid.index = df_newuser_ios_onepid['date']
    ss_newuser_ios_onepid = df_newuser_ios_onepid['newuser']
#    ss_newuser_ios_onepid.to_csv('~/Desktop/t.csv')
#    print onepid
#    print ss_rank_onepid.head()
#    print ss_rank_onepid.tail()
#    print ss_newuser_ios_onepid.head()
#    print ss_newuser_ios_onepid.tail()

    # 根据该productid沙箱有效数据对应的时间段来截取时间看排名
    # 先得到有效活跃数据的开始和结束时间
#    print ss_newuser_ios_onepid.head()
#    print ss_newuser_ios_onepid.tail()
    start_date = ss_newuser_ios_onepid[:1].index.values[0]
    end_date = ss_newuser_ios_onepid[-1:].index.values[0]
#    print start_date, end_date

    # 由此时间来截取得到所需时间段的排名数据
#    print ss_rank_onepid.head()
#    print ss_rank_onepid.tail()
    ss_rank_onepid = ss_rank_onepid.ix[start_date:end_date]

    # 
    #if len(ss_newuser_ios_onepid) != len(ss_rank_onepid):
    #    print len(ss_newuser_ios_onepid), len(ss_rank_onepid)
    #    ss_newuser_ios_onepid.to_csv('~/Desktop/test_ss_newuser_ios_onepid/' +\
    #            'ss_newuser_ios_' + str(onepid) + '.csv')

#    print onepid
    list_index = ss_newuser_ios_onepid.index
#    print list_index[0], list_index[-1]

    # 计算有效活跃量的日环比和对应排名的日环比
    list_momc_newuser_ios = []
    list_momc_rank = []
    for j in range(len(list_index)-1):
#        print list_index[j], list_index[j+1]
#        print ss_newuser_ios_onepid.ix[list_index[j+1]], ss_newuser_ios_onepid.ix[list_index[j]]
#        print ss_rank_onepid.ix[list_index[j+1]], ss_rank_onepid.ix[list_index[j]]

        try:
            list_momc_newuser_ios.append(\
                    ss_newuser_ios_onepid.ix[list_index[j+1]]/ss_newuser_ios_onepid.ix[list_index[j]] - 1)
        except Exception, e:
            print e
            list_momc_newuser_ios.append(0)
        try:
            list_momc_rank.append(ss_rank_onepid.ix[list_index[j]]/ss_rank_onepid.ix[list_index[j+1]] - 1)
        except Exception, e:
            print e
            list_momc_rank.append(0)

    # 得到历史每日两个环比的乘积列表, 如果乘积为正则说明当天的活跃量与排名的趋势一致
    list_flag_momc = [i*j for i,j in zip(list_momc_newuser_ios, list_momc_rank)]
#    print list_momc_newuser_ios[-1], list_momc_rank[-1], list_flag_momc[-1]
#    print list_flag_momc[:10]

    # 去除乘积是缺失的以及负无穷大的(正无穷大即分母为零的自动缺失)
    list_flag_momc = [x for x in list_flag_momc if str(x) != 'nan' and str(x) != '-inf']
#    print list_flag_momc


    # 统计趋势旗表中正负数的总数
    counts_pos = 0
    for c in list_flag_momc:
        if c>0:
            counts_pos += 1
    with open(working_space + '统计任意应用所有历史日新增量与日排名环比趋势一致的程度.txt', 'ab') as f1:
        try:
            to_write_strings = str(onepid) + ',' + str(counts_pos) + ',' +\
                    str(len(list_flag_momc)) + ',' + str(counts_pos*1.0/len(list_flag_momc)) + '\n'
        except Exception, e:
            print e
            to_write_strings = str(onepid) + ',' + str(counts_pos) + ',' +\
                    str(len(list_flag_momc)) + ',' + '' + '\n'
        f1.write(to_write_strings)




