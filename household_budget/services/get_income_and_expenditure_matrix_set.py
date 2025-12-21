from dataclasses import dataclass

from django.db.models import F
from django.http import HttpResponse
from household_budget.libraries.core import RequestBase, ServiceBase, ResponseBase
from household_budget.models import IncomeAndExpenditureRecord
from household_budget.services.get_income_and_expenditure_record import IncomeAndExpenditureMatrixSet

import logging
import datetime as dt
import locale

logger = logging.getLogger()

@dataclass
class RequestGetIncomeAndExpenditureMatrixSet(RequestBase):
    """ get_income_and_expenditure_matrixSet のリクエストデータクラス """
    year: int
    month: int
    day: int

    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day
        super().__init__()


@dataclass
class ResponseGetIncomeAndExpenditureMatrixSet(ResponseBase):
    matrix_set: IncomeAndExpenditureMatrixSet

    def __init__(self, matrix_set:IncomeAndExpenditureMatrixSet) -> None:
        self.matrix_set = matrix_set


class GetIncomeAndExpenditureMatrixSetService(ServiceBase):
    request: RequestGetIncomeAndExpenditureMatrixSet

    def __init__(self, request: RequestGetIncomeAndExpenditureMatrixSet):
        self.request = request


    def main_process(self) -> HttpResponse:
        try:
            return self.__process()
        except Exception as e:
            logger.error(f'<GetIncomeAndExpenditureMatrixSetService.main_process>: {e}')
            return HttpResponse(e)


    def __process(self) -> HttpResponse:
        matrix = (IncomeAndExpenditureRecord.objects
            .annotate(category_name=F('category_id__name'))
            .prefetch_related('Categories').filter(
                date__year=self.request.year,
                date__month=self.request.month,
                date__day=self.request.day
            )
            .values(
                'id',
                'date',
                'amount',
                'place',
                'comment',
                'category_name',
                'category_id'
            )
            .order_by('category_id__type'))

        income_expenditure_matrix_set = IncomeAndExpenditureMatrixSet(self.request.day, self.__get_day_of_the_week(), list(matrix))

        # 支出
        records = matrix.filter(category_id__type=0)
        income_expenditure_matrix_set.expenditure = sum(item["amount"] for item in records)
        # 収入
        records = matrix.filter(category_id__type=1)
        income_expenditure_matrix_set.income = sum(item["amount"] for item in records)

        return self.response(ResponseGetIncomeAndExpenditureMatrixSet(income_expenditure_matrix_set))


    def __get_day_of_the_week(self) -> str:
        """ 日付の取得 """
        locale.setlocale(locale.LC_TIME, '')
        date = dt.date(self.request.year, self.request.month, self.request.day)
        return date.strftime('%a')
