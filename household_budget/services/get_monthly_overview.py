from typing import List, Any
from datetime import datetime
from django.db.models import F, Sum
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
    sum_income_list: List[dict[str, Any]] = []
    sum_expenditure_list: List[dict[str, Any]] = []

    def __init__(self):
        self.sum_income_list = []
        self.sum_expenditure_list = []


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
        )

        self._response.sum_income_list = list(income_and_expenditure.filter(category_type=0).values("category_name", "category_type").annotate(total=Sum("amount")))
        self._response.sum_expenditure_list = list(income_and_expenditure.filter(category_type=1).values("category_name", "category_type").annotate(total=Sum("amount")))

        return self.response(self._response)
