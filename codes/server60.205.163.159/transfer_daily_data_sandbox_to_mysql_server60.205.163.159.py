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
            #db = 'thirdpart',
            charset = 'utf8',)
except Exception, e:
    print e
    sys.exit()
cursor = conn.cursor()

# CREATE TABLE a example
#try:
#    mysql = """CREATE TABLE active_iOS(
#            date char(30),
#            productid int(20) not null,
#            active_iOS float(20))"""
#    cursor.execute(mysql)
#except Exception, e:
#    print e
#    conn.rollback()

# 待传输数据[分月(文件夹)分天(文件)]
working_space = '/Users/Alas/Documents/TD_handover/sandbox_data_jupyter/'

list_month = os.listdir(working_space + 'daily_data_from_interface')
list_month = [item for item in list_month if '.' not in item]
#print list_month

# 分月(文件夹名)
for month in list_month:
    path_files_onemonth = working_space + 'daily_data_from_interface/' + month + '/'
    # 一个月所有的文件列表(一天4个文件)
    list_files_onemonth = os.listdir(path_files_onemonth)
    list_files_onemonth = [item for item in list_files_onemonth if '.DS' not in item]
    #print list_files_onemonth

    # 分天(文件名)
    for day in list_files_onemonth:
        # 一天四个不同类型的文件, 分别处理
        if month<='2017-07' and day[:10]<'2017-07-09':
            continue
        print month, day

        if 'active_iOS' in day:
            df_active_iOS_onemonth = pd.read_csv(path_files_onemonth + day)
            #print df_active_iOS_onemonth.head()
            #print day
            for i in df_active_iOS_onemonth.index:
                date = day[:10]
                productid, value = df_active_iOS_onemonth.ix[i].values
                #print [date, productid, value,]
                try:
                    # 给字符或字符串占位, 还得加上引号
                    sql = """INSERT INTO active_ios (date, productid, active_iOS)
                            VALUES ('{0}', {1}, {2})"""
                    sql = sql.format(date, productid, value)
                    #print sql
                    cursor.execute(sql)
                    conn.commit()
                except Exception, e:
                    print e
                    conn.rollback()
        elif 'active_android' in day:
            df_active_android_onemonth = pd.read_csv(path_files_onemonth + day)
            #print df_active_android_onemonth.head()
            #print day
            for i in df_active_android_onemonth.index:
                date = day[:10]
                productid, value = df_active_android_onemonth.ix[i].values
                #print [date, productid, value,]
                try:
                    sql = """INSERT INTO active_android (date, productid, active_android)
                            VALUES ('{0}', {1}, {2})"""
                    sql = sql.format(date, productid, value)
                    cursor.execute(sql)
                    conn.commit()
                except Exception, e:
                    print e
                    conn.rollback()
        elif 'newuser_iOS' in day:
            df_newuser_iOS_onemonth = pd.read_csv(path_files_onemonth + day)
            #print day
            #print df_newuser_iOS_onemonth.head()
            for i in df_newuser_iOS_onemonth.index:
                date = day[:10]
                productid, value = df_newuser_iOS_onemonth.ix[i].values
                #print [date, productid, value,]
                try:
                    sql = """INSERT INTO newuser_ios (date, productid, newuser_iOS)
                            VALUES ('{0}', {1}, {2})"""
                    sql = sql.format(date, productid, value)
                    cursor.execute(sql)
                    conn.commit()
                except Exception, e:
                    print e
                    conn.rollback()
        elif 'newuser_android' in day:
            df_newuser_android_onemonth = pd.read_csv(path_files_onemonth + day)
            #print df_newuser_android_onemonth.head()
            #print day
            for i in df_newuser_android_onemonth.index:
                date = day[:10]
                productid, value = df_newuser_android_onemonth.ix[i].values
                try:
                    sql = """INSERT INTO newuser_android (date, productid, newuser_android)
                            VALUES ('{0}', {1}, {2})"""
                    sql = sql.format(date, productid, value)
                    cursor.execute(sql)
                    conn.commit()
                except Exception, e:
                    print e
                    conn.rollback()
        else:
            continue

conn.close()
