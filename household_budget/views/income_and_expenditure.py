from household_budget.services.del_income_and_expenditure import RequestDelIncomeAndExpenditure, DelIncomeAndExpenditureService
from household_budget.services.get_income_and_expenditure_matrix_set import GetIncomeAndExpenditureMatrixSetService, RequestGetIncomeAndExpenditureMatrixSet
from household_budget.services.get_income_and_expenditure_record import RequestGetIncomeAndExpenditure, GetIncomeAndExpenditure
from household_budget.services.set_income_and_expenditure import RequestSetIncomeAndExpenditure, SetIncomeAndExpenditure
from household_budget.services.update_income_and_expenditure import RequestUpdateIncomeAndExpenditure, UpdateIncomeAndExpenditureService

# 収支

def get_income_and_expenditure(request):
    """ 収支一覧を取得する """
    request = RequestGetIncomeAndExpenditure.from_json(request.body.decode("utf-8"))
    obj = GetIncomeAndExpenditure(request)
    return obj.main_process()

def set_income_and_expenditure(request):
    """ 収支を設定する """
    request = RequestSetIncomeAndExpenditure.from_json(request.body.decode("utf-8"))
    obj = SetIncomeAndExpenditure(request)
    return obj.main_process()

def del_income_and_expenditure(request):
    """ 収支を削除する """
    request = RequestDelIncomeAndExpenditure.from_json(request.body.decode("utf-8"))
    obj = DelIncomeAndExpenditureService(request)
    return obj.main_process()

def update_income_and_expenditure(request):
    """ 収支を更新する """
    request = RequestUpdateIncomeAndExpenditure.from_json(request.body.decode("utf-8"))
    obj = UpdateIncomeAndExpenditureService(request)
    return obj.main_process()

def get_income_and_expenditure_matrix_set(request):
    """ 1日分の収支を取得 """
    request = RequestGetIncomeAndExpenditureMatrixSet.from_json(request.body.decode("utf-8"))
    obj = GetIncomeAndExpenditureMatrixSetService(request)
    return obj.main_process()
