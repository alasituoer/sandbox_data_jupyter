#coding:utf-8

path_source_file = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/lookup_table_from_dawei/'
path_to_write = '/Users/Alas/Documents/TD/iOS_Rank_Estimated_Model_V1/jupyter_sandbox_data/lookup_table_from_dawei/'
with open(path_to_write + 'product_basic_info_revised.txt', 'wb') as f1:
    with open(path_source_file + 'product_basic_info_v0.csv', 'r') as f2:
        for line in f2.readlines():
        #if 'li' in 'limingzhi':
            #line = f2.readline()
            #line = f2.readline()
            productid, product_name, product_type, platform =\
                    [strs.strip().replace('"', '') for strs in line.split('","')]
            #print [productid,]
            #print [product_name,]
            #print [product_type,]
            #print [platform,]

            product_name = product_name.replace(',', ' ').replace('，', ' ').replace("'",\
                    ' ').replace("’", ' ').replace('"', ' ').replace('”', ' ').replace(';', ' ')
            to_write_strings = productid + ',' + product_name + ',' +\
                    product_type + ',' + platform + '\n'
            #to_write_strings = product_name + '\n'
            #print to_write_strings
            f1.write(to_write_strings)





