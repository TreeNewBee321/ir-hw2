#!/usr/bin/env python
# encoding: utf-8


import sys
import os
import io
import importlib
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

'''
 解析pdf 文本，保存到txt文件中
'''
def parse(path,raw_path):
    fp = open(path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(r'D:/大三/信息检索/作业/VSM/ArchiveTxt/'+raw_path+r'.txt', 'a') as f:
                        results = x.get_text().encode("GBK", 'ignore')
                        f.write(results.decode("GBK")+'\n')
                        
def convertPDF():
    root = "D:/大三/信息检索/作业/VSM/Articles"
    pdfs = os.listdir(root)
    for i,pdf in enumerate(pdfs):
        print(pdf)
        curr_pdf = root+'/'+pdf
        print(curr_pdf)
        parse(curr_pdf,pdf)
if __name__ == '__main__':
    parse('D:/大三/信息检索/作业/VSM/Articles/Water-desalination-using-visible-light-by-disperse-red-1-modi_2017_Desalinat.pdf','Water-desalination-using-visible-light-by-disperse-red-1-modi_2017_Desalinat.pdf')
    #convertPDF()