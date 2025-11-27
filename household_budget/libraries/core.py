import json
from django.http import HttpResponse
import logging

logger = logging.getLogger()

class ResponseBase:
    def to_json(self):
        """ json文字列にシリアライズ """
        return json.dumps(self.__dict__, ensure_ascii=False)

def response(data:ResponseBase):
    """ レスポンスデータの作成 """

    res_json = data.to_json()
    logger.info(f'<response>: {res_json}')
    return HttpResponse(res_json)
