# -*- coding: utf-8 -*-
# @Time    : 2019/10/30 17:56
# @Author  : wenlei

'''
从dblp.xml中得到所有文章、书、会议等的作者列表authors.txt
'''

from config import *
from xml.sax import handler, make_parser

#包含作者的标签
paper_tag = ('article','inproceedings','proceedings','book','incollection','phdthesis','mastersthesis','www')

class mHandler(handler.ContentHandler):
    def __init__(self,result):
        self.result = result
        self.flag = 0

    def startDocument(self):
        print('Document Start...')

    def endDocument(self):
        print('Document End...')

    def startElement(self, name, attrs):
        if name == 'author':
            self.flag = 1

    def endElement(self, name):
        if name == 'author':
            self.result.write(',')
            self.flag = 0
        if (name in paper_tag) :
            self.result.write('\r\n')

    def characters(self, chrs):                                 # [8]
        if self.flag:
            self.result.write(chrs)

def parserDblpXml(source,result):
    handler = mHandler(result)
    parser = make_parser()
    parser.setContentHandler(handler)

    parser.parse(source)


if __name__ == '__main__':
    source = codecs.open(root_path+'/dblp.xml','r','utf-8')
    result = codecs.open(root_path+'/authors.txt','w','utf-8')
    parserDblpXml(source,result)
    result.close()
    source.close()
