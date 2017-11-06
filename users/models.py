from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=30,blank=True)

    class Meta(AbstractUser.Meta):
        pass


class BeautyUsers(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    user_type = models.BigIntegerField(default=0)
    nickname = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    birthday = models.CharField(max_length=30)
    gender = models.IntegerField(default=0)

    update_date = models.DateField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    add_people = models.ForeignKey(User)

    def __str__(self):
        return self.nickname
    # ,self.gender
        # return '{},{}'.format(self.nickname, self.gender)
    class Meta:
        db_table = 'BeautyUsers' #自定义表名称为mytable
        verbose_name = '黑名单列表' #指定在admin管理界面中显示的名称
        ordering = ['user_id']