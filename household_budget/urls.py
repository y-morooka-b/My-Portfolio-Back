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
    path('get_categories', views.get_categories, name='get_categories'),
    path('set_category', views.set_category, name='set_category')
]
