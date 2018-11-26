import json
from django.shortcuts import render
from django.views.generic.base import View
from search.models import Bole
from django.http import HttpResponse
from elasticsearch import Elasticsearch
re_datas={}
s = Bole.search()
s = s.suggest('my_suggest', "linux", completion={
    "field":"suggest", "fuzzy":{
        "fuzziness":2
    },
    "size": 10
})
suggestions = s.execute_suggest()
for match in suggestions.my_suggest[0].options:
    source = match._source
    re_datas[source["title"]]=source["url"]

list=[]
list.append(re_datas)
print(list)
temp=json.dumps(list)
print(temp)

print(re_datas)
