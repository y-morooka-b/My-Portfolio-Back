from dataclasses import dataclass
from datetime import date
from typing import List, Any
from django.db.models import F, Sum
from django.http import HttpResponse
from household_budget.libraries.core import ServiceBase, ResponseBase, RequestBase
from household_budget.models import IncomeAndExpenditureRecord

import calendar
import logging

logger = logging.getLogger()


@dataclass
class RequestGetIncomeAndExpenditure(RequestBase):
    """ get_income_and_expenditure のリクエストデータクラス """
    year: int
    month: int

    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month
        super().__init__()


@dataclass
class IncomeAndExpenditureMatrixSet:
    """ 収支のマトリックス管理セットのクラス """
    day: int
    weekday: str
    income: int
    expenditure: int
    matrix: List[dict[str, Any]]

    def __init__(self, day: int, weekday: str, matrix: List[dict[str, Any]]):
        self.day = day
        self.weekday = weekday
        self.matrix = matrix


class ResponseGetIncomeAndExpenditure(ResponseBase):
    """ get_income_and_expenditure のレスポンスデータクラス """
    matrix_set_list: List[IncomeAndExpenditureMatrixSet]

    def __init__(self) -> None:
        self.matrix_set_list = []

    def add_matrix_set(self, matrix_set_list: IncomeAndExpenditureMatrixSet) -> None:
        """ マトリックス管理セットの追加 """
        self.matrix_set_list.append(matrix_set_list)


class GetIncomeAndExpenditure(ServiceBase):
    """ get_income_and_expenditure のメイン処理を担当する """

    request: RequestGetIncomeAndExpenditure

    def __init__(self, request: RequestGetIncomeAndExpenditure):
        self.request = request

    def main_process(self) -> HttpResponse:
        try:
            return self.__process()
        except Exception as e:
            logger.error(f'<GetCategoryService.main_process>: {e}')
            return HttpResponse(e)

    def __process(self) -> HttpResponse:
        res = ResponseGetIncomeAndExpenditure()

        for day, weekday in self.__get_dates_and_weekdays(self.request.year, self.request.month):
            matrix = (IncomeAndExpenditureRecord.objects
            .annotate(category_name=F('category_id__name'))
            .prefetch_related('Categories').filter(
                date__year=self.request.year,
                date__month=self.request.month,
                date__day=day
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

            income_expenditure_matrix_set = IncomeAndExpenditureMatrixSet(day, weekday, list(matrix))
            records = matrix.filter(category_id__type=0)
            income_expenditure_matrix_set.expenditure = sum(item["amount"] for item in records)
            records = matrix.filter(category_id__type=1)
            income_expenditure_matrix_set.income = sum(item["amount"] for item in records)

            res.add_matrix_set(income_expenditure_matrix_set)
        return self.response(res)

    def __get_dates_and_weekdays(self, year, month) -> List:
        """ 指定年月の全日付と曜日を取得 """
        weekday_jp = ["月", "火", "水", "木", "金", "土", "日"]
        _, last_day = calendar.monthrange(year, month)
        result = []
        for day in range(1, last_day + 1):
            d = date(year, month, day)
            result.append((day, weekday_jp[d.weekday()]))
        return result
