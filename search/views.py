import json
import MySQL.mongodb as mongo
from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import render
import time

#返回搜索建议
class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s','')
        print(key_words)
        if key_words:
            #返回建议 字典
            # re_datas=self.get_dataByElasticSearch(key_words)
            # re_datas=self.get_dataByMysql(key_words)
            re_datas=mongo.query(key_words)

            return HttpResponse(json.dumps(re_datas), content_type="application/json")
        return HttpResponse(json.dumps({}), content_type="application/json")

class SearchView(View):
    def get(self, request):
        key_words = request.GET.get("q","")
        print(key_words,"wordword")
        start=time.clock()
        dict_list=mongo.find(key_words)
        total_nums=len(dict_list)
        end=time.clock()
        return render(request, "result.html", {"page":1,
                                               "all_hits":dict_list,
                                               "key_words":key_words,
                                               "total_nums":total_nums,
                                               "page_nums":10,
                                               "last_seconds":end-start,
                                               "jobbole_count":"asdf",
                                               "topn_search":"asdf"})



