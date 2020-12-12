"""定义learning_logs的api"""

from django.urls import path, re_path

from . import views

app_name = 'api'

urlpatterns = [
    # 显示所有暴露的接口
    re_path(r'^show_all_api/$', views.show_all_api, name='show_all_api'),
    # 增加暴露的接口
    re_path(r'^new_api/$', views.new_api, name='new_api'),
    # 修改暴露的接口
    re_path(r'^edit_api/?P<api_id>(\d+)/$', views.edit_api, name='edit_api'),

    # 现在开始是非html接口
    # 添加topic的接口 /api/add_topic
    re_path(r'^add_topic/', views.add_topic, name='add_topic'),
    # 添加指定topic下的entry  /api/add_entry
    re_path(r'^add_entry/$', views.add_entry, name='add_entry'),
    # 获取topic列表 /api/get_topic_lists
    re_path(r'^get_topic_lists/$', views.get_topic_lists, name='get_topic_lists'),
    # 获取某个topic的entry列表 /api/get_entry_lists
    re_path(r'^get_entry_lists/$', views.get_entry_lists, name='get_entry_lists'),
    # 删除topic接口 /api/delete_topic
    re_path(r'^delete_topic/$', views.delete_topic, name='delete_topic'),
    # 删除entry接口 /api/delete_entry
    re_path(r'^delete_entry/$', views.delete_entry, name='delete_entry'),
]
