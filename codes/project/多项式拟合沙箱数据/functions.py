#coding:utf-8
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import calendar

def GetAllDaysOfOneMonth(onemonth):
    """以格式'2017-06'输入某个月
        以['2017-06-01', '2017-06-02', ..., '2017-06-30',]的格式返回该月的所有天日期"""
    year, month = onemonth.split('-')
    days_themonth = calendar.monthrange(int(year), int(month))[1]
    list_days_themonth = [onemonth + '-0' + str(i) for i in range(1, 10)] +\
            [onemonth + '-' + str(i) for i in range(10, days_themonth+1)]
    return list_days_themonth
#print GetAllDaysOfOneMonth('2017-06')


def FillnaRank(df_rank_newuser):
    """去掉排名缺失的部分, 返回按newuser从大到小排列的数据"""
    df_rank_newuser.sort_values(by='newuser_ios', ascending=False, inplace=True)
    df_rank_newuser = df_rank_newuser[df_rank_newuser['rank']!=0]
    return df_rank_newuser

"""
    for i in range(len(df_rank_newuser)):
        # 避开那些newuser为0的循环项, 因为依照此方法估计的当前rank可能因为前一排名是0而缺失
        if df_rank_newuser[i:i+1]['newuser_ios'].values[0] == 0:
            continue
        # 循环检查，如果当前rank值为0(0即视为缺失)
        if df_rank_newuser[i:i+1]['rank'].values[0] == 0:
            # 则先初始化待调整 rank and newuser
            rank_to_be_revised, newuser_to_be_revised = df_rank_newuser[i:i+1].values[0]
            #print rank_to_be_revised
            # 再依次检查前一个或者后一个rank值是否为0
            try:
                rank_previous, newuser_previous = df_rank_newuser[i-1:i].values[0]
            except Exception, e:
                print e, '取不到前一个rank newuser值'
            try:
                rank_next, newuser_next = df_rank_newuser[i+1:i+2].values[0]
            except Exception, e:
                print e, '取不到后一个rank newuser值'

            #print rank_previous, newuser_previous
            #print rank_to_be_revised, newuser_to_be_revised
            #print rank_next, newuser_next

            # 当newuser_previous为0时利用newuser_next!=0估计, 反之亦然
            # 当两者都不为0时, 用两个一起估计
            try:
                if newuser_previous != 0 and newuser_next == 0:
                    rank_to_be_revised = (rank_previous*newuser_to_be_revised)/newuser_previous
                elif newuser_next != 0 and newuser_previous == 0:
                    rank_to_be_revised = (rank_next*newuser_to_be_revised)/newuser_next
                elif newuser_next != 0 and newuser_previous != 0:
                    rank_to_be_revised = rank_previous - (rank_previous - rank_next) *\
                            (newuser_previous - newuser_to_be_revised) /\
                            (newuser_previous - newuser_next)
                else:
                    pass
            except Exception, e:
                print e
                continue
            # 重置缺失的排名值
            df_rank_newuser[i:i+1]['rank'].values[0] = int(round(rank_to_be_revised))
            # 按rank去重后返回
    df_rank_newuser.drop_duplicates(['rank'], inplace=True)
"""



def FillnaNewuser(df_rank_newuser):
    # 从FillnaRank得到的DataFrame是按'newuser_ios'排序的
    # 得按照"Rank"排序后估计"newuser_ios"的缺失部分
    df_rank_newuser.sort_values(by='rank', inplace=True)

    for i in range(len(df_rank_newuser)):
        # 避开那些rank为0的循环体(rank为0的部分无利于估计缺失或异常的的newuser)
        if df_rank_newuser[i:i+1]['rank'].values[0] == 0:
            continue
        flag = df_rank_newuser[i:i+1]['newuser_ios'].values[0]
        if flag == 0 or flag < 100:
            rank_to_be_revised, newuser_to_be_revised = df_rank_newuser[i:i+1].values[0]
            try:
                rank_previous, newuser_previous = df_rank_newuser[i-1:i].values[0]
            except Exception, e:
                print e, '取不到前一个rank newuser值'
            try:
                rank_next, newuser_next = df_rank_newuser[i+1:i+2].values[0]
            except Exception, e:
                print e, '取不到后一个rank newuser值'

            #print rank_previous, newuser_previous
            #print rank_to_be_revised, newuser_to_be_revised
            #print rank_next, newuser_next
            #print '\n'

            try:
                if rank_previous != 0 and rank_next == 0:
                    newuser_to_be_revised = (newuser_previous*rank_to_be_revised)/rank_previous
                elif rank_next != 0 and rank_previous == 0:
                    newuser_to_be_revised = (newuser_next*rank_to_be_revised)/rank_next
                elif rank_next != 0 and rank_previous != 0:
                    newuser_to_be_revised = newuser_previous - (newuser_previous - newuser_next) *\
                            (rank_previous - rank_to_be_revised) / (rank_previous - rank_next)
                else:
                    pass
            except Exception, e:
                print e
                continue
            df_rank_newuser[i:i+1]['newuser_ios'].values[0] =\
                    int(round(newuser_to_be_revised))
    return df_rank_newuser[df_rank_newuser['rank']!=0]


