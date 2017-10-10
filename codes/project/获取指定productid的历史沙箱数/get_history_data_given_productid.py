#coding:utf-8
import os
import pandas as pd

# 有两种方法获得指定ProductID的历史沙箱新增或活跃值
# 一是从本地, 一是从服务器60.205.163.159 mysql: sandbox_data

working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/'

# 获取历史月份列表
path_history_month = working_space + 'daily_data_from_interface/'
list_history_month = os.listdir(path_history_month)
if '.DS_Store' in list_history_month:
    list_history_month.remove('.DS_Store')
#print list_history_month


def Get_Active_and_Newuser_History_Data_From_Sandbox(productid, path_to_write):
    with open(path_to_write, 'wb') as f1:
        for month in list_history_month:
            # 获取每个月份下的文件总数(4*月数)
            path_files_onemonth = path_history_month + month + '/'
            list_files_onemonth = os.listdir(path_files_onemonth)
            if '.DS_Store' in list_files_onemonth:
                list_files_onemonth.remove('.DS_Store')
    #        print list_files_onemonth
    
            # 依次获取每个文件(从中查询得到指定ProductID在该天该指标下的值)
            for f in list_files_onemonth:
                df_onefile_onemonth = pd.read_table(path_files_onemonth + f, sep=',', index_col=0,)
                #print df_onefile_onemonth.head()
                try:
                    the_value = df_onefile_onemonth.ix[productid].values[0]
                except Exception, e:
                    #print e, f, "can't find the productid."
                    continue
            
    #            print productid, f[:10], f[11:-4], the_value
                to_write_strings = str(productid) + ',' + f[:10] + ',' + f[11:-4]\
                        + ',' + str(the_value) + '\n'
                f1.write(to_write_strings)
           

# 待查找ProductID列表
productid = 3093682
#path_to_write = working_space + 'project/获取指定ProductID的沙箱活新增或活跃值/re.txt'
path_to_write = '/Users/Alas/Desktop/华住.txt'
Get_Active_and_Newuser_History_Data_From_Sandbox(productid, path_to_write)








