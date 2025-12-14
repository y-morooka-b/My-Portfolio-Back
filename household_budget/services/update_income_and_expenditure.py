from dataclasses import dataclass
from django.http import HttpResponse
from household_budget.libraries.core import RequestBase, ResponseBase, ServiceBase
from household_budget.models import IncomeAndExpenditureRecord

import logging
logger = logging.getLogger()

@dataclass
class RequestUpdateIncomeAndExpenditure(RequestBase):
    """ update_income_and_expenditure のリクエストデータクラス """
    id: int
    amount: int
    place: str
    category_id: int
    date: str
    comment: str

    def __init__(self, id: int, amount: int, place: str, category_id: int, date: str, comment: str):
        self.id = id
        self.amount = amount
        self.place = place
        self.category_id = category_id
        self.date = date
        self.comment = comment
        super().__init__()


@dataclass
class ResponseUpdateIncomeAndExpenditure(ResponseBase):
    """ update_income_and_expenditure のレスポンスデータクラス """
    success: bool

    def __init__(self, success: bool):
        self.success = success


class UpdateIncomeAndExpenditureService(ServiceBase):
    """ update_income_and_expenditure のメイン処理を担当する """
    request: RequestUpdateIncomeAndExpenditure

    def __init__(self, request: RequestUpdateIncomeAndExpenditure):
        self.request = request

    def main_process(self) -> HttpResponse:
        try:
            return self.__process()
        except Exception as e:
            logger.error(f'<UpdateIncomeAndExpenditureService.main_process>: {e}')
            return HttpResponse(e)

    def __process(self) -> HttpResponse:
        (IncomeAndExpenditureRecord.objects
        .filter(id=self.request.id)
        .update(
            date=self.request.date,
            amount=self.request.amount,
            place=self.request.place,
            category_id=self.request.category_id,
            comment=self.request.comment
        ))
        return self.response(ResponseUpdateIncomeAndExpenditure(True))
