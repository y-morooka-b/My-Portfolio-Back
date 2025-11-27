from django.http import HttpResponse
from household_budget.services.get_categories_service import GetCategoriesService

import logging

logger = logging.getLogger()

class Hoge:
    def __init__(self):
        self.pag = 'aaaa'
        self.dom = 1


# Create your views here.
def get_categories(request):
    """ カテゴリ一覧を取得する """
    obj = GetCategoriesService()
    return obj.main_process()
