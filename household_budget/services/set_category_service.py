from django.http import HttpResponse
from django.db import transaction
from household_budget.libraries.core import ServiseBase, ResponseBase, RequestBase
from household_budget.models import Categories

import logging

logger = logging.getLogger()

class RequestSetCategory(RequestBase):
    name: str
    type: int

    def __init__(self, name: str, type: int):
        self.name = name
        self.type = type

    # def __init__(self, category_name: str, category_type: int):
    #     self.category_name = category_name
    #     self.category_type = category_type


class ResponseSetCategory(ResponseBase):
    success: bool

    def __init__(self, success):
        self.success = success


class SetCategoryService(ServiseBase):
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
