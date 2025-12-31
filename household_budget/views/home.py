from django.http import HttpResponse

from household_budget.services.get_monthly_overview import RequestGetMonthlyOverview, GetMonthlyOverview


# ホーム

def get_monthly_overview(request):
    """ 当月の概要を取得する """
    request = RequestGetMonthlyOverview.from_json(request.body.decode("utf-8"))
    obj = GetMonthlyOverview(request)
    return obj.main_process()