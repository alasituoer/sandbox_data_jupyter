#coding:utf-8
import pandas as pd
import numpy as np

working_space = '/Users/Alas/Documents/TD/iOS_rank_estimate_model/ver_py/'

# sheetname 缺省时 pd.read_excel默认读取第一张表的
# sheetname = 0 时读取第一张表
# sheetname = 'New_user_free_rank' 写入具体表名
# sheetname = None 返回多个表组成的DataFrame字典, 通过关键字调用

# ios_free_rank
df_ios_free_rank = pd.read_excel(working_space +\
        'source_files/ios_free_rank_V1.xlsx', sheetname='New_user_free_rank')
#print df_ios_free_rank.ix['2014/8/1']
# 后面会自动跳过缺失值计算总和和平均值, 此处不用特地置0
#df_ios_free_rank = df_ios_free_rank.fillna(0)
#print df_ios_free_rank.ix['2014/8/1']

# ios_assorting_rank
#df_ios_assorting_rank = pd.read_excel(working_space +\
#        'source_files/ios_assorting_rank_V1.xlsx', sheetname='Billing rank')
#df_ios_assorting_rank = df_ios_assorting_rank.fillna(0)
#print df_ios_assorting_rank.ix['2015/4/8']

# 每个排名对应的新增或收入的历史总和、平均值、中位数
# compute the sum/average/median of ios_free_rank
# 缺省axis=1是默认按列计算, 缺省skipna=Ture默认是跳过缺失值计算
ss_sum_ios_free_rank = df_ios_free_rank.sum()
ss_mean_ios_free_rank = df_ios_free_rank.mean()
ss_median_ios_free_rank = df_ios_free_rank.median()
#print ss_sum_ios_free_rank
#print ss_mean_ios_free_rank
#print ss_median_ios_free_rank

df_info_data_process = pd.DataFrame({
        'sum': ss_sum_ios_free_rank,
        'mean': ss_mean_ios_free_rank,
        'median': ss_median_ios_free_rank,})
df_info_data_process.index.names = ['rank']
df_info_data_process.fillna(0, inplace=True)
#print df_info_data_process
#print list(df_info_data_process['mean'].values)

# define funciton computing_outliers deal with outliers
# 输入是一个一维的数组, 通过函数"多次"纠正那些异常的值(严重偏离既定趋势的值)
def computing_outliers(ss_data, window_len, interval, num_n):
    length_ss_data = len(ss_data) 
    list_with_interval = range(0, length_ss_data, interval)
    #print list_with_interval
    #print length_ss_data, len(list_with_interval)

    # 倒序核查(删除下一个值时不受列表长度影响), 若已经满足分组, 则将多余的分组去掉
    for i in list_with_interval[::-1]:
        if i+window_len>length_ss_data:
            list_with_interval.remove(i)
    #print list_with_interval

    # 根据不同分组(每组20个排名对应值)找出异常值
    for i in list_with_interval:
        for j in range(1, num_n):
            #print i, i+window_len
            ss_one_group = ss_data[i:i+window_len]
            #print ss_one_group

            # 根据对列表中的每个数据分配Z-Score, 判定Z-Score最高的即为异常值
            zscore_one_group = [abs((x-np.mean(ss_one_group))/np.std(ss_one_group))\
                    for x in ss_one_group]
            d1 = zip(ss_one_group, zscore_one_group)
            d2 = sorted(d1, key = lambda item:item[1], reverse=True)
            outliers = d2[0][0]

            # 根据异常值在输入数据中反向匹配, 重置异常值
            try:
                index_outliers = ss_one_group[ss_one_group==outliers].index.values[0]
            except Exception, e:
                print e, '\t', i, j, outliers

            # 屏幕输出每次调整过的值
            #print ss_one_group[ss_one_group==outliers]

            # 如果异常值在每组的第一位
            if index_outliers == i:
                ss_data.ix[index_outliers] = np.mean([ss_data.ix[i], ss_data.ix[i+1]])
            # 如果异常值在每组的最后一位
            elif index_outliers == i+window_len:
                ss_data.ix[index_outliers] = np.mean([ss_data.ix[i+window_len-1], ss_data.ix[i+window_len]])
            # 如果异常值既不在每组的第一位也不在每组的最后一位
            else:
                #ss_data.ix[index_outliers] = ss_data.ix[index_outliers-1] + ss_data.ix[index_outliers+1]
                ss_data.ix[index_outliers] = np.mean([ss_data.ix[index_outliers-1], ss_data.ix[index_outliers+1]])
            #print ss_data[i:i+window_len]

    return ss_data


para = df_info_data_process['mean']
#print para[:20]
test_para = computing_outliers(para, 20, 5, 10)
#print test_para[:20]

df_info_data_process['test_para'] = test_para
#print df_info_data_process[:20]

para.to_csv(working_space + 'sample.csv')
df_info_data_process.to_csv(working_space + 'model_data.csv')







