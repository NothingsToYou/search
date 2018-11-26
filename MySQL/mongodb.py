import pymongo
import re
import math
import numpy as np
import pandas as pd
import time
from django.conf import settings

def count_rows():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["bole"]
    mycol=mydb["bole"]
    return mycol.find().count()
ROWS=count_rows()


class Word():
    id,tf_idf="",0

    def tf_idf(self,tf,df):
        return tf*math.log(count_rows()/df,2)
    def __repr__(self):
        return self.id
    def __init__(self,dict):
        print(dict)
        id=dict["id"]
        tf_idf=self.tf_idf(dict["times"],dict["df"])


def query(word):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["bole"]
    mycol_doc = mydb["bole"]
    mycol_word = mydb["title_word"]
    temp=re.compile("^"+word,re.IGNORECASE)

    ads=mycol_word.find({"word":temp})

    if(ads.count()):
        Df=pd.DataFrame()
        for i in ads:
            dataframe=pd.DataFrame(i["doc"])
            df=dataframe["id"].count()
            dataframe["tf_idf"]=dataframe["times"].map(lambda x:x*math.log(ROWS/df,2))
            Df=pd.concat([Df,dataframe],axis=0,ignore_index=True)

        temp=Df.groupby("id",as_index=False)["tf_idf"].sum()


        temp=temp.sort_values(by="tf_idf",ascending=False)
        temp=temp.reset_index(drop=True)
        if(len(temp)>5):
            temp=temp[:5]
        temp=temp.set_index("id").to_dict()
        print(temp["tf_idf"])

        return query_id(temp["tf_idf"].keys(),mycol_doc)

    else:return {}

def find(word):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["bole"]
    mycol_doc = mydb["bole"]
    mycol_word = mydb["title_word"]
    temp = re.compile("^" + word, re.IGNORECASE)

    ads = mycol_word.find({"word": temp})

    if (ads.count()):
        Df = pd.DataFrame()
        for i in ads:
            dataframe = pd.DataFrame(i["doc"])
            df = dataframe["id"].count()
            dataframe["tf_idf"] = dataframe["times"].map(lambda x: x * math.log(ROWS / df, 2))
            Df = pd.concat([Df, dataframe], axis=0, ignore_index=True)

        temp = Df.groupby("id", as_index=False)["tf_idf"].sum()

        temp = temp.sort_values(by="tf_idf", ascending=False)
        temp = temp.reset_index(drop=True)
        if (len(temp) > 5):
            temp = temp[:5]
        temp = temp.set_index("id").to_dict()
        # print(temp["tf_idf"])
        # print(find_id(temp["tf_idf"], mycol_doc))

        return(find_id(temp["tf_idf"], mycol_doc))


    else:
        return []
def query_id(id_list,mongo_doc):
    result=dict()
    for id in id_list:
        doc=mongo_doc.find_one({"_id": id})
        temp={}
        temp[doc["title"]]=doc["url"]
        result=dict(result,**temp)
    print(result)
    return result

def find_id(id_list,mongo_doc):
    esult =[]
    for id,score in id_list.items():
        doc = mongo_doc.find_one({"_id": id})
        esult.append(dict(doc,**{"score":score}))
    return esult

if __name__=="__main__":
    s=time.clock()
    find("linux")
    e=time.clock()
    print(e-s)
