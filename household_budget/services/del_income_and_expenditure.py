from household_budget.libraries.core import RequestBase, ServiceBase, ResponseBase
from household_budget.models import IncomeAndExpenditureRecord

import logging

logger = logging.getLogger()


class RequestDelIncomeAndExpenditure(RequestBase):
    """ del_income_and_expenditure のリクエストデータクラス """
    id: int

    def __init__(self, id: int):
        self.id = id
        super().__init__()


class ResponseDelIncomeAndExpenditure(ResponseBase):
    """ del_income_and_expenditure のレスポンスデータクラス """
    success: bool

    def __init__(self, success: bool):
        self.success = success


class DelIncomeAndExpenditureService(ServiceBase):
    """ del_income_and_expenditure のメイン処理を担当する """
    request: RequestDelIncomeAndExpenditure

    def __init__(self, request: RequestDelIncomeAndExpenditure):
        self.request = request

    def main_process(self) -> ResponseDelIncomeAndExpenditure:
        try:
            return self.__process()
        except Exception as e:
            logger.error(f'<DelIncomeAndExpenditureService.main_process>: {e}')
            return ResponseDelIncomeAndExpenditure(False)

    def __process(self) -> ResponseDelIncomeAndExpenditure:
        (IncomeAndExpenditureRecord.objects
         .filter(id=self.request.id)
         .delete())

        return self.response(ResponseDelIncomeAndExpenditure(True))
