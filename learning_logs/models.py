from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Topic(models.Model):
    """用户存储的主题"""
    text = models.CharField(max_length=30)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        """返回模型字符串表示"""
        return self.text


class Entry(models.Model):
    """学习的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic, models.CASCADE)
    # 测试加入说明
    describe = models.TextField(default="", max_length=30)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示"""
        if len(self.text) <= 50:
            return self.text[:50]
        else:
            return self.text[:50] + '...'
