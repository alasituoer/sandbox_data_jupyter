%The text give us a demo, and give a suggestion about the useage of the
%code
%The code give a sample-demo for my data
%I find a instrument about the data-processing
%userpath('E:\talking_data\data_minning_project\nick_mi\matlab_ab');
data = load('../csv/sample.csv');
%do a call about the peakfit.m and give a interpretion about it
%�ص�����Ľ���
%data ------ ��һ��Ϊx���ڶ���Ϊy
%����center��ѡ������width/2��������width������ѡ����Ϊ��Ҫ�����ȫ�����ݼ��ĳ���
%[FitResults,GOF,baseline,coeff,residual,xi,yi,mmodel,xxx_off]=peakfit(data,160,300,2);
[FitResults,GOF,baseline,coeff,residual,xi,yi,mmodel,xxx_off]=peakfit(data, 160, 300, 2);
md = [xxx_off; mmodel];
md = md';
csvwrite('../csv/data_process.csv',md);
