import os
import sys
import re 
import pickle
import math
import pprint
rootdir=os.getcwd()
titleDic={}
Dicindex=[]
wordDic={}
docVector=[]
norm_list = []
stopset = set()
query_dict = {}
query_list = []

#下列两个函数均用于离线处理
#建立停用词集合
def createStopWordList():
    fp = rootdir +'\\'+ 'stopword.txt'
    curr_f = open(fp,'r')
    stopline = curr_f.read()
    stopword = stopline.split('\n')
    for x in stopword:
        stopset.add(x)

#建立带tf的倒排索引
def createIndex():
    files = os.listdir(rootdir+'\ArchiveTxt')
    for i,f in enumerate(files):
        titleDic[i]=f
        docVector.append([])
        Dicindex.append(f)
        curr_path = rootdir +'\\ArchiveTxt\\'+ f 
        curr_file = open(curr_path,'r')
        allLines = curr_file.read()
        curr_line = allLines.split('\n')
        wordSet = set()
        tmplist = {}
        tfValue = 0
        for index,val in enumerate(curr_line):
            #标题的权重                
            if index == 0:
                tfValue = 10000
            #摘要的权重
            if val == 'abstract' or val == 'H I G H L I G H T S':
                tfValue = 200
                continue
            #正文的权重
            if val == '1. Introduction':
                tfValue = 1
                continue

            word = re.split(r'[:;,.!\(\)\'\[\]\s+\-\?\/\d+\–\“\”\>\<\{\|\=]', val)
            for m in word:
                if m != '':
                    m = m.lower()
                    if m not in stopset:
                        if m not in wordSet:
                            tmplist[m]={'tf':0,'tfw':0}
                            wordDic.setdefault(m,[]).append(i)
                            tmplist[m]['tf'] += tfValue
                        else :
                            tmplist[m]['tf'] += tfValue
                        wordSet.add(m)
                    else:
                        continue     
        docVector[i].append(tmplist)
    for _ in docVector:
        for j in _[0]:
            if _[0][j]['tf'] != 1:
                _[0][j]['tfw'] = math.log(_[0][j]['tf'])+1.0
            else :
                _[0][j]['tfw'] = 1.0
    #余弦归一化
    for i,v in enumerate(docVector):
        norm_list.append(getNorm(i))

    #写入文件备用
    dict_file = open('wordDic.pkl','wb')
    pickle.dump(wordDic,dict_file)
    dict_file = open('titleDic.pkl','wb')
    pickle.dump(titleDic,dict_file)
    dict_file = open('Dicindex.pkl','wb')
    pickle.dump(Dicindex,dict_file)
    dict_file = open('docVector.pkl','wb')
    pickle.dump(docVector,dict_file)
    dict_file = open('norm_list.pkl','wb')
    pickle.dump(norm_list,dict_file)
    dict_file = open('stopset.pkl','wb')
    pickle.dump(stopset,dict_file)  

#余弦归一化
def getNorm(x):
    norm = 0
    for _ in docVector[x][0]:
        norm += docVector[x][0][_]['tfw']*docVector[x][0][_]['tfw']    
    norm = math.sqrt(norm)
    return norm

def getPickles():
    global norm_list
    global titleDic
    global wordDic
    global Dicindex
    global docVector
    pkl_file = open('norm_list.pkl','rb')
    norm_list = pickle.load(pkl_file)
    pkl_file = open('titleDic.pkl','rb')
    titleDic = pickle.load(pkl_file)
    pkl_file = open('wordDic.pkl','rb')
    wordDic = pickle.load(pkl_file)
    pkl_file = open('Dicindex.pkl','rb')
    Dicindex = pickle.load(pkl_file)
    pkl_file = open('docVector.pkl','rb')
    docVector = pickle.load(pkl_file)

#查询的tf-idf计算
def get_query(input_str):
    getPickles()
    global query_list
    query_list = input_str.split(' ')
    #pprint.pprint(query_list)
    queryset=set()
    for _ in query_list:
        if _ != '':
            if _ not in queryset:
                cur_df = len(wordDic[_])
                cur_idf = math.log(len(Dicindex))-math.log(cur_df)
                global query_dict
                query_dict.setdefault(_,{})
                query_dict[_]={'tf':1,'idf':cur_idf}
            else:
                query_dict[_]['tf'] +=1

#余弦相似度计算
def get_cosSimilarity(s):
    score = []
    #s = "boundary layer determination"
    get_query(s)
    for index,val in enumerate(docVector):
        summ = 0
        wdset = set()
        for _ in val[0]:
            wdset.add(_)
        cur_intersect = list(set(query_list)& set(wdset))
        for j in cur_intersect:
            if len(cur_intersect)!=0:
                wq = query_dict[j]['tf']*query_dict[j]['idf']
                wd = val[0][j]['tf']
                summ +=wq*wd
            else: 
                summ = 0
                break
        summ /= norm_list[index]
        score.append({'index':index,'grade':summ})
    score.sort(key=lambda x:(x['grade']),reverse = True)
    #pprint.pprint(score)
    return score

#根据结果返回相关的论文
def getResult(s):
    t_list = get_cosSimilarity(s)
    result_list = []
    for _ in range(len(t_list)):
        if t_list[_]['grade'] > 0.0:
            docid = t_list[_]['index']
            result_list.append(Dicindex[docid])
    return result_list
    
       
if __name__ == '__main__':
    # createStopWordList()
    # createIndex()   
        
    # pkl_file = open('norm_list.pkl','rb')
    # norm_list = pickle.load(pkl_file)
    # pkl_file = open('titleDic.pkl','rb')
    # titleDic = pickle.load(pkl_file)
    # pkl_file = open('wordDic.pkl','rb')
    # wordDic = pickle.load(pkl_file)
    # pkl_file = open('Dicindex.pkl','rb')
    # Dicindex = pickle.load(pkl_file)
    # pkl_file = open('docVector.pkl','rb')
    # docVector = pickle.load(pkl_file)    
    str_ = "robust bayesian"
    getResult(str_)
    # for _ in docVector:
    #     print(_[0])
    # print(rootdir)