from django.http import HttpResponse
from django.db import transaction
from household_budget.libraries.core import ServiceBase, ResponseBase, RequestBase
from household_budget.models import Categories, IncomeAndExpenditureRecord

import logging

logger = logging.getLogger()


class RequestSetIncomeAndExpenditure(RequestBase):
    """ set_income_and_expenditure のリクエストデータクラス """
    date: str
    amount: int
    place: str
    category_id: int
    comment: str

    def __init__(self, date: str, amount: int, place: str, category_id: int, comment: str):
        self.date = date
        self.amount = amount
        self.place = place
        self.category_id = category_id
        self.comment = comment
        super().__init__()


class ResponseSetIncomeAndExpenditure(ResponseBase):
    """ set_income_and_expenditure のレスポンスデータクラス """
    success: bool

    def __init__(self, success):
        self.success = success


class SetIncomeAndExpenditure(ServiceBase):
    """ set_income_and_expenditure のメイン処理を担当する """

    request: RequestSetIncomeAndExpenditure

    def __init__(self, request: RequestSetIncomeAndExpenditure):
        self.request = request

    def main_process(self) -> HttpResponse:
        try:
            return self.__process()
        except Exception as e:
            logger.error(f'<SetCategoryService.main_process>: {e}')
            return HttpResponse(e)

    def __process(self) -> HttpResponse:
        with transaction.atomic():
            IncomeAndExpenditureRecord(
                date=self.request.date,
                amount=self.request.amount,
                place=self.request.place,
                category_id=Categories(id=self.request.category_id),
                comment=self.request.comment
            ).save()

            res = ResponseSetIncomeAndExpenditure(True)
            return self.response(res)