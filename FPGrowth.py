# -*- coding: utf-8 -*-
# @Time    : 2019/10/30 17:56
# @Author  : wenlei

'''
用FPGrowth生成关联规则
'''

from config import *

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      #needs to be updated
        self.children = {}
    def inc(self, numOccur):
        self.count += numOccur
    def disp(self, ind=1):
        print('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet, minSup=1): #create FP-tree from dataset but don't mine
    freqDic = {}
    #go over dataSet twice
    for trans in dataSet: #first pass counts frequency of occurance
        for item in trans:
            freqDic[item] = freqDic.get(item, 0) + dataSet[trans]
    
    headerTable = {k:v for (k,v) in freqDic.items() if v >= minSup}


    #print 'freqItemSet: ',freqItemSet
    if len(headerTable) == 0: return None, None  #if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link
    #print 'headerTable: ',headerTable
    retTree = treeNode('Null Set', 1, None) #create tree
    for tranSet, count in dataSet.items():  #go through dataset 2nd time
        localD = {}
        for item in tranSet:  #put transaction items in order
            if headerTable.get(item,0):
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)#populate tree with ordered freq itemset
    return retTree, headerTable #return tree and header table

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:#check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count) #incrament count
    else:   #add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: #update header table
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:#call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):   #this version does not use recursion
    while (nodeToTest.nodeLink != None):    #Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode): #treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]#(sort header table)
    for basePat in bigL:  #start from bottom of header table
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #print 'finalFrequent Item: ',newFreqSet    #append to set
        if len(newFreqSet) > 1:
            freqItemList[frozenset(newFreqSet)] = headerTable[basePat][0]
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        #print 'condPattBases :',basePat, condPattBases
        #2. construct cond FP-tree from cond. pattern base
        
        myCondTree, myHead = createTree(condPattBases, minSup)
        #print 'head from conditional tree: ', myHead
        if myHead != None: #3. mine cond. FP-tree
            #print 'conditional tree for: ',newFreqSet
            #myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def loadSimpDat(inFile):
    dataSet = {}
    for line in inFile:
        line =line.strip().split(',')
        dataLine = [word for word in line if word.isdigit()]
        dataSet[frozenset(dataLine)] = dataSet.get(frozenset(dataLine),0) + 1
            
    return dataSet

if __name__ == "__main__":

    minSup = 100 #至少共同出现过100次
    print("Reading Source File ... ")
    with open(root_path+'/authors_encoded.txt','r') as f:
        dataSet = loadSimpDat(f)

    # 挖掘关联规则
    tik = time.time()
    print("Constructing FP-tree ...")
    myFPtree, myHeaderTab = createTree(dataSet, minSup)

    print("Mining frequent items ... ")
    myFreqList = {}
    mineTree(myFPtree, myHeaderTab, minSup, set([]), myFreqList)
    print("Totally %d frequent itemsets found." %len(myFreqList))
    tok=time.time()
    print('runtime:',tok-tik)

    #找到最大数目的共同合作者
    maxCoauthors = 0
    for freqAuthors in myFreqList.keys():
        if len(freqAuthors) > maxCoauthors:
            maxCoauthors = len(freqAuthors)
    print("the max num of coauthors is %d " % (maxCoauthors))

    print('Read author index...')
    with open(root_path+'/authors_index.txt','r') as authorsIndex:
        i = 0
        authorsDic = {}
        for name in authorsIndex:
            name = name.strip()
            authorsDic[i] = name
            i = i+1

    print("Writing result into result.txt...")
    with open(result_path+'/FPGrowth_result2_con.txt','w') as result2:
        with open(result_path+'/FPGrowth_result_con.txt','w') as result:
            result.write("%25s\t%25s\t%15s\t%10s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\n" \
                         %('authorA','authorB','authorC','Sup(A,B,C)','Sup(A)','Sup(B)','Sup(C)',\
                           'Con(A)','Con(B)','Con(C)','all_con','max_con','kulc','cosine','coherence'))
            result2.write("%25s\t%25s\t%15s\t%10s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\n" \
                          %('authorA','authorB','authorC','Sup(A,B,C)','Sup(A)','Sup(B)','Sup(C)',\
                            'Con(A)','Con(B)','Con(C)','all_con','max_con','kulc','cosine','coherence'))
            resultList = sorted(myFreqList.items(), key=lambda p: p[1], reverse=True)
            for itemSet, support in resultList:
                itemList = list(itemSet)
                A = itemList[0]
                authorA = authorsDic.get(int(A),'0')
                B = itemList[1]
                authorB = authorsDic.get(int(B),'0')
                SupAB_C = int(support)
                SupA = int(myHeaderTab.get(A,[0])[0])
                SupB = int(myHeaderTab.get(B,[0])[0])
                ConA = float(SupAB_C) / float(SupA)
                ConB = float(SupAB_C) / float(SupB)
                (C,authorC,SupC,ConC) = ('','',0.0,0.0)

                if len(itemList) == 3:
                    C = itemList[2]
                    authorC = authorsDic.get(int(C),'0')
                    SupC = int(myHeaderTab.get(C,[0])[0])
                    ConC = float(SupAB_C) / float(SupC)
                    #有效性分析
                    # lift = SupAB_C/(SupA*SupB*SupC)*7131572
                    cosine = np.sqrt(ConA*ConB*ConC)
                    allCon = min([ConA, ConB, ConC])
                    MaxCon = max([ConA, ConB, ConC])
                    kulc = (allCon + MaxCon) / 2
                    coherence = SupAB_C /(SupA+SupB+SupC-SupAB_C)

                elif len(itemList) == 2:
                    # 有效性分析
                    # lift = SupAB_C / (SupA * SupB ) * 7131572
                    cosine = np.sqrt(ConA * ConB)
                    allCon = min([ConA, ConB])
                    MaxCon = max([ConA, ConB])
                    kulc = (allCon + MaxCon) / 2
                    coherence = SupAB_C / (SupA + SupB - SupAB_C)

                #设置confidence阈值，进行过滤
                if allCon < 0.4 or MaxCon < 0.5 or kulc < 0.5:
                    continue

                #姓名
                result.write("%25s\t%25s\t%15s\t%10.0f\t%6.0f\t%6.0f\t%6.0f\t%6.4f\t%6.4f\t%6.4f\t%6.4f\t%6.4f\t%6.4f\t%6.4f\t%6.4f\n" \
                             %(authorA,authorB,authorC,SupAB_C,\
                               SupA,SupB,SupC,ConA,ConB,ConC,allCon,MaxCon,kulc,cosine,coherence))
                #encoded
                result2.write("%25s\t%25s\t%15s\t%10.0f\t%6.0f\t%6.0f\t%6.0f\t%6.4f\t%6.4f\t%6.4f\t%6.4f\t%6.4f\t%6.4f\t%6.4f\t%6.4f\n" \
                              %(A,B,C,SupAB_C,SupA,SupB,SupC,\
                                ConA,ConB,ConC,allCon,MaxCon,kulc,cosine,coherence))
    print("Finished !")
