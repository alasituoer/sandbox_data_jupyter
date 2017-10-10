#coding:utf-8
import os
import sys
import MySQLdb
import pandas as pd

try:
    conn = MySQLdb.connect(
            host = '60.205.163.159',
            port = 3306,
            user = 'alas',
            passwd = '6143',
            db = 'sandbox_data',
            charset = 'utf8',)
except Exception, e:
    print e
    sys.exit()
cursor = conn.cursor()

# CREATE TABLE a example
mysql = """CREATE TABLE lookup_table_v1(
        productid int(20) not null,
        product_name char(50),
        product_type int(5),
        platform int(5))"""
try:
    cursor.execute(mysql)
except Exception, e:
    print e
    conn.rollback()

# 待传输数据[分月(文件夹)分天(文件)]
working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/lookup_table_from_dawei/'
df_lookup_table = pd.read_csv(working_space + 'product_basic_info_revised.txt')
#print df_lookup_table.head()

for i in range(len(df_lookup_table)):
#for i in range(3):
    productid, product_name, product_type, platform = df_lookup_table.ix[i].values
    try:
        # 给字符或字符串占位, 还得加上引号
        sql = """INSERT INTO lookup_table_v1 (productid, product_name, product_type, platform)
        VALUES ({0}, '{1}', {2}, {3})"""
        sql = sql.format(productid, product_name, product_type, platform)
        #print sql
        cursor.execute(sql)
        conn.commit()
    except Exception, e:
        print e
        conn.rollback()

conn.close()




