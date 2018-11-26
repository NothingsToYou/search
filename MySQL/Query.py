import pymysql
import jieba
import re
import os
import math
from zhon import hanzi
from operator import attrgetter

class Tie():
    pass
class Word():
    tf,df,id,tf_idf=0,0,"",0
    def __repr__(self):
        return self.id

#根据tf_idf 排序
def sort(list_word):
    return sorted(list_word,key=attrgetter('tf_idf', 'tf_idf'),reverse=True)

#文档表的总行数
def count_rows():
    db=connect()
    cursor=db.cursor()
    sql="select count(*) from bole"
    cursor.execute(sql)
    result=cursor.fetchone()
    return result[0]

#获取关键词tf-idf
def tf_idf(tf,df):
    return tf*math.log(count_rows()/df,2)

#停词表
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

#分词
def analyze(content):
    stopList = stopwordslist(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + ("\\MySQL\\stopword.txt"))
    stopList.append(" ")

    word_list=[]
    content=re.sub(r"[%s]+" % hanzi.punctuation, "", content)
    for word in jieba.cut_for_search(content):
        if word not in stopList:
            word_list.append(word)
    return word_list

#连接mysql
def connect():
    try:
        db = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="666666",
            db="serchengine",
            charset="utf8mb4"
        )
        return db
    except BaseException as e:
        print(e)
        print("数据库连接出错")

#对查询句子进行分词  搜索每个词  求交集  返回结果
def query(word):
    db = connect()
    cursor = db.cursor()
    word_list=analyze(word)

    # word交集
    reB = []

    # 分词后查找 每个单词
    for temp_word in word_list :
        sql = "select * from title_word where word REGEXP {}{}{};".format("\"","^"+temp_word,"\"")
        cursor.execute(sql)
        result = cursor.fetchall()

        #type(word)=tuple  word[0]:单词   word[1]:df  word[2]:id
        for word in result:
            for id in re.findall("(\d,.+?)\s",word[2]):
                temp = id.split(",")
                w=Word()
                w.df=int(word[1])
                w.id=temp[-1]
                w.tf=int(temp[0])
                w.tf_idf=tf_idf(w.tf,w.df)
                reB.append(w)

    reB=sort(reB)

    result={}
    for i in reB:
        doc=query_id(i.id)
        result[doc.title]=doc.url
    return result


#返回指定id的文章
def query_id(id):
    db = connect()
    cursor = db.cursor()
    sql = "select title,url from bole where id ={}{}{};".format("\"",id,"\"")
    cursor.execute(sql)
    result = cursor.fetchone()
    tie=Tie()
    tie.title=result[0]
    tie.url=result[1]
    return tie


if __name__=="__main__":
    query('s')
    # tf_idf(1,1)

