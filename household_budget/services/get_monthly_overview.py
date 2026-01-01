from enum import nonmember
from typing import List, Any
from datetime import datetime
from django.db.models import F, Sum, QuerySet, Model
from django.http import HttpResponse
from household_budget.libraries.core import ServiceBase, ResponseBase, RequestBase
from household_budget.models import IncomeAndExpenditureRecord

import logging

logger = logging.getLogger()


class RequestGetMonthlyOverview(ResponseBase):
    """ get_monthly_overview のリクエストデータクラス """

    def __init__(self):
        super().__init__()

    @classmethod
    def from_json(cls, param):
        pass


class ResponseGetMonthlyOverview(ResponseBase):
    """ get_monthly_overview のレスポンスデータクラス """

    total_expenditure: int
    total_income: int
    sum_expenditure_list: List[dict[str, Any]]
    sum_income_list: List[dict[str, Any]]

    def __init__(self):
        self.total_expenditure = 0
        self.total_income = 0
        self.sum_expenditure_list = []
        self.sum_income_list = []


class GetMonthlyOverview(ServiceBase):
    """ get_monthly_overview のメイン処理を担当する """

    request: RequestGetMonthlyOverview
    _response: ResponseGetMonthlyOverview
    
    def __init__(self, request: RequestGetMonthlyOverview):
        self.request = request
        self._response = ResponseGetMonthlyOverview()

    def main_process(self) -> HttpResponse:
        try:
            return self.__process()
        except Exception as e:
            logger.error(f'<GetMonthlyOverview.main_process>: {e}')
            return HttpResponse(e)

    def __process(self) -> HttpResponse:
        now = datetime.now()

        income_and_expenditure = (IncomeAndExpenditureRecord.objects
            .annotate(category_name=F('category_id__name'), category_type=F('category_id__type'))
            .prefetch_related('Categories')
            .filter(
                date__year=now.year,
                date__month=now.month,
            )
            .values(
                'category_name',
                'category_type',
                'amount'
            )
            .order_by('category_id__type', 'category_id__id')
        )

        self.__set_graph_data(income_and_expenditure)
        self.__set_total_amount(income_and_expenditure)

        return self.response(self._response)


    def __set_graph_data(self, income_and_expenditure: QuerySet[Model | Any, dict[str, Any]]) -> None:
        """ グラフ用データをレスポンスに設定 """

        self._response.sum_expenditure_list = list(
            income_and_expenditure
                .filter(category_type=0)
                .values("category_name", "category_type")
                .annotate(total=Sum("amount"))
        )

        self._response.sum_income_list = list(
            income_and_expenditure
                .filter(category_type=1)
                .values("category_name", "category_type")
                .annotate(total=Sum("amount"))
        )

    def __set_total_amount(self, income_and_expenditure: QuerySet[Model | Any, dict[str, Any]]) -> None:
        """ 支出の合計をレスポンスに設定 """

        records = income_and_expenditure.filter(category_id__type=0)
        self._response.total_expenditure = sum(item["amount"] for item in records)

        records = income_and_expenditure.filter(category_id__type=1)
        self._response.total_income = sum(item["amount"] for item in records)
