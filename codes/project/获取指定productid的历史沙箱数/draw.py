#coding:utf-8
import pandas as pd
from bokeh.plotting import figure, output_file, show

working_space = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/project/获取指定ProductID的沙箱活新增或活跃值/'

path_file = working_space + 're.txt'

df = pd.read_csv(path_file, names=['ProductID', 'Date', 'Type', 'Value',])
print df.head()

df_active = df[df['Type']=='active_android']
df_newuser = df[df['Type']=='newuser_android']
print df_active.head()
print df_newuser.head()

x = range(len(df_active['Date'].values))
y = list(df_active['Value'].values)

output_file('draw.html')

p = figure(title='sample', x_axis_label='date', y_axis_label='value')
p.line(x, y, legend ='trend', line_width=2)
#show(p)

