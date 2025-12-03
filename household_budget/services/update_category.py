from django.http import HttpResponse
from django.db import transaction
from household_budget.libraries.core import ServiceBase, ResponseBase, RequestBase
from household_budget.models import Categories

import logging

logger = logging.getLogger()

class RequestUpdateCategory(RequestBase):
    """
    update_category のリクエストデータクラス
    """
    id: int
    name: str
    type: int

    def __init__(self, id: int, name: str, type: int):
        self.id = id
        self.name = name
        self.type = type
        super().__init__()

class ResponseUpdateCategory(ResponseBase):
    """
    update_category のレスポンスデータクラス
    """
    success: bool

    def __init__(self, success):
        self.success = success


class UpdateCategoryService(ServiceBase):
    """
    update_category のメイン処理を担当する
    """

    request: RequestUpdateCategory

    def __init__(self, request: RequestUpdateCategory):
        self.request = request

    def main_process(self) -> HttpResponse:
        try:
            return self.__process()
        except Exception as e:
            logger.error(f'<UpdateCategoryService.main_process>: {e}')
            return HttpResponse(e)

    def __process(self) -> HttpResponse:
        with transaction.atomic():
            Categories.objects.filter(
                id=self.request.id
            ).update(
                name=self.request.name,
                type=self.request.type
            )

        res = ResponseUpdateCategory(True)
        return self.response(res)
