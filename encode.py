# -*- coding: utf-8 -*-
# @Time    : 2019/10/30 17:56
# @Author  : wenlei

'''
对authors.txt进行编码，生成authors_encoded.txt和authors_index.txt
'''

from config import *

source = codecs.open(root_path+'/authors.txt','r','utf-8')
result = codecs.open(root_path+'/authors_encoded.txt','w','utf-8')
index = codecs.open(root_path+'/authors_index.txt','w','utf-8')
index_dic = {}   #{authorName:[id,count],...,}
name_id = 0

for line in source:
    name_list = line.split(',')
    for name in name_list:
        if not (name == '\r\n'):
            if name in index_dic:
                index_dic[name][1] +=1  #count+1
            else:
                index_dic[name] = [name_id,1]
                index.write(name + u'\r\n')  #write to author_index.txt
                name_id += 1
            result.write(str(index_dic[name][0]) + u',') #write encoded line to authors_encoded.txt
    result.write('\r\n')  #start a new encoded line

source.close()
result.close()
index.close()
