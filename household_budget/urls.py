# from rest_framework import routers
# from .views import CategoriesViewSet, test_view_set
#
# router = routers.DefaultRouter()
# router.register('categories', CategoriesViewSet)
# urlpatterns = router.urls


from django.urls import path
from . import views

app_name = 'household_budget'

urlpatterns = [
    # カテゴリ関連
    path('get_categories', views.get_categories, name='get_categories'),
    path('set_category', views.set_category, name='set_category'),
    path('del_category', views.del_category, name='del_category'),
    path('update_category', views.update_category, name='update_category'),
    # 収支関連
    path('get_income_and_expenditure', views.get_income_and_expenditure, name='get_income_and_expenditure'),
    path('set_income_and_expenditure', views.set_income_and_expenditure, name='set_income_and_expenditure'),
    path('del_income_and_expenditure', views.del_income_and_expenditure, name='del_income_and_expenditure'),
    path('update_income_and_expenditure', views.update_income_and_expenditure, name='update_income_and_expenditure'),
]