def FilterOutliers(df_rank_newuser):
    """若某个排名对应的新增量比未缺失且相邻新增量高出或低出太多, 则按照排名的相对关系对其修正"""
    df = df_rank_newuser[df_rank_newuser['rank']!=0][['rank', 'newuser_ios']]
    #print df
    for i in range(len(df)):
        try:
            rank_pre, newuser_pre = df[i-1:i].values[0]
            rank_now, newuser_now = df[i:i+1].values[0]
            rank_next, newuser_next = df[i+1:i+2].values[0]
            #if newuser_now*1.0/newuser_pre>2 and newuser_now*1.0/newuser_next>2 or\
            #   newuser_now*1.0/newuser_pre<2 and newuser_now*1.0/newuser_next<2:
            if newuser_now*1.0/newuser_pre<2 and newuser_now*1.0/newuser_next<2:
                #print newuser_pre, newuser_now, newuser_next
                df[i:i+1]['newuser_ios'].values[0] = newuser_pre -\
                        (newuser_pre - newuser_next) * (rank_pre - rank_now) /\
                        (rank_pre - rank_next)
        except Exception, e:
            print e, '从第二个以及倒数第二个开始清理异常值, 所以取到第一个和最后一个时报错'
            continue
    return df


# 多项式拟合函数
def fake_func(p, x):
    f = np.poly1d(p)
    return f(x)
# 残差函数
#regularization = 0.05
def residuals(p, y, x):
    ret = y - fake_func(p, x)
#    ret = np.append(ret, np.sqrt(regularization) * p)
    return ret
def GetOptimalCoef_(x, y, M):
    """ 输入两列数据, 寻找有限次数内曲线拟合得最好的多项式, 返回多项式的系数"""
    dict_plsq = {}
    for m in range(1, M+1):
    #if 'li' in 'limingzhi':
    #    m = M
        p0 = np.random.randn(m)
        plsq = leastsq(residuals, p0, args=(y, x))
        #print 'Fitting Parameters: ', plsq[0]
        
        sum_residuals = sum([(y1-y2)*(y1-y2) for y1,y2 in zip(y, fake_func(plsq[0], x))])
        #print '多项式次数: ', m,
        #print '差的平方和: ', sum_residuals
        dict_plsq[sum_residuals] = [m, plsq[0]]

    coef_ =  dict_plsq[min(dict_plsq.keys())][1]
    return coef_

def FittingRevised(df_rank_newuser, num_coef):
    """用多项式拟合离散数据"""
    print df_rank_newuser

    # X,Y 序列
    list_x = list(df_rank_newuser['rank'].values)
    list_y = list(df_rank_newuser['newuser_ios'].values)
    rank_newuser = zip(list_x, list_y)
    # 为了防止多项式拟合函数在起始和末尾排名过拟合
    # 我们在起始和末尾的较小的训练数据范围内另外进行多项式拟合(暂定为前100, 后200)

    # flag 标记第一个大于10,000的值, 从flag处截取排名和排名对应的数值
    flag = (i for i in list_y if i>10000).next()
    list_y_revised = list_y[list_y.index(flag):]
    list_x_revised = list_x[list_y.index(flag):]
    #print flag
    #print list_x_revised[:10]
    #print list_y_revised[:10]
    
    # 来拟合返回多项式参数
    coef_ = GetOptimalCoef_(list_x_revised, list_y_revised, num_coef)
    x_for_line = np.linspace(list_x_revised[0], list_x_revised[-1], 2*list_x_revised[-1])

    rank_start = int(list_x_revised[0])
    rank_end = int(list_x_revised[-1])
    list_fitting_rank = range(rank_start, rank_end)
    list_fitting_data = [int(round(fake_func(coef_, x))) for x in list_fitting_rank]
    print min(list_fitting_data)

#    print list_fitting_rank
#    print list_fitting_data

    plt.plot(list_x_revised, list_y_revised, 'bo', label='real')
    plt.plot(x_for_line, fake_func(coef_, x_for_line), label='Fitting')
    plt.show()

    return {'list_fitting_rank': list_fitting_rank, 'list_fitting_data': list_fitting_data} 







