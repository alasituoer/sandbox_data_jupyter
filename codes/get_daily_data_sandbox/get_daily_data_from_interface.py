#coding:utf-8
import urllib2
import json
import calendar

# 从沙箱接口下载指定天日期的


working_space = '/sandbox_data_jupyter/'

def GetAllDaysOfOneMonth(curmonth):
    """以'2016-09'个格式输入某个月日期
        以列表['2016-09-01', '2016-09-02', ..., '2016-09-30',]的形式返回该月所有的天日期"""
    year, month = curmonth.split('-')
    #print [year, month]
    days_curmonth = calendar.monthrange(int(year), int(month))[1]
    return [curmonth + '-0' + str(i) for i in range(1, 10)] +\
            [curmonth + '-' + str(i) for i in range(10, days_curmonth+1)]
#print GetAllDaysOfOneMonth('2016-09')


def GetTop1wNewuserActiveOneDay(day):
    """获取某一天top1w的新增数据"""
    url = ‘*’
    # 1代表Android 2代表iOS
    dict_platformid = {1: 'android', 2: 'iOS',}
    for platformid in [1, 2,]:
        # 构造访问地址的参数
        data_dict = {'metrics': ['newuser'], 'groupby': 'productid',
                        'conditions': {
                            'platformid': str(platformid),
                            'top': 10000, 'start': day, 'end': day}}
        para_json_newuser = json.dumps(data_dict)

        #print [data_dict]
        #print [para_json_newuser]
        #req1 = urllib2.Request(url)

        req1 = urllib2.Request(url, para_json_newuser)
        # 指定返回的对象类型
        req1.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req1)

        # 读取响应结果
        newuser_result = response.read()
        # 转换为JSON格式
        data_json_newuser = json.loads(newuser_result)[0]
        #print data_json_newuser.keys()[:5]
        #print len(data_json_newuser)
        #print data_json_newuser

        # 构造保存文件名形如: 2017-04-18_newuser_iOS.txt
        # 存放到所属月份文件夹 '2017-04-18'[:-3] -> '2017-04'文件夹
        path_to_write_and_filename = working_space + 'daily_data_from_interface/' +\
                day[:-3] + '/' + day + '_newuser_' + dict_platformid[platformid] + '.txt'
        with open(path_to_write_and_filename, 'wb') as f1:
            f1.write('productid,newuser\n')
            for productid in data_json_newuser.keys():
                #print [productid, data_json_newuser[productid]]
                f1.write(productid + ',' + str(data_json_newuser[productid]) + '\n')

        # 访问活跃数据的网址所需参数与新增不一样(新增是限制top1w)
        # 活跃采用那些有新增的productid构成productid list参数
        product_list = []
        for k in data_json_newuser:
            product_list.append(k)
        #print product_list

        para_json_active = json.dumps({
                "metrics": ["launchuser"],
                "groupby": "productids",
                "conditions": {
                        "productid_list": product_list,
                        "start": day,
                        "end": day}})
        req2 = urllib2.Request(url, para_json_active)
        req2.add_header('Content-Type','application/json')
        response = urllib2.urlopen(req2)
        active_result = response.read()
        data_json_active = json.loads(active_result)[0]
        #print data_json_active

        path_to_write_and_filename = working_space + 'daily_data_from_interface/' +\
                day[:-3] + '/' + day + '_active_' + dict_platformid[platformid] + '.txt'
        with open(path_to_write_and_filename, 'wb') as f2:
            f2.write('productid,active\n')
            for productid in data_json_active.keys():
                f2.write(productid + ',' + str(data_json_active[productid]) + '\n')


# 更改需要爬取的时间
list_day = GetAllDaysOfOneMonth('2017-08')[24:]
print list_day
#for oneday in list_day:
#    GetTop1wNewuserActiveOneDay(oneday)



