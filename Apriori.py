from config import *
import random

# C1 是大小为1的所有候选项集的集合
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item]) #store all the item unrepeatly

    C1.sort()
    #return map(frozenset, C1)#frozen set, user can't change it.
    return list(map(frozenset, C1))

#该函数用于从 C1 生成 L1 。
def scanD(D,Ck,minSupport):
#参数：数据集、候选项集列表 Ck以及感兴趣项集的最小支持度 minSupport
    ssCnt={}
    for tid in D:#遍历数据集
        for can in Ck:#遍历候选项
            if can.issubset(tid):#判断候选项中是否含数据集的各项
                #if not ssCnt.has_key(can): # python3 can not support
                if not can in ssCnt:
                    ssCnt[can]=1 #不含设为1
                else: ssCnt[can]+=1#有则计数加1
    # numItems=float(len(D))#数据集大小
    retList = []#L1初始化
    supportData = {}#记录候选项中各个数据的支持度
    for key in ssCnt:
        support = ssCnt[key]#计算支持度
        if support >= minSupport:
            retList.insert(0,key)#满足条件加入L1中
        supportData[key] = support
    return retList, supportData

#total apriori
def aprioriGen(Lk, k): #组合，向上合并
    #creates Ck 参数：频繁项集列表 Lk 与项集元素个数 k
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): #两两组合遍历
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2: #若两个集合的前k-2个项相同时,则将两个集合合并
                retList.append(Lk[i] | Lk[j]) #set union
    return retList

#apriori
def apriori(dataSet, minSupport = 100):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet)) #python3
    L1, supportData = scanD(D, C1, minSupport)#单项最小支持度判断 0.5，生成L1
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):#创建包含更大项集的更大列表,直到下一个大的项集为空
        Ck = aprioriGen(L[k-2], k)#Ck
        Lk, supK = scanD(D, Ck, minSupport)#get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

#生成关联规则
def generateRules(L, supportData, minConf=0.7):
    #频繁项集列表、包含那些频繁项集支持数据的字典、最小可信度阈值
    bigRuleList = [] #存储所有的关联规则
    for i in range(1, len(L)):  #只获取有两个或者更多集合的项目，从1,即第二个元素开始，L[0]是单个元素的
        # 两个及以上的才可能有关联一说，单个元素的项集不存在关联问题
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            #该函数遍历L中的每一个频繁项集并对每个频繁项集创建只包含单个元素集合的列表H1
            if (i > 1):
            #如果频繁项集元素数目超过2,那么会考虑对它做进一步的合并
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:#第一层时，后件数为1
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)# 调用函数2
    return bigRuleList

#生成候选规则集合：计算规则的可信度以及找到满足最小可信度要求的规则
def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    #针对项集中只有两个元素时，计算可信度
    prunedH = []#返回一个满足最小可信度要求的规则列表
    for conseq in H:#后件，遍历 H中的所有项集并计算它们的可信度值
        conf = supportData[freqSet]/supportData[freqSet-conseq] #可信度计算，结合支持度数据
        if conf >= minConf:
            print (freqSet-conseq,'-->',conseq,'conf:',conf)
            #如果某条规则满足最小可信度值,那么将这些规则输出到屏幕显示
            brl.append((freqSet-conseq, conseq, conf))#添加到规则里，brl 是前面通过检查的 bigRuleList
            prunedH.append(conseq)#同样需要放入列表到后面检查
    return prunedH

#合并
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    #参数:一个是频繁项集,另一个是可以出现在规则右部的元素列表 H
    m = len(H[0])
    if (len(freqSet) > (m + 1)): #频繁项集元素数目大于单个集合的元素数
        Hmp1 = aprioriGen(H, m+1)#存在不同顺序、元素相同的集合，合并具有相同部分的集合
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)#计算可信度
        if (len(Hmp1) > 1):    #满足最小可信度要求的规则列表多于1,则递归
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

if __name__ == '__main__':
    # dataSet=[[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    print('loading the dataset...')
    with open(root_path+'/authors_encoded.txt','r') as f:
        f_lines = list(line for line in (l.strip() for l in f) if line) #去除空行
        dataSet = loadData(f_lines)

    #700w条跑了很久很久
    #取10000条
    sample=dataSet[0:10000]

    print('start mining...')

    #生成频繁项集
    print('generate frequent_itemsets...')
    tik = time.time()
    L,supportData=apriori(sample,10)
    tok = time.time()
    print('runtime:', tok - tik)

    #生成关联规则
    print('generate rules...')
    rules=generateRules(L,supportData,0.5)

    print('mining finished!')




