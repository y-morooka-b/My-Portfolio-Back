from django.urls import path
from .views import categories
from .views import income_and_expenditure

app_name = 'household_budget'

urlpatterns = [
    # カテゴリ関連
    path('get_categories', categories.get_categories, name='get_categories'),
    path('set_category', categories.set_category, name='set_category'),
    path('del_category', categories.del_category, name='del_category'),
    path('update_category', categories.update_category, name='update_category'),
    # 収支関連
    path('get_income_and_expenditure', income_and_expenditure.get_income_and_expenditure, name='get_income_and_expenditure'),
    path('set_income_and_expenditure', income_and_expenditure.set_income_and_expenditure, name='set_income_and_expenditure'),
    path('del_income_and_expenditure', income_and_expenditure.del_income_and_expenditure, name='del_income_and_expenditure'),
    path('update_income_and_expenditure', income_and_expenditure.update_income_and_expenditure, name='update_income_and_expenditure'),
]
