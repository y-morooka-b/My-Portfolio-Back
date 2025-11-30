from django.db.models import QuerySet
from django.http import HttpResponse
from household_budget.libraries.core import ResponseBase, ServiseBase
from django.core import serializers
from household_budget.models import Categories

import json
import logging

logger = logging.getLogger()


class ResponseGetCategories(ResponseBase):
    """
    get_categories のレスポンスデータクラス
    """

    categories:QuerySet

    def __init__(self, categories):
        self.categories = categories

    def to_json(self):
        """ json文字列にシリアライズ """
        return json.dumps({
            'categories': serializers.serialize('json', self.categories)
        })

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
        res = ResponseGetCategories(drops)
        return self.response(res)