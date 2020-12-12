from django.db import models


# Create your models here.

class ApiDescribe(models.Model):
    """所有api"""
    name = models.CharField(max_length=200)
    describe = models.CharField(max_length=200)
    url = models.URLField()

    METHOD_CHOICE = (
        ('GET','GET'),
        ('POST', 'POST'),
        ('DELETE', 'DELETE'),
    )
    method = models.CharField(max_length=200, choices=METHOD_CHOICE)

    date_added = models.DateTimeField(auto_now_add=True)
    input_para = models.CharField(max_length=400)
    return_value = models.CharField(max_length=400)
    status_code = models.CharField(max_length=400)
    attention = models.CharField(max_length=400)

    def __str__(self):
        """返回模型字符串表示"""
        return self.name
