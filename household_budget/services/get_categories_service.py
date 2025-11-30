from dataclasses import dataclass
from typing import Any, List
from django.http import HttpResponse
from household_budget.libraries.core import ResponseBase, ServiseBase
from household_budget.models import Categories

import logging

logger = logging.getLogger()

@dataclass
class ResponseGetCategories(ResponseBase):
    """
    get_categories のレスポンスデータクラス
    """

    categories: List[dict[str, Any]]

    def __init__(self, categories):
        self.categories = categories

class GetCategoriesService(ServiseBase):
    """
    get_categories のメイン処理を担当する
    """

    def main_process(self) -> HttpResponse:
        try:
            return self.__process()
        except Exception as e:
            logger.error(f'<GetCategoriesService.main_process>: {e}')
            return HttpResponse(e)

    def __process(self) -> HttpResponse:
        drops = Categories.objects.all()
        drops= list(drops.values())

        res = ResponseGetCategories(drops)
        return self.response(res)
