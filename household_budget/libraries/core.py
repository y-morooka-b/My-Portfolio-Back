from django.http import HttpResponse
from dataclasses import dataclass
import json
import datetime
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
        return json.dumps(self.to_dict(self))

    def to_dict(self, obj):
        if isinstance(obj, dict):
            return {k: self.to_dict(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.to_dict(item) for item in obj]
        elif isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return {k: self.to_dict(v) for k, v in vars(obj).items()}
        else:
            return obj

class ServiceBase:
    def response(self, data:ResponseBase):
        """ レスポンスデータの作成 """

        res_json = data.to_json()
        logger.info(f'<response>: {res_json}')
        return HttpResponse(res_json)
