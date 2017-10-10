library(readxl)
library(outliers)
library(mclust)

# 指定文件路径
path_source_file = '../source_files/ios_free_rank.xlsx'
# 得到处理文件名(含文件类型和不含文件类型)
name_source_file_with_filetype = strsplit(path_source_file, split="/")[[1]][3]
#print(name_source_file_with_filetype)
name_source_file = strsplit(name_source_file_with_filetype, split=".xlsx")[[1]][1]
# 得到该文件中的表名列表
list_name_sheet = excel_sheets(path_source_file)
print(list_name_sheet)
# 选择该文件的第二张表读入
name_sheet = list_name_sheet[2]
print(name_sheet)

dat = read_excel(path_source_file, sheet=name_sheet)
#print(dat[213:217, 2])



# 处理缺失值为0
md = dim(dat)
for (i in c(2:md[2])){
    k = which(is.na(dat[i]))
    dat[k,i]=0
}
#print(dat[1:10, 1:5])

# print(dim(dat)) 返回数组的（行数、列数、向量个数）
# 取第二个代表所有记录数 1501列（个排名）
number_columns = dim(dat)[2]
#print(number_columns)
# 初始化排名值: 1, 2, .., 1500 # 应用的总体收入
# 初始化应用的平均收入	# 初始化应用的中位数收入
rank_total = c(1:(number_columns-1)) 
sum_total = rep(0,(number_columns-1))
sum_mean = rep(0,(number_columns-1))
sum_median = rep(0,(number_columns-1))
#print(class(rank_total))
#print(rank_total[10])
#print(sum_total)

for (i in c(2:number_columns)){
	# 返回值不等于0的列表
	kd = which(dat[,i]!=0)
	# 依次计算每个排名的历史每天排名的总收入、平均收入和中位数收入
	sum_total[i-1] = sum(dat[,i])
	sum_mean[i-1] = mean(dat[kd,i])	
	sum_median[i-1] = median(dat[kd,i])
}
mc <- which(is.na(sum_mean))
sum_mean[mc]<-0

# 将上述计算得到的排名、收入总和、平均收入、中位数收入 合并成一个DataFrame结构
# 便于后面调用
info_dat_process = as.data.frame(list(rank_total = rank_total, sum_total=sum_total, sum_mean=sum_mean, sum_median=sum_median))
#print(info_dat_process[c(1:10), ])


# 自定义函数处理一组数据(20个)中的异常值(为相连两项的平均值, 如果是收尾元素则特别对待)
# computing_outliers(model_dat$sum_mean, window_len=20, n_num=10, interval=5)
computing_outliers = function(para,window_len,n_num,interval){
	# 得到para数组的长度p_len
	p_len = length(para)
	# 指定interval间隔, 起始是1, 终点是p_len, 得到间隔数组kd
	kd = seq(1,p_len,interval)
	# 得到间隔数组的长度
	last_sub = length(kd)

	# 每间隔interval(5)个作为起始排名, 连续选择window_len(20)个进行异常值处理
	# 如果间隔数组的最后一个数字加参数window_len超出输入数组长度,
	# 则不用管倒数一二位的间隔, 最后一组的起始排名改变为输入数组的倒数第20位
	# 即最后20个排名作为一组, 保证所有的排名都会分到一个组, 且每组有20个排名
	if (kd[last_sub]+window_len > p_len){
		kd[last_sub] = p_len - window_len
	}

	# kd :1, 6, 11, 
	for (i in kd){      
		# 循环n_num次
		for (j in c(1:n_num)){
			# function outlier():
			# 
			outlier_n = outlier(para[i:(i+window_len)])
			# 反推异常值的位置
			md = which(para[i:(i+window_len)]==outlier_n)
			md = md+i-1
			# 返回的位置可能有多个, 只取第一个
			if (md[1]==1 || md[1]==p_len){
				# 如果返回的异常值是组内的第一个
				# 那么重置它的值为第一第二的的平均值
				if(md[1]==1){
					para[md[1]] = (para[md[1]] + para[md[1]+1])/2
				}
				# 如果返回的异常值是组内的最后一个
				# 那么重置它的值为倒数第一第二的的平均值
				else{
					para[md[1]] = (para[md[1]] + para[md[1]-1])/2  
				}
			}
			# 如果不是上述的首尾部分
			# 那么重置为相连前后值的平均
			else{
				para[md[1]] = (para[md[1]-1] + para[md[1]+1])/2                 
			}		
		}
	}
	para
}

if (FALSE){
model_dat = info_dat_process#[1:300,]
#print(model_dat$sum_mean)
window_len = 20
interval = 5
para = model_dat$sum_mean
para_len = length(para)
kd = seq(1, para_len, interval)
kd_len = length(kd)

if(kd[kd_len] + window_len > para_len){
    kd[kd_len] = para_len - window_len
}
#print(kd)

#kd = [1, 6, 11, 16, 21   26   31   36   41   46   51   56   61   66   71
#76   81   86   91   96  101  106  111  116  121  126  131  136  141  146
# ...
#1351 1356 1361 1366 1371 1376 1381 1386 1391 1396 1401 1406 1411 1416 1421
#1426 1431 1436 1441 1446 1451 1456 1461 1466 1471 1476 1481 1486, 1491, 1480,]

for (i in kd[100:100]){
    print(para[i:(i+window_len)])
    outlier_n = outlier(para[i:(i+window_len)])
    print(i)
    print(outlier_n)

    md = which(para[i:(i+window_len)]==outlier_n)
    md = md+i-1
    print(md)
    print(md[1])}

}



# 模型仅采用原始数据（1500个排名）中的前300个
model_dat = info_dat_process
#model_dat = info_dat_process[300:600,]
#print(model_dat[1:10, ])
# 选择model_dat中的一列sum_total作为函数输入
test_para = computing_outliers(model_dat$sum_mean, window_len=20, n_num=10, interval=5)
#print(test_para)


# 得到 model_dat 的行列数元组
#dim_matrix = dim(model_dat)
# 去掉之前添加的 fill_num 列
#model_dat = model_dat[1:(dim_matrix[2]-1)]
#print(model_dat[1:10, ])
# 将生成的 rest_para列添加到model_dat后面
model_dat = cbind(model_dat,test_para)
print(model_dat[1:20, ])

if (FALSE){
#下面的聚类分析, 仅是用于展示绘图?
cluster_label = Mclust(test_para)
gaussian_matrix = as.data.frame(list(var_l=c(1:length(test_para)), para=test_para, cluster=map(cluster_label$z)))
#print(gaussian_matrix)
# 得到的图形保存在当前路径下 文件名是Rplots.pdf
plot(gaussian_matrix$var_l, gaussian_matrix$para)


#path_to_write_file = paste('../csv/', name_source_file, '_', name_sheet, '_sample.csv', sep = '')
path_to_write_file = '../csv/sample.csv'
# 仅将 model_dat 的第一列的rank和第五列的test_para存入'sample.csv'
write.table(model_dat[c(1, 5)], file = path_to_write_file, sep = ',', row.names=FALSE, col.names=FALSE)

path_to_write_file = '../csv/model_dat.csv'
write.table(model_dat, file = path_to_write_file, sep = ',', row.names=FALSE, col.names=TRUE)


}

