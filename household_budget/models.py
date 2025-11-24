from django.db import models

# Create your models here.
class Categories(models.Model):
    """ カテゴリテーブルのクラス

    家計簿の収支のカテゴリを管理するテーブル
    """

    # ID
    id = models.AutoField(primary_key=True)
    # カテゴリ名
    name = models.CharField(max_length=200)
    # 収支のタイプ
    type = models.IntegerField()
