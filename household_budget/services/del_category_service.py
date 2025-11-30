from django.db import transaction
from django.http import HttpResponse
from household_budget.libraries.core import RequestBase, ResponseBase, ServiceBase
from household_budget.models import Categories

import logging

logger = logging.getLogger()

class RequestDelCategory(RequestBase):
    """
    del_category のリクエストデータクラス
    """
    id: int

    def __init__(self, id:int):
        self.id = id

class ResponseDelCategory(ResponseBase):
    """
    del_category のレスポンスデータクラス
    """
    success: bool

    def __init__(self, success):
        self.success = success

class DelCategoryService(ServiceBase):
    """
    del_category のメイン処理を担当する
    """

    request: RequestDelCategory

    def __init__(self, request: RequestDelCategory):
        self.request = request

    def main_process(self) -> HttpResponse:
        try:
            return self.__process()
        except Exception as e:
            logger.error(f'<DelCategoryService.main_process>: {e}')
            return HttpResponse(e)

    def __process(self) -> HttpResponse:
        with transaction.atomic():
            Categories.objects.filter(id=self.request.id).delete()

        res = ResponseDelCategory(True)
        return self.response(res)
