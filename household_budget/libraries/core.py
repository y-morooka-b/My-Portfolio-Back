from django.http import HttpResponse
from dataclasses import dataclass, asdict
import json
import logging

logger = logging.getLogger()

class RequestBase:
    def __init__(self, **kwargs):
        logger.info(f'<request>: {self.__dict__}')

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

@dataclass
class ResponseBase:
    def to_json(self):
        """ json文字列にシリアライズ """
        return json.dumps(asdict(self))

class ServiceBase:
    def response(self, data:ResponseBase):
        """ レスポンスデータの作成 """

        res_json = data.to_json()
        logger.info(f'<response>: {res_json}')
        return HttpResponse(res_json)
