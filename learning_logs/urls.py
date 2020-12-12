"""定义learning_logs的url模式"""

from django.urls import path, re_path

from . import views

app_name = 'learning_logs'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    # 显示所有主题
    re_path(r'^topics/$', views.topics, name='topics'),
    # 显示特定主题的页面
    re_path(r'^topics/?P<topic_id>(\d+)/$', views.topic, name='topic'),
    #用于添加新标题的网页
    re_path(r'^new_topic/$', views.new_topic, name='new_topic'),
    # 用于添加新条目的网页
    re_path(r'^new_entry/?P<topic_id>(\d+)/$', views.new_entry, name='new_entry'),
    # 用于重新编辑新条目的网页
    re_path(r'^edit_entry/?P<entry_id>(\d+)/$', views.edit_entry, name='edit_entry'),
    # 用于删除条目的接口
    re_path(r'^delete_entry/?P<entry_id>(\d+)/$', views.delete_entry, name='delete_entry'),
]
