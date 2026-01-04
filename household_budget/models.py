from django.db import models

# Create your models here.
class Categories(models.Model):
    """ カテゴリテーブルのクラス

    家計簿の収支のカテゴリを管理するテーブル
    """
    objects = models.Manager()

    # ID
    id = models.AutoField(primary_key=True)
    # カテゴリ名
    name = models.CharField(max_length=200)
    # 収支のタイプ
    type = models.IntegerField()

class IncomeAndExpenditureRecord(models.Model):
    """ 収支記録テーブルのクラス

    家計簿の収支記録を管理するテーブル
    """
    objects = models.Manager()

    # ID
    id = models.AutoField(primary_key=True)
    # 金額
    amount = models.IntegerField()
    # 購入場所・収入場所
    place = models.TextField(default='')
    # カテゴリID
    category_id = models.ForeignKey(Categories, on_delete=models.PROTECT)
    # 取引日
    date = models.DateField()
    # フリーコメント
    comment = models.TextField(blank=True)
    # レコード登録日付
    log_time = models.DateTimeField(auto_now_add=True)
