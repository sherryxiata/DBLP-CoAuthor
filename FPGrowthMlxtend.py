# -*- coding: utf-8 -*-
# @Time    : 2019/10/31 8:53
# @Author  : wenlei

'''
用mlxtend的FPGrowth包实现
'''


from config import *
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules

# data = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

if __name__ == '__main__':
    dataLen = 10000
    minSup = 10
    min_con = 0.5

    print('loading the dataset...')
    with open(root_path + '/authors_encoded.txt', 'r') as f:
        f_lines = list(line for line in (l.strip() for l in f) if line)  # 去除空行
        dataSet = loadData(f_lines)

    data = dataSet[0:dataLen]

    print('change the format to one-hot...')
    #转化为One-Hot编码
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    # df = pd.SparseDataFrame(te_ary, columns=te.columns_)
    te_len = te_ary.shape[0]
    print('change format end')

    print('start mining...')
    #进行挖掘
    tik=time.time()
    print('generate frequent_itemsets...')
    frequent_itemsets = fpgrowth(df, min_support=minSup/te_len, use_colnames=True)
    tok = time.time()
    print('runtime:',tok-tik)

    print('generate rules...')
    rules = association_rules(frequent_itemsets, min_threshold=min_con)

    print('mining finished!')

    # print('Read author index...')
    # with open(root_path + '/authors_index.txt', 'r') as authorsIndex:
    #     i = 0
    #     authorsDic = {}
    #     for name in authorsIndex:
    #         name = name.strip()
    #         authorsDic[i] = name
    #         i = i + 1
    #
    # print("Writing result into result.txt...")
    #
    # ant_author = []
    # con_author = []
    #
    # for index, row in rules.iterrows():
    #     a_list = []
    #     c_list = []
    #
    #     antecedents = row['antecedents']
    #     consequents = row['consequents']
    #     for a in antecedents:
    #         authorA = authorsDic.get(int(a), '0')
    #         a_list.append(authorA)
    #     ant_author.append(a_list)
    #
    #     for c in consequents:
    #         authorC = authorsDic.get(int(c), '0')
    #         c_list.append(authorC)
    #     con_author.append(c_list)
    #
    # rules['ant_author'] = ant_author
    # rules['con_author'] = con_author
    #
    # rules.to_csv(
    #     result_path + '/FPGrowth(Mlxtend)_result_' + str(dataLen) + '_' + str(minSup) + '_' + str(min_con) + '.csv',
    #     index=False)

