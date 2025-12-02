from django.http import HttpResponse
from django.db import transaction
from household_budget.libraries.core import ServiceBase, ResponseBase, RequestBase
from household_budget.models import Categories

import logging

logger = logging.getLogger()

class RequestSetCategory(RequestBase):
    """
    set_category のリクエストデータクラス
    """
    name: str
    type: int

    def __init__(self, name: str, type: int):
        self.name = name
        self.type = type
        super().__init__()

class ResponseSetCategory(ResponseBase):
    """
    set_category のレスポンスデータクラス
    """
    success: bool

    def __init__(self, success):
        self.success = success


class SetCategoryService(ServiceBase):
    """
    set_category のメイン処理を担当する
    """

    request: RequestSetCategory

    def __init__(self, request: RequestSetCategory):
        self.request = request

    def main_process(self) -> HttpResponse:
        try:
            return self.__process()
        except Exception as e:
            logger.error(f'<SetCategoryService.main_process>: {e}')
            return HttpResponse(e)

    def __process(self) -> HttpResponse:
        with transaction.atomic():
            Categories(
                name=self.request.name,
                type=self.request.type
            ).save()

        res = ResponseSetCategory(True)
        return self.response(res)
