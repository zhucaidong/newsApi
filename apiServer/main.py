
from sanic import Sanic
from sanic.response import json
from db.MongoHelp import MongoHelper as SqlHelper

class apiNews:
    def __init__(self):
        self.sqlhelper = SqlHelper()

    def queryNews(self,category,pz,page,db_name):
        self.sqlhelper.init_db(db_name)
        newsJson = self.sqlhelper.select(pz,{'category':category},page)
        self.sqlhelper.close_client()
        return newsJson
apiNews=apiNews()
app = Sanic(__name__)
@app.route("/news",methods=['GET'])
async def get_handler(request):
    parameter = request.args
    return json({"news":apiNews.queryNews(parameter['category'][0],parameter['pageSize'][0],parameter['page'][0],'baiduNews')})
@app.route("/wx",methods=['GET'])
async def get_handler(request):
    parameter = request.args
    return json({"wx":apiNews.queryNews(parameter['category'][0],parameter['pageSize'][0],parameter['page'][0],'weixin')})

app.run(host="0.0.0.0", port=80, debug=True)
