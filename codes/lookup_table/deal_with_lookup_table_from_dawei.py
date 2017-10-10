#coding:utf-8
import pandas as pd

path_lookup_table_from_dawei = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/lookup_table_from_dawei/'

# Input the lookup table of Productid and Chinese Name defined by the developer
df_prod_info = pd.read_csv(path_lookup_table_from_dawei + 'product_basic_info.csv')
df_prod_info.columns =\
        ['Product Id', 'Product Name', 'Product Type', 'Platform Id',]
#print df_prod_info.head()

# select the lookup table of apps of the platform android
df_prod_info_android = df_prod_info[df_prod_info['Platform Id']==1]
df_lookup_table_android = df_prod_info_android[['Product Id', 'Product Name',]]
df_lookup_table_android.index = df_lookup_table_android['Product Id']
del df_lookup_table_android['Product Id']
#print df_lookup_table_android[:10]

# select the lookup table of apps included in the platform ios
df_prod_info_ios = df_prod_info[df_prod_info['Platform Id']==2]
df_lookup_table_ios = df_prod_info_ios[['Product Id', 'Product Name',]]
df_lookup_table_ios.index = df_lookup_table_ios['Product Id']
del df_lookup_table_ios['Product Id']
#print df_lookup_table_ios[:10]


print df_lookup_table_ios

"""
for pid in [3206653, 3206643,]:
    try:
        pname = df_lookup_table_ios.ix[pid]
    except Exception, e:
        print e, '\t', pid
    print pid, pname
""""





