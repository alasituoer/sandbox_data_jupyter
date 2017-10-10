library(readxl)
library(outliers)
library(mclust)

# 从 data_process 中读入估计预测排名和对应的新增用户数(可能有多个)
# 所以下面的功能，先是简单的将排名唯一化, 多个排名位最终取中位数作为排名对应的新增用户数
dat_predict <- read.csv("../csv/project/V4-new_user_free_rank/data_process.csv",header = FALSE)
names(dat_predict) <- c("rank", "num")
#print(dat_predict)

# 读入deal_with_ios_free_rank.r中生成的model_dat
# 比重现当时的工作空间方便
model_dat = read.csv("../csv/project/V4-new_user_free_rank/model_dat.csv")
print(model_dat[1:10, ])


# 对排名值向下取整(取不大于该值的最大整数)
rank_n <- floor(dat_predict$rank)
# 将上述取整后的排名值添加列到data_predict之后
dat_predict <- cbind(dat_predict,rank_n)
print(dat_predict[1:20, ])
# 对取整后的排名值去重
interator_c <- unique(dat_predict$rank_n)

# 初始化 new and new_dat_predict 为一行两列的矩阵
new <- as.data.frame(list(rank_n = 1, num = 15))
new_dat_predict <- as.data.frame(list(rank_n = 1,num = 15))
#for (i in interator_c[1:20]){
for (i in interator_c){
        kd <- which(dat_predict$rank_n == i)
	# 选择排名相同值的中位数作为新排名的值
        km_mid <- median(dat_predict[kd,]$num)
	#print(dat_predict[kd,]$num)
	#print(km_mid)
        new$rank_n <- i
        new$num <- km_mid
        new_dat_predict <- rbind(new_dat_predict, new)
}
#print(new_dat_predict[1:10, ])
#print(new_dat_predict)


kd <- dim(new_dat_predict)
# 去掉初始化 new_dat_predict 在第一行写入的默认记录
new_dat_predict <- new_dat_predict[2:kd[1],]
print(new_dat_predict[1:10, ])

# 计算model_dat中异常点(若test_pare与sum_mean相等, 改点为异常点)的比例
#print(which(model_dat$test_para==model_dat$sum_mean))
#print(dim(model_dat)[1])
outliers_ratio <- sum(which(model_dat$test_para==model_dat$sum_mean))/dim(model_dat)[1]
#print(outliers_ratio)

if (FALSE){
# 得到新预测排名的最小排名
min_num <- min(new_dat_predict$rank_n)
md <- which(model_dat$rank_total==min_num)[1]
# 最小排名前的用默认平滑处理过的test_para值代替
predict_vector <- model_dat$test_para[1:(md-1)]
#print(predict_vector)
# 得到最新的预测排名下的值
predict_vector <- append(predict_vector,new_dat_predict$num)
#print(predict_vector)

model_dat <- cbind(model_dat,predict_vector)
print(model_dat[1:20, ])


wd <- model_dat$test_para - model_dat$predict_vector
hist(wd)

probility_search <- function(dat,pro,stepp){
        mean_std <- mean(dat)
        n <- 1
        upper <- 0.1
        lower <- 0.1
        probility <- 0
        total_len <- length(dat)
        while(probility < pro){
                up <- mean_std+n*stepp
                low <- mean_std - n*stepp
                probility <- length(which(dat <= up & dat > low))/total_len
                n <- n+1
        }
        upper <- mean_std + (n-1)*stepp
        lower <- mean_std - (n-1)*stepp
        kd <- as.data.frame(list(pro = probility,up = upper,low = lower))
        kd
}

kdd <- probility_search(wd, 0.8, 300)
#print(kdd)

write.csv(model_dat, "../csv/final_computing.csv", row.names=FALSE)
write.csv(kdd, "../csv/predict_error.csv")






}
