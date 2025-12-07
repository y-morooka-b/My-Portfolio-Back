from household_budget.services.del_category_service import RequestDelCategory, DelCategoryService
from household_budget.services.get_categories_service import GetCategoriesService
from household_budget.services.get_income_and_expenditure_record import GetIncomeAndExpenditure, RequestGetIncomeAndExpenditure
from household_budget.services.set_category_service import SetCategoryService, RequestSetCategory
from household_budget.services.set_income_and_expenditure import RequestSetIncomeAndExpenditure, SetIncomeAndExpenditure
from household_budget.services.update_category import RequestUpdateCategory, UpdateCategoryService

# カテゴリ
def get_categories(request):
    """ カテゴリ一覧を取得する """
    obj = GetCategoriesService()
    return obj.main_process()

def set_category(request):
    """ カテゴリを設定する """
    request = RequestSetCategory.from_json(request.body.decode("utf-8"))
    obj = SetCategoryService(request)
    return obj.main_process()

def del_category(request):
    """ カテゴリを削除する """
    request = RequestDelCategory.from_json(request.body.decode("utf-8"))
    obj = DelCategoryService(request)
    return obj.main_process()

def update_category(request):
    """ カテゴリを更新する """
    request = RequestUpdateCategory.from_json(request.body.decode("utf-8"))
    obj = UpdateCategoryService(request)
    return obj.main_process()


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
