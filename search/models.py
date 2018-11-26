from datetime import datetime
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class Bole(DocType):

    title = Text(analyzer="ik_max_word")
    date = Date()
    url = Keyword()
    id = Integer()
    content = Text(analyzer=ik_analyzer)
    suggest = Completion(analyzer=ik_analyzer)
    image_url = Keyword()
    image_path = Keyword()

    class Meta:
        index="lagou"
        doc_type="work"

if (__name__=="__main__"):
    Bole.init()
