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
#print(list_name_sheet)
# 选择该文件的第二张表读入
name_sheet = list_name_sheet[1]
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


# 自定义函数处理异常值
computing_outliers = function(para,window_len,n_num,interval){
	p_len = length(para)
	kd = seq(1,p_len,interval)
	last_sub = length(kd)
	if (kd[last_sub]+window_len > p_len){
		kd[last_sub] = p_len - window_len
	}	
	for (i in kd){      
		for (j in c(1:n_num)){
			outlier_n = outlier(para[i:(i+window_len)])
			md = which(para[i:(i+window_len)]==outlier_n)
			md = md+i-1
			if (md[1]==1 || md[1]==p_len){
				if(md[1]==1){
					para[md[1]] = (para[md[1]] + para[md[1]+1])/2
				}
				else{
					para[md[1]] = (para[md[1]] + para[md[1]-1])/2  
				}
			}
			else{
				para[md[1]] = (para[md[1]-1] + para[md[1]+1])/2                 
			}		
		}
	}
	para
}

model_dat = info_dat_process[1:300,]
# 模型仅采用原始数据（1500个排名）中的前300个
#model_dat = info_dat_process
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
#print(model_dat[1:10, ])

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
write.table(model_dat, file = path_to_write_file, sep = ',', row.names=TRUE, col.names=TRUE)



if(FALSE){

}


